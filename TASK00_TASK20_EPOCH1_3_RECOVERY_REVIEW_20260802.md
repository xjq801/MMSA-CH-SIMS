# Task00 independent review — Task20 VC-CSA Epoch 1–3 recovery Attempt2

> Review version: v1.0  
> Review object: `main@da9c52a3747035851eb03185285b580f8d7f0f47`  
> Attempt: `TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_SEED3407_ATTEMPT2`  
> Decision: `SUPPLEMENT_REQUIRED_NO_ACCEPTANCE_YET`  
> Evidence identity remains: `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`  
> Formal evidence eligibility remains: `INELIGIBLE`

## 1. Controller conclusion

Task00 finds the submitted execution and disconnected display materially coherent with the authorized independent-attempt boundary. The reviewed materials do not show an attempt to overwrite the historical Epoch 1–3 gap, join Epoch 3 to Epoch 4, access test, modify the paper, or promote this run into T0/G3/Task30/50 evidence.

Acceptance is nevertheless deferred. The submission contains two correctable record-schema defects, one irrecoverable-but-disclosable evidence gap, and an incomplete non-secret index for evidence that remains private. These issues do **not** authorize a rerun and do **not** invalidate the already-produced private payloads. Task20 must issue an append-only correction and hash-only supplement; it must not invent timestamps, overwrite history, reopen the experiment, or expose restricted content.

## 2. Independently verified evidence

1. Git binding: review object, local `HEAD`, and `origin/main` were all `da9c52a3747035851eb03185285b580f8d7f0f47` at review start; tracked files were clean. User-owned untracked `NEmoP/`, `__MACOSX/`, and `tmp/` were not read or modified.
2. Submitted hashes independently matched:
   - completion: `e003cfa59e3e4d356cc8517f98a4f01f7600440b50e1988db784ad9ffab2adae`;
   - non-secret artifact ledger: `ccda5a7e8118cab8420f08692285c6a39a13b7b8784fdfae38d0d036c04029e1`;
   - run manifest: `9c029559f101edee158bab702ac8fd0dedf794f20a8b2feade1c32c0272b96a9`;
   - metrics summary: `444d55ec62c95b927d9acc29cbf66811378aa6cf34080cb896197cd1f217db30`;
   - disconnected CSV/PNG/SVG: `e98f0fa5877ea6ddb6b278e81d06d920802e6bd666ff8085f48d7e253475176f`, `fad4b68656141ce416e04324db74aca5c6633cc317bda24e8220b66a50680fcc`, and `38f9616ca1961c7ccbd1be545955ae6e78a18d8699e9e7f04fb11566a20ca5a7`.
3. All 16 entries in `nonsecret-artifact-hashes.json` matched independent SHA-256 recomputation. The stated six-file code-bundle digest independently recomputed to `d189175655803bd2274731490b956fd5bfaf6fbca6321f26eea2f6e67f6c4c5b` under the documented path/NUL/hash/newline scheme.
4. The corrected private final-bundle `SHA256SUMS` root is `ff070dd3f92b78cd1e5a4d7b85d9ed16fd3d273fb30e26f7a92694bba82f524b`. It is consistent across the committed completion, run manifest, and WORK_LOG. The different string in Task20's first chat handoff was a message-transcription error and appears nowhere in the reviewed repository.
5. The versioned configuration freezes seed 3407, fresh initialization, `max_epoch=120`, stop after completed Epoch 3, and `test_access=0`. The patch rejects the stop guard when either a resume checkpoint or fine-tuning checkpoint is supplied. The guard executes only after the epoch's evaluation and checkpoint block.
6. The display CSV has 120 rows partitioned as three Attempt2 rows and 117 Attempt1 rows; every row declares `cross_attempt_comparable=false`, and the two provenance digests differ. The plot generator makes separate calls for the two partitions, places a boundary at Epoch 3/4, and does not interpolate or smooth across it. Visual inspection and the 2/2 boundary tests both confirmed the physical break. The tracked historical CSV contains Epoch 4–33 only; those rows match the new display exactly. Epoch 34–120 remain bound to Task20-reported private historical evidence rather than an independently inspectable tracked source.
7. Protected historical files were byte-identical between the authorization parent and the review object, including `HANDOFF_20.md`, the exact-resume runbook, final closeout manifest, historical CSV/PNG/Word, and the paper SSOT.
8. Controller-side tests with the bundled Python runtime passed the 2/2 boundary tests and 12 applicable VC-CSA author/metrics tests. Importing the resume-runtime test was blocked because that runtime lacks `torch`; this is an environment limitation, not a recorded test assertion failure. `validate_work_log.py` reported 246 entries and 0 errors, and `git diff --check 349be41..da9c52a` passed.

## 3. Required correction and supplement

### R1 — append-only correction of impossible WORK_LOG time

