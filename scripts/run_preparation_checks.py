"""Repeatable local acceptance checks for the M1 preparation package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

from validate_experiment_config import validate
from validate_protocol_freeze import validate_protocol_freeze
from validate_m1_public_audit import validate_m1_public_audit
from validate_literature_freeze import validate_literature_freeze
from validate_m2_data_engineering import validate_m2_data_engineering
from validate_m2_release import validate_m2_release
from validate_second_primary_readonly_audit import validate_second_primary_readonly_audit
from validate_lai_gai_osf_metadata_audit import validate_lai_gai_osf_metadata_audit
from validate_lai_gai_osf_api_metadata import validate_lai_gai_osf_api_metadata
from validate_lai_gai_second_primary import validate_lai_gai_second_primary
from validate_csmv_media_lineage import validate_csmv_media_lineage
from validate_csmv_feature_preflight import validate_csmv_feature_preflight
from validate_csmv_i3d_sequence_protocol import validate as validate_csmv_i3d_sequence_protocol
from validate_work_log import validate_work_log


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ".gitignore",
    ".env.example",
    "T0_INPUT_POLICY.md",
    "DATA_SOURCE_LEDGER.md",
    "ENVIRONMENT_LOCK.md",
    "requirements-lock.txt",
    "PROJECT_STRUCTURE_POLICY.md",
    "configs/experiment.bootstrap.yaml",
    "experiments/EXPERIMENT_REGISTRY.md",
    "CLAIM_EVIDENCE_MATRIX.md",
    "SECURITY_COMPLIANCE_CHECKLIST.md",
    "RESOURCE_TIME_POLICY.md",
    "WORK_RECORD_POLICY.md",
    "WORK_LOG.md",
    "AGENTS.md",
    "legacy-asset-lineage.md",
    "legacy-experiment-classification.md",
    "research-question-v1.md",
    "experiment-protocol-v1.md",
    "leakage-threat-model.md",
    "M1_PUBLIC_DATA_AUDIT.md",
    "CSMV_MEDIA_LINEAGE_AUDIT_20260715.md",
    "LABEL_SPACE_MAPPING_DRAFT.md",
    "DATASET_SELECTION_DECISION.md",
    "LITERATURE_SEARCH_REPORT.md",
    "CONTRIBUTION_PRIOR_ART_MATRIX.md",
    "CARM_NAME_AUDIT.md",
    "RESEARCH_PROTOCOL_FREEZE_AUDIT.md",
    "BASELINE_CANDIDATES.md",
    "DATA_DICTIONARY.md",
    "M2_DATA_PROTOCOL.md",
    "SILVER_LABEL_PROTOCOL.md",
    "LABEL_ERROR_REVIEW_PROTOCOL.md",
    "NEAR_DUPLICATE_SOURCE_AUDIT.md",
    "CUC_CANONICAL_AUDIT.md",
    "configs/silver-label-pipeline-v1.yaml",
    "M2_LEAKAGE_AUDIT.md",
    "DATA_AUDIT_REPORT_V1.md",
    "DATA_CARD_DATASET_V1.md",
    "DATASHEET_DATASET_V1.md",
    "PRIVACY_STATEMENT.md",
    "PLATFORM_TERMS_STATEMENT.md",
    "DATA_RELEASE_BOUNDARY.md",
    "G1_G2_EVIDENCE_MATRIX.md",
    "HANDOFF_10.md",
    "M1_SECOND_PRIMARY_SHORTLIST_20260714.md",
    "M1_LIRIS_ACCEDE_DEEP_AUDIT_20260714.md",
    "HANDOFF_10_SECOND_PRIMARY_READONLY.md",
    "M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md",
    "M1_LAI_GAI_OSF_API_METADATA_AUDIT_20260714.md",
    "TASK00_LAI_GAI_OSF_API_METADATA_REVIEW_20260714.md",
    "TASK00_SECOND_PRIMARY_RESOLUTION_AUTHORIZATION_20260714.md",
    "M1_M2_LAI_GAI_SECOND_PRIMARY_FREEZE_20260714.md",
    "TASK00_LAI_GAI_SECOND_PRIMARY_FREEZE_REVIEW_20260715.md",
    "CSMV_MEDIA_LINEAGE_AUDIT_20260715.md",
    "TASK00_CSMV_LINEAGE_G2_REVIEW_20260715.md",
    "TASK00_CSMV_FEATURE_PREFLIGHT_AUTHORIZATION_20260715.md",
    "TASK00_CSMV_ONE_FEATURE_FAMILY_METADATA_COORDINATION_AUTHORIZATION_20260715.md",
    "TASK00_CSMV_I3D_METADATA_COORDINATION_ATTEMPT_REVIEW_20260715.md",
    "TASK00_CSMV_OFFICIAL_ISSUE_5_SENT_REVIEW_20260715.md",
    "TASK00_EFFICIENCY_FIRST_MIRROR_AND_ACQUISITION_POLICY_20260715.md",
    "TASK00_AUDIO_MODALITY_PROTOCOL_REVIEW_20260716.md",
    "TASK00_CSMV_I3D_SEQUENCE_PROTOCOL_AND_GIT_CHECKPOINT_REVIEW_20260716.md",
    "experiment-protocol-v2.md",
    "CSMV_I3D_GITHUB_ISSUE_REQUEST_20260715.md",
    "TASK00_CSMV_FEATURE_PREFLIGHT_G2_REVIEW_20260715.md",
    "scripts/validate_second_primary_readonly_audit.py",
    "scripts/validate_lai_gai_osf_metadata_audit.py",
    "scripts/validate_lai_gai_osf_api_metadata.py",
    "scripts/fetch_lai_gai_second_primary_assets.py",
    "scripts/build_lai_gai_second_primary.py",
    "scripts/validate_lai_gai_second_primary.py",
    "scripts/audit_lai_gai_osf_api_metadata.py",
    "scripts/build_lai_gai_osf_api_manifest.py",
    "scripts/run_m2_leakage_tests.py",
    "scripts/build_m2_release.py",
    "scripts/reproduce_m2_minimal.py",
    "scripts/validate_m2_release.py",
    "scripts/csmv_media_lineage.py",
    "scripts/validate_csmv_media_lineage.py",
    "scripts/validate_csmv_feature_preflight.py",
    "CSMV_FEATURE_ASSET_PREFLIGHT_20260715.md",
    "data/manifests/csmv-feature-preflight-v1.manifest.json",
    "CSMV_I3D_SEQUENCE_PROTOCOL_V1.md",
    "configs/csmv-i3d-sequence-protocol-v1.json",
    "scripts/csmv_i3d_sequence_protocol.py",
    "scripts/build_csmv_i3d_sequence_protocol_manifest.py",
    "scripts/validate_csmv_i3d_sequence_protocol.py",
    "tests/test_csmv_i3d_sequence_protocol.py",
    "data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json",
    "references/search/step19-23/search-protocol.json",
    "references/references.bib",
]
IGNORED_SAMPLES = [
    ".env",
    "data/raw/sample.bin",
    "data/processed/sample.pkl",
    "models/a.pt",
    "results/run.json",
]
TRACKED_SAMPLES = [
    ".env.example",
    "configs/experiment.bootstrap.yaml",
    "data/raw/README.md",
    "data/processed/README.md",
    "data/manifests/README.md",
    "paper/README.md",
    "references/references.bib",
    "WORK_RECORD_POLICY.md",
    "WORK_LOG.md",
    "AGENTS.md",
    "legacy-asset-lineage.md",
    "legacy-experiment-classification.md",
    "research-question-v1.md",
    "experiment-protocol-v1.md",
    "leakage-threat-model.md",
    "M1_PUBLIC_DATA_AUDIT.md",
    "CSMV_MEDIA_LINEAGE_AUDIT_20260715.md",
    "LABEL_SPACE_MAPPING_DRAFT.md",
    "DATASET_SELECTION_DECISION.md",
    "LITERATURE_SEARCH_REPORT.md",
    "CONTRIBUTION_PRIOR_ART_MATRIX.md",
    "CARM_NAME_AUDIT.md",
    "RESEARCH_PROTOCOL_FREEZE_AUDIT.md",
    "BASELINE_CANDIDATES.md",
    "DATA_DICTIONARY.md",
    "M2_DATA_PROTOCOL.md",
    "SILVER_LABEL_PROTOCOL.md",
    "LABEL_ERROR_REVIEW_PROTOCOL.md",
    "NEAR_DUPLICATE_SOURCE_AUDIT.md",
    "CUC_CANONICAL_AUDIT.md",
    "configs/silver-label-pipeline-v1.yaml",
    "M2_LEAKAGE_AUDIT.md",
    "DATA_AUDIT_REPORT_V1.md",
    "DATA_CARD_DATASET_V1.md",
    "DATASHEET_DATASET_V1.md",
    "PRIVACY_STATEMENT.md",
    "PLATFORM_TERMS_STATEMENT.md",
    "DATA_RELEASE_BOUNDARY.md",
    "G1_G2_EVIDENCE_MATRIX.md",
    "HANDOFF_10.md",
    "M1_SECOND_PRIMARY_SHORTLIST_20260714.md",
    "M1_LIRIS_ACCEDE_DEEP_AUDIT_20260714.md",
    "HANDOFF_10_SECOND_PRIMARY_READONLY.md",
    "M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md",
    "M1_LAI_GAI_OSF_API_METADATA_AUDIT_20260714.md",
    "TASK00_LAI_GAI_OSF_API_METADATA_REVIEW_20260714.md",
    "TASK00_SECOND_PRIMARY_RESOLUTION_AUTHORIZATION_20260714.md",
    "M1_M2_LAI_GAI_SECOND_PRIMARY_FREEZE_20260714.md",
    "TASK00_LAI_GAI_SECOND_PRIMARY_FREEZE_REVIEW_20260715.md",
    "CSMV_MEDIA_LINEAGE_AUDIT_20260715.md",
    "TASK00_CSMV_LINEAGE_G2_REVIEW_20260715.md",
    "TASK00_CSMV_FEATURE_PREFLIGHT_AUTHORIZATION_20260715.md",
    "data/manifests/canonical-audience-affect-v1.schema.json",
    "data/manifests/csmv-primary-raw-v1.manifest.json",
    "data/manifests/csmv-split-v1.manifest.json",
    "data/manifests/csmv-media-lineage-v1.manifest.json",
    "data/manifests/cuc-auxiliary-raw-v1.manifest.json",
    "data/manifests/cuc-canonical-v1.manifest.json",
    "data/manifests/human-gold-v1.manifest.json",
    "data/manifests/silver-v1.manifest.json",
    "data/manifests/unlabeled-v1.manifest.json",
    "data/manifests/label-provenance-v1.manifest.json",
    "data/manifests/second-primary-label-map-v1.manifest.json",
    "data/manifests/index-boundary-v1.manifest.json",
    "data/manifests/label-error-review-v1.manifest.json",
    "data/manifests/leakage-audit-v1.manifest.json",
    "data/manifests/dataset-v1.manifest.json",
    "data/manifests/split-v1.manifest.json",
    "data/manifests/reproducibility-v1.manifest.json",
    "references/search/step19-23/search-protocol.json",
    "data/manifests/csmv-source-v1.manifest.json",
    "data/manifests/inews-source-v1.manifest.json",
    "data/manifests/nemo-source-v1.manifest.json",
    "data/manifests/m1-public-audit-v1.manifest.json",
    "data/manifests/second-primary-readonly-audit-v1.manifest.json",
    "data/manifests/lai-gai-osf-metadata-audit-v1.manifest.json",
    "data/manifests/lai-gai-osf-api-metadata-v1.manifest.json",
    "data/manifests/lai-gai-second-primary-raw-v1.manifest.json",
    "data/manifests/lai-gai-label-provenance-v1.manifest.json",
    "data/manifests/lai-gai-split-v1.manifest.json",
    "data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json",
]
TEXT_SUFFIXES = {".py", ".md", ".txt", ".yaml", ".yml", ".json", ".toml"}
SKIP_PARTS = {".git", ".venv", "data", "models", "saved_models", "installers", "__pycache__"}
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "generic_assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"']([^\"'\s]{12,})[\"']"
    ),
}


def secret_hits():
    hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".env", ".env.example"}:
            continue
        for line_number, line in enumerate(path.read_text("utf-8", errors="ignore").splitlines(), 1):
            for kind, pattern in SECRET_PATTERNS.items():
                match = pattern.search(line)
                if not match or "os.getenv" in line or "environ.get" in line or "${" in line:
                    continue
                fingerprint = hashlib.sha256(match.group(0).encode()).hexdigest()[:12]
                hits.append(
                    {
                        "file": str(path.relative_to(ROOT)),
                        "line": line_number,
                        "type": kind,
                        "fingerprint": fingerprint,
                    }
                )
    return hits


def main() -> int:
    checks = {}
    checks["required_files"] = {
        "passed": all((ROOT / path).is_file() for path in REQUIRED_FILES),
        "missing": [path for path in REQUIRED_FILES if not (ROOT / path).is_file()],
    }

    with (ROOT / "configs" / "experiment.bootstrap.yaml").open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    try:
        validate(config, ROOT)
        config_error = None
    except Exception as error:  # report exact local validation failure
        config_error = str(error)
    checks["experiment_config"] = {"passed": config_error is None, "error": config_error}
    checks["work_log"] = validate_work_log()
    checks["protocol_freeze"] = validate_protocol_freeze()
    checks["m1_public_audit"] = validate_m1_public_audit()
    checks["csmv_media_lineage"] = validate_csmv_media_lineage()
    checks["csmv_feature_preflight"] = validate_csmv_feature_preflight()
    checks["csmv_i3d_sequence_protocol"] = validate_csmv_i3d_sequence_protocol()
    checks["literature_freeze"] = validate_literature_freeze()
    checks["m2_data_engineering"] = validate_m2_data_engineering()
    checks["m2_release"] = validate_m2_release()
    checks["second_primary_readonly_audit"] = validate_second_primary_readonly_audit()
    checks["lai_gai_osf_metadata_audit"] = validate_lai_gai_osf_metadata_audit()
    legacy_osf_api = validate_lai_gai_osf_api_metadata()
    checks["lai_gai_osf_api_metadata_historical"] = {
        "passed": True,
        "classification": "HISTORICAL_NONCONFORMING_NO_GATE_CREDIT",
        "historical_validator_passed": legacy_osf_api["passed"],
        "superseded_for_current_gate_by": "REVIEW-00-LAI-GAI-FREEZE-20260715",
        "original_result": legacy_osf_api,
    }
    checks["lai_gai_second_primary"] = validate_lai_gai_second_primary()

    imports = {
        name: importlib.util.find_spec(name) is not None
        for name in ["torch", "catboost", "transformers", "sklearn", "MMSA"]
    }
    checks["historical_environment"] = {"passed": all(imports.values()), "imports": imports}
    checks["formal_carm_environment"] = {
        "passed": importlib.util.find_spec("faiss") is not None,
        "faiss_available": importlib.util.find_spec("faiss") is not None,
        "classification": "BLOCKED_M1" if importlib.util.find_spec("faiss") is None else "READY_FOR_REVIEW",
    }

    ignored = {}
    for sample in IGNORED_SAMPLES:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", sample],
            cwd=str(ROOT),
            check=False,
        )
        ignored[sample] = result.returncode == 0
    checks["git_ignore"] = {"passed": all(ignored.values()), "samples": ignored}

    tracked = {}
    for sample in TRACKED_SAMPLES:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", sample],
            cwd=str(ROOT),
            check=False,
        )
        tracked[sample] = result.returncode != 0
    checks["git_trackable_policy_files"] = {
        "passed": all(tracked.values()),
        "samples": tracked,
    }

    hits = secret_hits()
    checks["secret_scan"] = {"passed": not hits, "hits": hits}

    placeholders = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text("utf-8", errors="ignore")
        for token in ["{{", "TODO_TEMPLATE", "[待填写]", "REPLACE_BEFORE_RUN"]:
            if token in text:
                placeholders.append({"file": relative, "token": token})
    checks["template_residuals"] = {"passed": not placeholders, "hits": placeholders}

    blocking = [
        name
        for name, result in checks.items()
        if name != "formal_carm_environment" and not result["passed"]
    ]
    report = {
        "schema": "mmsa.preparation-check.v1",
        "python": sys.version.split()[0],
        "checks": checks,
        "m1_read_only_work_ready": not blocking,
        "formal_model_work_ready": not blocking and checks["formal_carm_environment"]["passed"],
        "blocking_checks": blocking,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["m1_read_only_work_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
