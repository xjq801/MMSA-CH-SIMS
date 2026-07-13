from pathlib import Path

from MMSA import MMSA_run


ROOT = Path(__file__).resolve().parent


if __name__ == "__main__":
    MMSA_run(
        model_name="self_mm",
        dataset_name="sims",
        config={
            "featurePath": str(ROOT / "data" / "SIMS" / "Processed" / "unaligned_39.pkl"),
            "pretrained": str(ROOT / "models" / "bert-base-chinese"),
        },
        seeds=[1111, 1112, 1113],
        gpu_ids=[0],
        num_workers=0,
        verbose_level=1,
        model_save_dir=ROOT / "saved_models",
        res_save_dir=ROOT / "results",
        log_dir=ROOT / "logs",
    )