`WR-20260802-005` records `2026-08-02 15:20:00 +08:00`, but the reviewed commit was authored and committed at `2026-08-02T14:05:13+08:00`; the file metadata also predates the claimed time. The timestamp is therefore impossible for that committed record.

Task20 must not rewrite WR-005. It must append an erratum stating that `15:20:00` is invalid and that the exact authoring time is `UNKNOWN_WITHIN_BOUND`, no later than the trusted commit time `14:05:13 +08:00`, unless it has a stronger already-existing trustworthy timestamp. It must not promote filesystem modification time into an invented event time.

### R2 — use an allowed experiment-registry status

The registry declares the only allowed states as `PLANNED`, `RUNNING`, `COMPLETED`, `FAILED`, `LEAKAGE_BLOCKED`, and `VALIDATION_ONLY`, but the new row uses `COMPLETED_AWAITING_00_REVIEW`. Task20 must change that row to `COMPLETED`; review-pending state belongs in the evidence/review note, not the controlled status field. This is a registry-schema correction only and does not mean Task00 acceptance.

### R3 — disclose missing per-step timestamps; never reconstruct them

The execution contract requires each optimizer-step record to contain a timestamp. The submitted instrumentation writes epoch, step, global step, total/opinion/emotion loss, and learning rate, but no timestamp. The 14,079-row continuity and numeric fields may still be reported, but step timestamps are a permanent evidence gap for this attempt.

Task20 must add `KNOWN_EVIDENCE_GAP_STEP_TIMESTAMPS_NOT_RECORDED` to the completion supplement and private/non-secret evidence index. No wall-clock timestamps may be inferred, interpolated, or backfilled after the run.

### R4 — provide a non-secret private-evidence index sufficient for independent audit

The committed material reports a root ledger and selected checkpoint/fixity hashes, but it does not expose the contract-required category-level hash linkage for the complete private evidence chain. Add a non-secret supplement containing relative category names, counts, byte counts where safe, and hashes only—never credentials, endpoints, absolute paths, sample identities, predictions, checkpoints, labels, or restricted assets. At minimum include:

- final remote runtime aggregate tree SHA-256 and final `main.py`, `train_vccsv.py`, `csmv_dataset.py`, and `resume_utils.py` hashes;
- final argv digest, config hash, code-tree hash, environment hash, input-manifest/fixity hash, and their linkage to this attempt;
- stdout and stderr hashes plus exit-code/stop-reason record hash;
- step-ledger hash, 14,079-row count, continuity/uniqueness result, and the explicit missing-timestamp status;
- per-epoch dev metrics and prediction-file hashes with 10,727 uniqueness/count summaries;
- per-epoch/final checkpoint hashes and cursor summaries, plus failure-bundle ledger roots;
- an explanation that `preflight.json` contains pre-run snapshot hashes, while the final run manifest and final metric script necessarily have later hashes.

The supplement may be derived from existing private ledgers. It does not authorize renewed asset access or another training attempt.

## 4. Independent reproducibility limitation

Both repository virtual-environment launchers failed in the controller session before Python started because they resolve to an unavailable historical Python 3.8 executable. Consequently, Task00 could not independently reproduce Task20's claimed 16/16 and 80/80 runs using those exact environments. With the bundled runtime, the applicable no-torch tests passed, while `run_preparation_checks.py` honestly remained blocked by the historical environment (`formal_model_work_ready=false`, FAISS unavailable, and major ML imports unavailable).

Task20 must record this controller-side limitation in its supplement. It may provide a non-secret launcher/environment provenance explanation; it must not alter or rebuild the environment as part of this correction unless separately authorized.

## 5. Decision and immutable boundaries

- `REVIEW-00-TASK20-EPOCH1-3-RECOVERY-20260802 = SUPPLEMENT_REQUIRED_NO_ACCEPTANCE_YET`.
- No rerun is authorized. The single completed Attempt2 remains the only authorized attempt.
- The original Attempt1 Epoch 1–3 evidence gap remains unchanged.
- Attempt2 stays permanently NON_T0 and formally ineligible; it cannot enter G3, Task30/40/50, the paper SSOT, a baseline ranking, statistical testing, or a performance/generalization/no-leakage claim.
- I3D license, official revision, and rights-holder package identity/fixity remain `UNKNOWN`; no redistribution is authorized.
- The visible-layer deletion deadline remains `2026-08-31 23:59:59 +08:00`; platform-control-plane erasure remains `UNKNOWN`.
- G1, G2, G3, the manuscript status, Task30's H1 gate, and the prohibition on creating Task40 before H1 are unchanged.

Task20 may return one minimal corrective commit containing the append-only WORK_LOG erratum, registry-state correction, versioned non-secret supplement/index, and any directly necessary manifest/completion cross-reference. Task00 will then perform a new independent review.
