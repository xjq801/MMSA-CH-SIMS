"""Prepare the author-released VC-CSA source without vendoring it.

The author-original experiment consumes target-comment text and author-provided
comment-level splits.  It is intentionally kept separate from the project's T0
video-level protocol.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Dict, Iterable
import zipfile


EXPECTED_AUTHOR_REVISION = "3e8c42608f4e89bc2082c55760aa63535e8e276a"


def load_reproduction_contract(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_reproduction_contract(contract: Dict) -> None:
    source = contract.get("source", {})
    scope = contract.get("claim_scope", {})
    smoke = contract.get("smoke", {})
    if source.get("revision") != EXPECTED_AUTHOR_REVISION:
        raise ValueError("author source revision is not the frozen revision")
    if scope.get("classification") != "AUTHOR_ORIGINAL_SETTING_NON_T0":
        raise ValueError("author-original run must remain NON_T0")
    if not scope.get("uses_target_comment_text") or scope.get("split_unit") != "comment":
        raise ValueError("author-original input and split semantics changed")
    if scope.get("t0_adaptation") or scope.get("may_be_reported_as_t0_baseline"):
        raise ValueError("T0 adaptation requires a separate REIMPLEMENTATION experiment")
    if smoke.get("test_examples") != 0 or smoke.get("may_be_reported_as_reproduction"):
        raise ValueError("smoke must not access test or be reported as reproduction")


def verify_source_revision(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    revision = result.stdout.strip()
    if revision != EXPECTED_AUTHOR_REVISION:
        raise ValueError(
            f"unexpected author revision: expected {EXPECTED_AUTHOR_REVISION}, got {revision}"
        )
    return revision


def build_smoke_inputs(
    comments_source: Path,
    output_dir: Path,
    train_examples: int = 8,
    dev_examples: int = 4,
) -> Dict:
    """Create ignored smoke-only inputs while making test access impossible."""
    if train_examples < 1 or dev_examples < 1:
        raise ValueError("smoke requires positive train and dev example counts")
    output_dir.mkdir(parents=True, exist_ok=True)
    train = json.loads((comments_source / "train_set.json").read_text(encoding="utf-8"))
    dev = json.loads((comments_source / "dev_set.json").read_text(encoding="utf-8"))
    selected_train = train[:train_examples]
    selected_dev = dev[:dev_examples]
    if len(selected_train) != train_examples or len(selected_dev) != dev_examples:
        raise ValueError("author split is smaller than the requested smoke subset")

    for name in (
        "video_to_comment.json",
        "opinion_label_map.json",
        "emotion_label_map.json",
    ):
        shutil.copyfile(comments_source / name, output_dir / name)

    archive_path = comments_source / "lable_data_dict.json.zip"
    with zipfile.ZipFile(archive_path) as archive:
        members = [name for name in archive.namelist() if not name.endswith("/")]
        if members != ["lable_data_dict.json"]:
            raise ValueError(f"unexpected annotation archive members: {members}")
        with archive.open(members[0]) as source_handle, (
            output_dir / "lable_data_dict.json"
        ).open("wb") as target_handle:
            shutil.copyfileobj(source_handle, target_handle)

    for name, values in (
        ("train_set.json", selected_train),
        ("dev_set.json", selected_dev),
        ("test_set.json", []),
    ):
        with (output_dir / name).open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(values, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

    return {
        "schema_version": "task20-vccsa-author-smoke-input-v1",
        "status": "SMOKE_INPUTS_READY_NO_TEST",
        "train_examples": len(selected_train),
        "dev_examples": len(selected_dev),
        "test_examples": 0,
        "files": {
            path.name: _sha256(path)
            for path in sorted(output_dir.iterdir())
            if path.is_file()
        },
    }


def _replace_once_or_already(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise ValueError(f"cannot patch {label}: expected upstream text is absent")
    return text.replace(old, new, 1)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_if_changed(path: Path, text: str) -> bool:
    original = path.read_text(encoding="utf-8")
    if original == text:
        return False
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return True


def apply_compatibility_patch(source_root: Path) -> Dict:
    required = [
        source_root / "utils" / "tokenize.py",
        source_root / "csmv_dataset.py",
        source_root / "script" / "train.sh",
        source_root / "script" / "eval.sh",
        source_root / "main.py",
        source_root / "model_VCCSA.py",
        source_root / "utils" / "compute_args.py",
    ]
    missing = [path.name for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"author source files missing: {missing}")

    changed = []
    (
        tokenize_path,
        dataset_path,
        train_path,
        eval_path,
        main_path,
        model_path,
        compute_args_path,
    ) = required

    tokenize = tokenize_path.read_text(encoding="utf-8")
    tokenize = _replace_once_or_already(
        tokenize,
        "import en_vectors_web_lg\n",
        "try:\n    import en_vectors_web_lg\nexcept ModuleNotFoundError:\n    en_vectors_web_lg = None\n",
        "optional legacy GloVe import",
    )
    tokenize = _replace_once_or_already(
        tokenize,
        "    if use_glove:\n        spacy_tool = en_vectors_web_lg.load()",
        "    if use_glove:\n        if en_vectors_web_lg is None:\n"
        "            raise RuntimeError(\"legacy GloVe path requires en_vectors_web_lg\")\n"
        "        spacy_tool = en_vectors_web_lg.load()",
        "legacy GloVe error",
    )
    if _write_if_changed(tokenize_path, tokenize):
        changed.append("utils/tokenize.py")

    dataset = dataset_path.read_text(encoding="utf-8")
    known_model_paths: Iterable[str] = (
        '"~/.cache/torch/hub/transformers/roberta-base"',
        '"/home/jac/.cache/torch/hub/transformers/roberta-base"',
    )
    replacements = 0
    for pretrained_path_literal in known_model_paths:
        count = dataset.count(f"pretrained_model_name_or_path={pretrained_path_literal}")
        count += dataset.count(f"pretrained_model_name_or_path = {pretrained_path_literal}")
        dataset = dataset.replace(
            f"pretrained_model_name_or_path={pretrained_path_literal}",
            "pretrained_model_name_or_path=args.pre_trained_LM",
        ).replace(
            f"pretrained_model_name_or_path = {pretrained_path_literal}",
            "pretrained_model_name_or_path = args.pre_trained_LM",
        )
        replacements += count
    if "args.pre_trained_LM" not in dataset or replacements == 0 and dataset_path.read_text(encoding="utf-8") == dataset:
        if "args.pre_trained_LM" not in dataset:
            raise ValueError("cannot parameterize dataset RoBERTa path")
    if _write_if_changed(dataset_path, dataset):
        changed.append("csmv_dataset.py")

    train = train_path.read_text(encoding="utf-8")
    if "pre_trained_lm=" not in train:
        train = train.replace(
            "video_feature=../dataset/csmv/visual-feature\n",
            "video_feature=../dataset/csmv/visual-feature\n"
            "pre_trained_lm=${PRETRAINED_LM:-../models/roberta-base}\n",
            1,
        ).replace(
            "video_feature=../visual-feature\n",
            "video_feature=../visual-feature\n"
            "pre_trained_lm=${PRETRAINED_LM:-../models/roberta-base}\n",
            1,
        )
    train = train.replace("--video_feature_dir ${video_feature_dir} \\ \n", "--video_feature_dir ${video_feature} \\\n")
    train = train.replace("--video_feature_dir ${video_feature_dir} \\\n", "--video_feature_dir ${video_feature} \\\n")
    if "--pre_trained_LM ${pre_trained_lm}" not in train:
        train = train.replace(
            "--datadir ${comment_text}",
            "--pre_trained_LM ${pre_trained_lm} \\\n--datadir ${comment_text}",
            1,
        ).replace(
            "--datadir ../comments",
            "--pre_trained_LM ${pre_trained_lm} \\\n--datadir ../comments",
            1,
        )
    if "--video_feature_dir ${video_feature}" not in train or "\\ " in train:
        raise ValueError("train launcher compatibility patch did not verify")
    if _write_if_changed(train_path, train):
        changed.append("script/train.sh")

    evaluate = eval_path.read_text(encoding="utf-8")
    if "pre_trained_lm=" not in evaluate:
        anchor = "video_feature=../dataset/csmv/visual-feature\n"
        if anchor not in evaluate:
            anchor = "python ../main_eval.py \\\n"
            evaluate = evaluate.replace(
                anchor,
                "pre_trained_lm=${PRETRAINED_LM:-../models/roberta-base}\n" + anchor,
                1,
            )
        else:
            evaluate = evaluate.replace(
                anchor,
                anchor + "pre_trained_lm=${PRETRAINED_LM:-../models/roberta-base}\n",
                1,
            )
    if "--pre_trained_LM ${pre_trained_lm}" not in evaluate:
        evaluate = evaluate.replace(
            "--datadir ${comment_text}",
            "--pre_trained_LM ${pre_trained_lm} \\\n--datadir ${comment_text}",
            1,
        ).replace(
            "--datadir ../comments",
            "--pre_trained_LM ${pre_trained_lm} \\\n--datadir ../comments",
            1,
        )
    if "--pre_trained_LM ${pre_trained_lm}" not in evaluate:
        raise ValueError("eval launcher compatibility patch did not verify")
    if _write_if_changed(eval_path, evaluate):
        changed.append("script/eval.sh")

    entrypoints = [main_path]
    entrypoints.extend(
        path
        for path in (source_root / "main_eval.py", source_root / "main_multigpu.py")
        if path.is_file()
    )
    for entrypoint in entrypoints:
        entrypoint_text = entrypoint.read_text(encoding="utf-8")
        entrypoint_text = entrypoint_text.replace(
            ", CSMV_Dataset_VideoMAEv2FPS16", ""
        )
        if "CSMV_Dataset_VideoMAEv2FPS16" in entrypoint_text:
            raise ValueError(f"invalid dataset import remains in {entrypoint.name}")
        if _write_if_changed(entrypoint, entrypoint_text):
            changed.append(str(entrypoint.relative_to(source_root)).replace("\\", "/"))

    model = model_path.read_text(encoding="utf-8")
    without_imports = model.replace("from layers.fc import MLP\n", "").replace(
        "from layers.layer_norm import LayerNorm\n", ""
    )
    if "MLP" in without_imports or "LayerNorm" in without_imports:
        raise ValueError("missing layers package is referenced beyond dead imports")
    if _write_if_changed(model_path, without_imports):
        changed.append("model_VCCSA.py")

    compute_args = compute_args_path.read_text(encoding="utf-8")
    if "args.aux_task = False" not in compute_args:
        compute_args = _replace_once_or_already(
            compute_args,
            "    return args",
            "    args.aux_task = False\n    return args",
            "disabled undeclared auxiliary task default",
        )
    if _write_if_changed(compute_args_path, compute_args):
        changed.append("utils/compute_args.py")

    return {
        "schema_version": "task20-vccsa-author-patch-report-v1",
        "status": "PATCHED_AND_VERIFIED",
        "changed_files": changed,
        "post_patch_sha256": {
            str(path.relative_to(source_root)).replace("\\", "/"): _sha256(path)
            for path in required
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    contract = load_reproduction_contract(args.contract)
    validate_reproduction_contract(contract)
    revision = verify_source_revision(args.repo_root)
    report = {"revision": revision, "contract_status": "VALID"}
    if args.apply:
        report["patch"] = apply_compatibility_patch(args.repo_root / "source_vcssa")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
