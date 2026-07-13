import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.decomposition import PCA
from sklearn.metrics import precision_score, recall_score
from sklearn.preprocessing import StandardScaler


DATA_PATH = Path(r"D:\MMSA-CH-SIMS\data\SIMS\Processed\unaligned_39.pkl")
OUTPUT_DIR = Path(r"D:\MMSA-CH-SIMS\results\catboost_adapted")
MODEL_DIR = Path(r"D:\MMSA-CH-SIMS\saved_models\catboost_adapted")
SEEDS = [1111, 1112, 1113]


def load_data():
    with DATA_PATH.open("rb") as f:
        return pickle.load(f)


def _masked_mean_std(array, lengths):
    lengths = np.asarray(lengths, dtype=np.int64)
    means = []
    stds = []
    for idx, length in enumerate(lengths):
        valid = array[idx, :length]
        means.append(valid.mean(axis=0))
        stds.append(valid.std(axis=0))
    return np.concatenate([np.asarray(means), np.asarray(stds)], axis=1)


def build_split_features(split):
    text_stats = np.concatenate(
        [split["text"].mean(axis=1), split["text"].std(axis=1)],
        axis=1,
    )
    audio_stats = _masked_mean_std(split["audio"], split["audio_lengths"])
    vision_stats = _masked_mean_std(split["vision"], split["vision_lengths"])
    return {
        "text": text_stats.astype(np.float32),
        "audio": audio_stats.astype(np.float32),
        "vision": vision_stats.astype(np.float32),
        "label": split["regression_labels"].astype(np.float32),
        "id": split["id"],
    }


def fit_pca(train_x, valid_x, test_x, n_components=16):
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_x)
    valid_scaled = scaler.transform(valid_x)
    test_scaled = scaler.transform(test_x)
    pca = PCA(n_components=n_components, random_state=0)
    return (
        pca.fit_transform(train_scaled),
        pca.transform(valid_scaled),
        pca.transform(test_scaled),
        scaler,
        pca,
    )


def multiclass_acc(y_pred, y_true):
    return float(np.sum(np.round(y_pred) == np.round(y_true)) / len(y_true))


def sims_metrics(y_pred, y_true):
    y_pred = np.asarray(y_pred, dtype=np.float32).reshape(-1)
    y_true = np.asarray(y_true, dtype=np.float32).reshape(-1)
    y_pred = np.clip(y_pred, -1.0, 1.0)
    y_true = np.clip(y_true, -1.0, 1.0)

    def bucketize(values, bins):
        out = values.copy()
        for i in range(len(bins) - 1):
            mask = np.logical_and(values > bins[i], values <= bins[i + 1])
            out[mask] = i
        return out

    pred_a2 = bucketize(y_pred, [-1.01, 0.0, 1.01])
    true_a2 = bucketize(y_true, [-1.01, 0.0, 1.01])
    pred_a3 = bucketize(y_pred, [-1.01, -0.1, 0.1, 1.01])
    true_a3 = bucketize(y_true, [-1.01, -0.1, 0.1, 1.01])
    pred_a5 = bucketize(y_pred, [-1.01, -0.7, -0.1, 0.1, 0.7, 1.01])
    true_a5 = bucketize(y_true, [-1.01, -0.7, -0.1, 0.1, 0.7, 1.01])

    mae = float(np.mean(np.abs(y_pred - y_true)))
    corr = float(np.corrcoef(y_pred, y_true)[0][1])
    weighted_precision = float(precision_score(true_a2, pred_a2, average="weighted", zero_division=0))
    weighted_recall = float(recall_score(true_a2, pred_a2, average="weighted", zero_division=0))

    classes = np.unique(np.concatenate([true_a2, pred_a2]))
    f1_parts = []
    weights = []
    for cls in classes:
        tp = np.sum((pred_a2 == cls) & (true_a2 == cls))
        fp = np.sum((pred_a2 == cls) & (true_a2 != cls))
        fn = np.sum((pred_a2 != cls) & (true_a2 == cls))
        cls_precision = tp / (tp + fp) if (tp + fp) else 0.0
        cls_recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * cls_precision * cls_recall / (cls_precision + cls_recall) if (cls_precision + cls_recall) else 0.0
        support = np.sum(true_a2 == cls)
        f1_parts.append(f1 * support)
        weights.append(support)
    weighted_f1 = float(sum(f1_parts) / sum(weights))

    return {
        "Mult_acc_2": round(multiclass_acc(pred_a2, true_a2), 4),
        "Precision": round(weighted_precision, 4),
        "Recall": round(weighted_recall, 4),
        "Mult_acc_3": round(multiclass_acc(pred_a3, true_a3), 4),
        "Mult_acc_5": round(multiclass_acc(pred_a5, true_a5), 4),
        "F1_score": round(weighted_f1, 4),
        "MAE": round(mae, 4),
        "Corr": round(corr, 4),
    }


