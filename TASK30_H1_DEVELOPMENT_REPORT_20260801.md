# Task30 H1 development report

> Evidence identity: `DEVELOPMENT_EVIDENCE_ONLY_H1_GATE_NOT_PASSED`  
> Decision branch: `NOT_PASSED_MECHANISM_NOT_STABLE`  
> Task timepoint: `T0`  
> Formal test: `TEST_ROWS_NOT_MATERIALIZED_OR_USED`  
> Task40: `BLOCKED_NOT_AUTHORIZED`

## 1. Question and evidence boundary

Task30 asks whether train-response privileged supervision improves a student that reads only admissible T0 content at training and inference. Teacher/student and KD are implementation mechanisms, not the contribution. This report contains development evidence only; it is not the Task50 five-seed formal test result and cannot support a paper performance claim.

G1 remains `PASS`, G2 protocol/data `PASS_WITH_LIMITATIONS`, asset admissibility `DEFERRED_ACCEPTED_RISK`, and G3 `PASS_WITH_LIMITATIONS`. I3D licence, official revision, rightsholder package identity and fixity remain unknown. No restricted array, response text, private prediction row, model weight, credential or local absolute path is committed or redistributed.

## 2. Input and leakage audit

- CSMV formal split remained `group_by_video_v1`: 5,698 train / 837 dev / 1,675 test.
- The teacher adapter used only the 5,698 formal-train videos and aggregated 74,727 mapped reactions. Class counts were anger 1,130; anticipation 11,798; disgust 6,252; fear 1,543; joy 23,893; sadness 4,045; surprise 5,989; trust 20,076.
- One missing emotion label and five missing opinion labels were retained in the audit and excluded only from their respective field denominators. Unknown labels, missing required fields, video mismatch, count mismatch, non-finite values, or all-missing fields fail closed.
- Dev/test response text was never emitted or supplied to a teacher. Student batches contain only pooled frozen I3D content features and label-side training targets. Formal test rows were not materialized or used for model, temperature, lambda, threshold, calibration, early stopping, or selection.
- Task20 metrics were imported unchanged. No Task20 frozen evaluation-core file was modified.

## 3. Implemented comparison

The CSMV student is a minimal pooled-I3D content MLP. Each deployable row received the same 12-trial architecture and optimization budget: hidden dimension 128/256/512, dropout 0.1/0.3, learning rate 0.0003/0.001, maximum 200 epochs, patience 20, batch size 64, dev selection by JSD then NLL, Brier, parameter count and trial order.

Rows: hard label; soft distribution; ordinary content-only KD; train-comment-privileged KD; deterministic mismatched-comment teacher; and a soft-distribution Dirichlet head. Temperature candidates were 1/2/4 and KD weights 0.25/0.5/0.75. The teacher-only result is a non-deployable **train diagnostic**, because dev/test responses are unreachable; it is not a comparable dev upper bound.

No memory, retrieval, router, GNN, generation, remote service, paid LLM, object store or model-weight export was introduced.

## 4. Primary CSMV development result

The complete seed-20260802 search ran 72 student trials on 837 dev items. Selected metrics were:

| Row | JSD ↓ | NLL ↓ | Brier ↓ | ECE ↓ | ACE ↓ |
|---|---:|---:|---:|---:|---:|
| hard label | 0.180825 | 1.790076 | 0.239266 | 0.041093 | 0.045672 |
| soft distribution | 0.172843 | **1.703714** | 0.218402 | 0.048944 | 0.061966 |
| ordinary KD | 0.171793 | 1.712183 | 0.219297 | 0.041235 | 0.060414 |
| comment-privileged KD | **0.169667** | 1.723492 | 0.220087 | **0.028594** | **0.052400** |
| mismatched-comment control | 0.171766 | 1.714517 | 0.218371 | 0.044501 | 0.064686 |
| soft Dirichlet | 0.172688 | 1.706831 | **0.213503** | 0.072300 | 0.067911 |

Privileged KD improves the primary JSD in this seed, including versus ordinary KD and mismatch, and does not degrade ECE/ACE. However NLL and Brier are worse than the soft baseline. Dirichlet gives only a 0.000155 JSD improvement over softmax while materially worsening ECE/ACE, so it is not a clear replacement.

The privileged teacher train diagnostic reached JSD 0.014677 but ECE 0.347062. Because it consumes train-only privileged inputs and is evaluated on train, it is neither deployable nor comparable to dev students.

## 5. Stability and mechanism controls

The selected configurations were frozen from seed 20260802. A same-seed replay produced byte-identical private predictions. Two additional development seeds then ran only those frozen configurations; they did not repeat selection.

