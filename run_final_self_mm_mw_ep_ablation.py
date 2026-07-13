from pathlib import Path

from MMSA import MMSA_run


ROOT = Path(__file__).resolve().parent
SEEDS = [1111, 1112, 1113]


def config(use_mw=False, use_ep=False):
    return {
        "featurePath": str(ROOT / "data" / "SIMS" / "Processed" / "unaligned_39.pkl"),
        "pretrained": str(ROOT / "models" / "bert-base-chinese"),
        "use_modality_weighting": use_mw,
        "use_emotion_prototypes": use_ep,
        "gate_hidden_dim": 128,
        "gate_dropout": 0.1,
        "gate_temperature": 1.5 if use_mw else 1.0,
        "gate_regularization_weight": 0.05 if use_mw else 0.0,
        "gate_entropy_floor": 0.8,
        "prototype_loss_weight": 0.2 if use_ep else 0.0,
        "prototype_residual_weight": 0.15 if use_ep else 0.0,
        "prototype_temperature": 0.5 if use_ep else 1.0,
        "num_emotion_prototypes": 5,
        "use_multi_emotion_prototypes": use_ep,
    }


for name, use_mw, use_ep in [
    ("self_mm", False, False),
    ("self_mm_mw", True, False),
    ("self_mm_ep", False, True),
    ("self_mm_mw_ep", True, True),
]:
    exp_root = ROOT / "experiments" / "final_classic_metrics" / name
    MMSA_run(
        model_name="self_mm",
        dataset_name="sims",
        config=config(use_mw, use_ep),
        seeds=SEEDS,
        gpu_ids=[0],
        num_workers=0,
        verbose_level=1,
        model_save_dir=exp_root / "saved_models",
        res_save_dir=exp_root / "results",
        log_dir=exp_root / "logs",
    )
