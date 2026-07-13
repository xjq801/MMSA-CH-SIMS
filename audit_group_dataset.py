import csv
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np


def video_id(value):
    match = re.search(r"BV[0-9A-Za-z]+", value or "")
    return match.group(0) if match else ""


root = Path(sys.argv[1]).resolve()
topics = sorted(path for path in root.iterdir() if path.is_dir())
publishers = sorted(path for topic in topics for path in topic.iterdir() if path.is_dir())

labels = []
emotions = []
labeled_ids = []
topic_counts = Counter()
publisher_counts = Counter()
timestamps = {}
vector_ids = []
file_counts = Counter()
label_sources = Counter()
threshold_mismatches = 0
training_audit = Counter()

for publisher in publishers:
    label_path = publisher / "3.视频群体情绪值对应.csv"
    video_path = publisher / "6.发布者视频列表.csv"
    vector_path = publisher / "5.预测向量.csv"

    local_labels = {}
    local_timestamps = {}
    if label_path.exists():
        file_counts["label"] += 1
        with label_path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                try:
                    emotion = float(row["群体情绪"])
                except (KeyError, TypeError, ValueError):
                    continue
                derived_label = int(emotion > 0.5217 or emotion < -0.2558)
                try:
                    label = int(float(row["极端情绪分类"]))
                    label_sources["explicit"] += 1
                    threshold_mismatches += label != derived_label
                except (KeyError, TypeError, ValueError):
                    label = derived_label
                    label_sources["derived"] += 1
                labels.append(label)
                emotions.append(emotion)
                identifier = video_id(row.get("视频地址", "") or row.get("urls", ""))
                labeled_ids.append(identifier)
                if identifier:
                    local_labels.setdefault(identifier, []).append((emotion, label))
                topic_counts[publisher.parent.name] += 1
                publisher_counts[str(publisher.relative_to(root))] += 1

    if video_path.exists():
        file_counts["video"] += 1
        with video_path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter=";"):
                identifier = video_id(row.get("视频地址", ""))
                if identifier and row.get("发布时间"):
                    timestamps[identifier] = row["发布时间"]
                    local_timestamps[identifier] = row["发布时间"]

    if vector_path.exists():
        file_counts["vector"] += 1
        with vector_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=";")
            next(reader, None)
            for row in reader:
                if len(row) < 49:
                    training_audit["short_vector_row"] += 1
                    continue
                try:
                    vector_label = int(float(row[48]))
                except ValueError:
                    training_audit["invalid_vector_label"] += 1
                    continue
                training_audit["valid_vector_row"] += 1
                identifier = video_id(row[49]) if len(row) > 49 else ""
                vector_ids.append(identifier)
                if not identifier:
                    training_audit["missing_vector_id"] += 1
                    continue
                if identifier in local_labels:
                    training_audit["local_label_match"] += 1
                    if any(label == vector_label for _, label in local_labels[identifier]):
                        training_audit["vector_label_agreement"] += 1
                else:
                    training_audit["missing_local_label"] += 1
                if identifier in local_timestamps:
                    training_audit["local_timestamp_match"] += 1

labels = np.asarray(labels)
emotions = np.asarray(emotions)
labeled_nonempty = [item for item in labeled_ids if item]
vector_nonempty = [item for item in vector_ids if item]
labeled_set = set(labeled_nonempty)
vector_set = set(vector_nonempty)

print("root:", root)
print("topics:", len(topics), [item.name for item in topics])
print("publisher folders:", len(publishers))
print("files:", dict(file_counts))
print("labeled videos:", len(labels))
print("labels:", dict(sorted(Counter(labels.tolist()).items())))
print("label sources:", dict(label_sources), "threshold mismatches:", threshold_mismatches)
print("emotion range/mean/std:", float(emotions.min()), float(emotions.max()), float(emotions.mean()), float(emotions.std()))
print("emotion quantiles:", dict(zip([0, .1, .25, .5, .75, .9, 1], np.quantile(emotions, [0, .1, .25, .5, .75, .9, 1]).round(6))))
print("missing label BV ids:", len(labeled_ids) - len(labeled_nonempty))
print("duplicate labeled BV rows:", len(labeled_nonempty) - len(labeled_set))
print("timestamp matches:", sum(item in timestamps for item in labeled_nonempty), "/", len(labeled_nonempty))
print("vector rows/unique ids:", len(vector_nonempty), len(vector_set))
print("label-vector matches:", len(labeled_set & vector_set), "/", len(labeled_set))
print("global vector timestamp matches:", len(vector_set & set(timestamps)), "/", len(vector_set))
print("training-vector audit:", dict(training_audit))
print("samples by topic:", dict(sorted(topic_counts.items())))
print("publishers with labels:", len(publisher_counts), "min/max samples:", min(publisher_counts.values()), max(publisher_counts.values()))