| Seed | privileged JSD | gain vs soft | gain vs ordinary KD | gain vs mismatch | NLL delta vs soft |
|---|---:|---:|---:|---:|---:|
| 20260802 | 0.169667 | +0.003176 | +0.002126 | +0.002100 | +0.019778 |
| 20260803 | 0.169030 | +0.003141 | +0.001716 | +0.001741 | +0.012115 |
| 20260804 | 0.170083 | +0.002883 | −0.000003 | −0.000304 | +0.022081 |
| mean | — | +0.003067 | +0.001280 | +0.001179 | +0.017991 |

Positive “gain” means lower JSD. Privileged KD beats the plain soft student in 3/3 seeds, but its specific advantage over ordinary KD and the mismatched-comment negative control holds in only 2/3 seeds. NLL is worse in 3/3 seeds. Therefore the development evidence does not isolate a stable comment-privileged mechanism.

## 6. Response-count, disagreement and label-noise analysis

Against the soft student, privileged-KD JSD gain is positive in all three seeds for low-comment (1–2), medium (3–10), and high (11+) groups, with the largest gain in the small low-comment group (n=15). This finding is descriptive and unstable in precision because that group is small.

The stronger mechanism diagnostic is adverse:

- high normalized target entropy (n=178): privileged KD is worse in 3/3 seeds, with mean per-item JSD changes of −0.00858, −0.00945 and −0.00679;
- upper-third binomial-standard-error noise proxy (n=279): worse in 3/3 seeds, −0.00371, −0.00548 and −0.00158;
- low-entropy and mixed groups: better in 3/3 seeds.

Thus the apparent benefit concentrates in less ambiguous targets and does not explain high-disagreement reactions. Sarcasm is `NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE`; no dev response text was opened to create qualitative anecdotes.

## 7. Dataset and head applicability

- **CSMV:** H1 applicable with train responses only; results above are development-only.
- **LAI-GAI:** H1 fixed `NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE`. A real T0 image-content boundary used SHA-verified images and a fixed 12-dimensional RGB-statistics feature. On 594 train / 127 dev, content-softmax JSD was 0.054140, Dirichlet 0.054456, and train overall-mean 0.074507. ECE remained high (0.232821/0.253942), so this is only a content/calibration boundary.
- **Video2Reaction native:** H1 fixed `NOT_APPLICABLE_DATA_NOT_RELEASED`; no comment teacher was fabricated.

## 8. Reproducibility and private run identities

All generated runs are Git-ignored and redistribution-prohibited. Only aggregate identities and hashes are recorded here.

| Artifact ID | SHA-256 |
|---|---|
| full CSMV dev manifest | `330c9de88918a9cea5293ebf7c721d9f3c6738a9e7142c3a8fdff18cb86e3fa7` |
| full CSMV aggregate | `17f23df0b6d883fc01b7c6e35b2dd06930adad1d761064f13ac750c8f21a3e4d` |
| private CSMV predictions | `195e60290d867ca2ce75be75830bffb4bd808228f0786b9f65deb019e5ade53a` |
| same-seed replay manifest | `7c37a51234051bb02bcb51fb18d3bf6b17b098e1bf5e1021870c8fe6e0c141b1` |
| seed-20260803 manifest | `8d241df7dc1a04e04111de140f077d9c934a0a3434ecd80fc35c8f9c7a57e56d` |
| seed-20260804 manifest | `c0c97dfe760e2a089c8235591e9af123f60d31031268a24336e62176ebed1e8b` |
| LAI-GAI boundary aggregate | `a972278f1b2101bc1a776d4cf9ae5049c25326a556290e487532c46fc8ed97a6` |

Every declared manifest artifact hash revalidated. The full run contains 72 raw trial rows and 837 private prediction rows; stderr is empty. Same-seed predictions are byte-identical. No model weights were saved. Local RTX 3070 Ti execution used below 2.2 GiB observed GPU memory; rented compute was unnecessary.

## 9. H1 development-gate decision

Decision: `NOT_PASSED_MECHANISM_NOT_STABLE`.

The result is not `H1_SUCCESS`: improvement over soft supervision is stable, but improvement specifically attributable to correct train-comment privileged information is not stable against ordinary KD and mismatch, and high-disagreement/high-noise groups degrade. It is also not a formal `H1_REJECTED` conclusion because formal test, Task50 five-seed inference, and a second comment-bearing public dataset are absent.

Task30 therefore freezes teacher/student-v1 as development code and private run evidence, but does **not** authorize Task40. Any future retry requires a new 00 decision and a predeclared mechanism change within H1 scope; it cannot tune on test or reinterpret this result after seeing test.
