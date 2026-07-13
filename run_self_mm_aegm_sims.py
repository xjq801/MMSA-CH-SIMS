import argparse
from pathlib import Path

from MMSA import MMSA_run


ROOT = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(description="Run Self-MM with adaptive gating and emotion prototypes on CH-SIMS.")
    parser.add_argument("--seeds", nargs="+", type=int, default=[1111, 1112, 1113])
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument(
        "--variant",
        choices=["gate", "prototype", "both", "refined_gate", "refined_prototype", "refined", "residual", "balanced_aux", "reliability", "subprototype", "cross_attention"],
        default="both",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    use_gate = args.variant in {"gate", "both", "refined_gate", "refined", "residual", "balanced_aux", "reliability", "subprototype", "cross_attention"}
    use_prototype = args.variant in {"prototype", "both", "refined_prototype", "refined", "residual", "balanced_aux", "reliability", "subprototype", "cross_attention"}
    refined_gate = args.variant in {"refined_gate", "refined", "residual", "balanced_aux", "reliability", "subprototype", "cross_attention"}
    refined_prototype = args.variant in {"refined_prototype", "refined", "residual", "balanced_aux", "reliability", "subprototype", "cross_attention"}
    exp_name = {
        "gate": "self_mm_gate",
        "prototype": "self_mm_prototype",
        "both": "self_mm_aegm",
        "refined_gate": "self_mm_refined_gate",
        "refined_prototype": "self_mm_refined_prototype",
        "refined": "self_mm_refined",
        "residual": "self_mm_residual",
        "balanced_aux": "self_mm_balanced_aux",
        "reliability": "self_mm_reliability",
        "subprototype": "self_mm_subprototype",
        "cross_attention": "self_mm_cross_attention",
    }[args.variant]
    exp_root = ROOT / "experiments" / exp_name
    MMSA_run(
        model_name="self_mm",
        dataset_name="sims",
        config={
            "featurePath": str(ROOT / "data" / "SIMS" / "Processed" / "unaligned_39.pkl"),
            "pretrained": str(ROOT / "models" / "bert-base-chinese"),
            "use_modality_weighting": use_gate,
            "use_emotion_prototypes": use_prototype,
            "gate_hidden_dim": 128,
            "gate_dropout": 0.1,
            "gate_temperature": 1.5 if refined_gate else 1.0,
            "gate_regularization_weight": 0.05 if refined_gate else 0.0,
            "gate_entropy_floor": 0.8,
            "use_residual_gate": args.variant == "residual",
            "residual_gate_alpha": 0.5,
            "use_aux_5class": args.variant == "balanced_aux",
            "aux_5class_loss_weight": 0.1 if args.variant == "balanced_aux" else 0.0,
            "use_modality_reliability": args.variant == "reliability",
            "reliability_strength": 1.0,
            "use_cross_modal_attention": args.variant == "cross_attention",
            "interaction_dim": 64,
            "interaction_heads": 4,
            "interaction_dropout": 0.1,
            "interaction_alpha": 0.1,
            "prototype_loss_weight": 0.2 if use_prototype else 0.0,
            "prototype_residual_weight": 0.15 if use_prototype else 0.0,
            "prototype_temperature": 0.5 if refined_prototype else 1.0,
            "num_emotion_prototypes": 5,
            "num_subprototypes": 2 if args.variant == "subprototype" else 1,
            "prototype_diversity_loss_weight": 0.01 if args.variant == "subprototype" else 0.0,
            "use_multi_emotion_prototypes": refined_prototype,
        },
        seeds=args.seeds,
        gpu_ids=[args.gpu],
        num_workers=0,
        verbose_level=1,
        model_save_dir=exp_root / "saved_models",
        res_save_dir=exp_root / "results",
        log_dir=exp_root / "logs",
    )
