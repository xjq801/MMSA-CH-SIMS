# Task30 H1 delta audit and TDD plan

> Status: `READY_FOR_TDD_WITH_LOCAL_INPUT_BINDING_LIMITATION`  
> Audit time: 2026-08-01 22:16:53 +08:00  
> Audit-start Git anchor: `32e8967f` (`origin/main`, detached clean worktree)  
> Final Task30 anchor: `7c4b20c83b15c14b4f189fc36b18d7478244dc82` (`CREATED_STARTUP_AUDIT_IN_PROGRESS`)  
> SSOT: `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21, sections 5 and 17 task 30

## 1. Frozen scientific contract

- Task30 tests H1 only: whether train-response privileged supervision improves a student that reads only admissible T0 content at training and inference.
- Task30 produces development evidence only. Formal test reuse, five seeds, paired bootstrap, paper tables and claims remain Task50 work.
- CSMV is the primary H1 development dataset. LAI-GAI supports only the distribution/calibration boundary its released fields actually permit. Native Video2Reaction H1 is `NOT_APPLICABLE_DATA_NOT_RELEASED`.
- Teacher/student and KD are established mechanisms, not the claimed innovation.
- Memory, retrieval, router, GNN and generative modules are out of scope. Task30 cannot create Task40 or approve its own H1 gate.

## 2. Gate and asset state

| Gate or asset | Frozen state | Task30 consequence |
|---|---|---|
| G1 | `PASS` | data-governance foundation accepted |
| G2 protocol/data | `PASS_WITH_LIMITATIONS` | only frozen dataset/split contracts may be used |
| Asset admissibility | `DEFERRED_ACCEPTED_RISK` | existing I3D may be used internally only; no redistribution |
| G3 | `PASS_WITH_LIMITATIONS` | Task30 development may start without changing Task20 evaluation core |
| VC-CSA exploration | `NON_T0/INELIGIBLE` | never a Task30 baseline or evidence source |
| I3D licence/revision/rightsholder package fixity | `UNKNOWN` | stop and report if identity, coverage or hash drifts |

## 3. Hash-bound inputs checked

| Input | SHA-256 |
|---|---|
| master plan v1.21 | `ab9a1b7f619b76ead7dfbcd8a393ab2c8ad7779d0178a390b4dd0512e25b8843` |
| Task30 creation authorization | `9b18b5e3056d6fd6825e739522dfcbf586e134258c7ef5b8ba8c0316747aeab4` |
| Task30 startup handoff | `8cae02156b9ecb60798818486ba18a0a211abb9552999139b8ff8c82a3ee6dd2` |
| Task20 handoff | `5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb` |
| Task20 handoff manifest | `6d75e2190a50dc4a2191458d6d379a7d49a84f630d5ccf3eb27ac83294f96e91` |
| T0 input policy | `287356695d0be3b6cbbd5760ee926e43dde90437abf4bfcd920b3c1276cea1d5` |
| experiment protocol v2 | `53a08ff90608c982c700759683566fb0a52216ebeed33f185b2406373ba4d976` |
| leakage threat model | `88a4896012992c6c74b55f774bfe22227ddec8a12276f477fe85856a7218182c` |
| Task20 tuning plan | `01878e74f6f9c150d583ad591b0b7b5fb662208119076aef51ccb237ab741cf9` |
| Task20 experiment/prediction/run schemas | `31b9665...` / `fadc6ff7...` / `7c14ba2c...` |

`python scripts/validate_task20_handoff.py` returned `passed=true`, `tracked_evidence_checked=22`, and did not require restricted assets.

## 4. Delta from Task20

1. Task20's evaluator, metrics, split, class ordering for CSMV, T0 rule and test policy are frozen and must remain unmodified.
2. Task20 model constructors already accept a dynamic `class_count`; Task30 must preserve that property and add a dataset-head contract instead of hard-coding eight CSMV classes.
3. Task20 schemas are versioned to v1.16 and baseline identities. Task30 needs new v1.21 contracts; copying and silently editing Task20 schemas would blur provenance.
4. The release manifest explicitly says `comment_text_in_release=false`. The current worktree contains manifests and documentation only, not the restricted I3D arrays, processed HUMAN_GOLD records or train-comment material needed for a real H1 run.
5. No `.venv`, `.venv-task20` or `.venv-task30` exists in this worktree. Task30 therefore requires a fresh Python 3.8 environment and its own lock/evidence; Task20 readiness cannot be inherited.
6. Historical target-comment scripts are leakage-positive legacy references. They may not be imported into the student path or treated as H1 evidence.

## 5. Fail-closed data-flow contract

```text
train responses --[split=train only]--> response teacher --[distribution target only]--+
                                                                                  |
T0 content -------------------------> content student -----------------------------+--> dev predictions

dev responses  --X--> teacher fit / KD target cache / early stopping
test responses --X--> all Task30 development code
test labels    --X--> selection, calibration, temperature, threshold or stopping
```

- A teacher batch must carry `dataset_id`, `sample_id`, `split`, `class_order`, response-derived distribution, response count and confidence.
- Teacher fitting and privileged-target construction accept `split=train` only. A dev/test record raises a leakage error before any tensor is returned.
- Student batches expose only declared T0 content tensors, masks and label-side training distributions. Response text, response IDs and future fields are rejected by name and provenance.
- Missing required fields, duplicate sample IDs, class-order mismatch, illegal dataset/head mapping, non-finite values, negative probabilities and rows that do not sum to one all fail closed.

## 6. First TDD batch (must be observed red before implementation)

1. `test_teacher_fit_rejects_dev_comments` and `test_teacher_fit_rejects_test_comments`.
2. `test_student_batch_rejects_response_or_future_fields`.
3. `test_missing_teacher_fields_fail_closed`.
4. `test_distribution_rejects_negative_non_normalized_nan_and_inf` plus a known-valid normalization gold case.
5. `test_mismatched_teacher_is_train_only_deterministic_derangement` and a mismatch provenance check.
6. `test_dataset_head_is_dynamic_and_rejects_wrong_class_order`.
7. `test_lai_gai_disables_comment_teacher` and `test_video2reaction_h1_is_not_applicable_data_not_released`.
8. `test_student_forward_is_content_only_and_returns_finite_normalized_distribution`.
9. Loss gold tests for hard-label, soft-distribution, ordinary KD and comment-privileged KD with explicit temperature and finite-value rejection.
10. Parameter/budget comparison test: matched student architecture and trial budget across hard/soft/ordinary-KD/privileged-KD/mismatch rows; teacher-only is separately marked non-deployable upper bound.

## 7. Minimal implementation boundary

- New Task30 contracts, models, loss functions, configuration schema and tests only.
- Reuse Task20 metrics/evaluation by import after compatibility tests; do not edit their implementation.
- Use synthetic fixtures solely for deterministic unit/smoke tests. Such outputs are `TEST_EVIDENCE_ONLY`, never H1 development evidence.
- A real CSMV development run starts only after an authorized local input binding supplies frozen train/dev I3D plus train-only response-derived teacher records and passes hash/split checks. Formal test remains unreachable.