def prepare_features(dataset):
    train = build_split_features(dataset["train"])
    valid = build_split_features(dataset["valid"])
    test = build_split_features(dataset["test"])

    packed = {}
    transforms = {}
    for modality in ["text", "audio", "vision"]:
        train_x, valid_x, test_x, scaler, pca = fit_pca(
            train[modality], valid[modality], test[modality], n_components=16
        )
        packed[modality] = {
            "train": train_x.astype(np.float32),
            "valid": valid_x.astype(np.float32),
            "test": test_x.astype(np.float32),
        }
        transforms[modality] = {
            "explained_variance_ratio_sum": float(pca.explained_variance_ratio_.sum()),
            "input_dim": int(train[modality].shape[1]),
            "output_dim": 16,
        }

    features = {
        split: np.concatenate(
            [packed["text"][split], packed["audio"][split], packed["vision"][split]],
            axis=1,
        )
        for split in ["train", "valid", "test"]
    }
    labels = {split: part["label"] for split, part in [("train", train), ("valid", valid), ("test", test)]}
    ids = {split: part["id"] for split, part in [("train", train), ("valid", valid), ("test", test)]}
    return features, labels, ids, transforms


def train_once(seed, features, labels):
    model = CatBoostRegressor(
        iterations=2000,
        depth=6,
        learning_rate=0.03,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=seed,
        allow_writing_files=False,
        verbose=False,
    )
    model.fit(
        features["train"],
        labels["train"],
        eval_set=(features["valid"], labels["valid"]),
        use_best_model=True,
        early_stopping_rounds=200,
    )
    preds = {
        split: model.predict(features[split]).reshape(-1)
        for split in ["train", "valid", "test"]
    }
    metrics = {split: sims_metrics(preds[split], labels[split]) for split in preds}
    return model, preds, metrics


def summarize_runs(rows):
    df = pd.DataFrame(rows)
    metric_cols = ["Mult_acc_2", "Precision", "Recall", "Mult_acc_3", "Mult_acc_5", "F1_score", "MAE", "Corr"]
    summary = {}
    for col in metric_cols:
        summary[col] = {
            "mean": round(float(df[col].mean()), 4),
            "std": round(float(df[col].std(ddof=0)), 4),
        }
    return summary


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_data()
    features, labels, ids, transforms = prepare_features(dataset)

    run_rows = []
    detailed = []
    for seed in SEEDS:
        model, preds, metrics = train_once(seed, features, labels)
        model_path = MODEL_DIR / f"catboost_sims_seed{seed}.cbm"
        model.save_model(model_path)
        row = {"seed": seed, **metrics["test"]}
        run_rows.append(row)
        detailed.append(
            {
                "seed": seed,
                "best_iteration": int(model.get_best_iteration()),
                "model_path": str(model_path),
                "train_metrics": metrics["train"],
                "valid_metrics": metrics["valid"],
                "test_metrics": metrics["test"],
                "test_preview": [
                    {
                        "id": str(ids["test"][i]),
                        "y_true": round(float(labels["test"][i]), 4),
                        "y_pred": round(float(np.clip(preds["test"][i], -1.0, 1.0)), 4),
                    }
                    for i in range(min(10, len(ids["test"])))
                ],
            }
        )

    runs_df = pd.DataFrame(run_rows)
    runs_df.to_csv(OUTPUT_DIR / "catboost_sims_runs.csv", index=False, encoding="utf-8-sig")

    report = {
        "experiment_name": "catboost_adapted_on_ch_sims",
        "note": (
            "This is an adapted benchmark experiment, not a direct replay of the thesis M-DRGE feature pipeline. "
            "CH-SIMS does not provide the thesis paper's original 48 propagation/retrieval features, so we pooled "
            "official text/audio/vision sequences, reduced each modality to 16 PCA components on the train split, "
            "concatenated them into 48 dimensions, and trained CatBoostRegressor under the official train/valid/test split."
        ),
        "dataset": {
            "path": str(DATA_PATH),
            "train_size": int(len(labels["train"])),
            "valid_size": int(len(labels["valid"])),
            "test_size": int(len(labels["test"])),
        },
        "feature_protocol": transforms,
        "seeds": SEEDS,
        "test_runs": detailed,
        "test_summary": summarize_runs(run_rows),
    }
    (OUTPUT_DIR / "catboost_sims_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report["test_summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
