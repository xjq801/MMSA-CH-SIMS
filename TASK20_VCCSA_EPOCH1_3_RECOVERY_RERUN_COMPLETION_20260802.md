# Task20 VC-CSA Epoch 1–3 independent recovery rerun completion

> Attempt: `TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_SEED3407_ATTEMPT2`  
> Status: `COMPLETED_AWAITING_00_REVIEW`  
> Identity: `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY`  
> Formal evidence eligibility: `INELIGIBLE`

## 1. Scope and immutable boundary

This was the single authorized independent rerun under `TASK00_TASK20_EPOCH1_3_RECOVERY_RERUN_DECISION_AND_EXECUTION_CONTRACT_20260802.md` (SHA-256 `f94198fba4329808544be060087af8b6e45a7dfeae42527e81531caed097922c`). It began from a new model/optimizer/scheduler/RNG initialization, retained `max_epoch=120` scheduler semantics, and used a tested execution guard only after Epoch 3 training, dev evaluation, dev prediction, and checkpoint persistence had closed.

It is not a resume or continuation of the historical full run. The original run's Epoch 1–3 raw evidence remains missing. Attempt2 Epoch 1–3 and Attempt1 Epoch 4–120 are not cross-attempt comparable and may only be displayed as disconnected partitions.

## 2. Bound execution outcome

- Start: `2026-08-02T11:26:51+08:00`; end: `2026-08-02T13:12:53+08:00`; exit code `0`.
- Exact stop message: `execution guard stopped after completed epoch 3`.
- Three complete epochs, 4,693 train steps per epoch, 14,079 unique continuous global steps.
- Each epoch has 10,727 unique dev predictions. `test_access=0`; no test metric or prediction was read or reported.
- The structured ledger contains finite total/opinion/emotion loss and learning rate for every step. No NaN/Inf, CUDA OOM, `Killed`, traceback, or data-read error was detected in the completed run.
- Final rolling checkpoint cursor: `epoch_index=3`, `next_batch_index=0`, `global_step=14079`.
- The source-label audit found one non-normalized raw opinion label row per epoch and zero emotion rows. The sidecar did not silently normalize malformed raw vectors; it used the explicit `author_label_classindex_one_hot` target contract and disclosed the anomaly.

The complete aggregate Epoch 1–3 losses, author dev scores, and nine dev metrics are in `experiments/task20-vccsa-epoch1-3-recovery-attempt2/epoch-metrics-summary.json` (SHA-256 `444d55ec62c95b927d9acc29cbf66811378aa6cf34080cb896197cd1f217db30`). Per-sample predictions and checkpoints remain private and are not in Git.

## 3. Private evidence and fixity

- Private final-bundle `SHA256SUMS`: `ff070dd3f92b78cd1e5a4d7b85d9ed16fd3d273fb30e26f7a92694bba82f524b`; every listed file verified.
- Directory mode `0700`; payload file mode `0600`; residual `.tmp` files: `0`.
- Final rolling checkpoint: 1,742,994,811 bytes; SHA-256 `dcf8952e418d73267ea8dccb79bd5fd13b0d88a7223d2542aa8da88ab3e916e2`.
- Final best update at Epoch 3: 1,742,976,061 bytes; SHA-256 `49da29417ea2b6e522c14947a16d2e2d000f603f8062923f36fff0abdbfcd7c7`.
- Post-run I3D fixity record SHA-256 `05492891ee63bbd0f7fffef62908191223c31c944b95e185dcc50be91b7c14d4`: 8,210/8,210 files, 2,283,804,928 bytes, content-tree SHA-256 `592eb698694388f3ab169c924f88e470daa64d5b496ff007cec390f7d1ada925`; missing/extra/size/hash/mode differences all empty.
- Per-epoch private ledgers: Epoch 1 `b2aade33154043cb297098eacc3d6ad8823764d6b089315abe220ae01561656d`; Epoch 2 `e4f1a70668399e340c9fcb10a3be1fb382863a92145c5c9eb1736ee1cdfb7d9b`; Epoch 3 `ccd623aee519450e9f804dacf063abd0989b784faf66b7dcdeb5e6cc713931c4`.

The existing visible-layer deletion deadline remains `2026-08-31 23:59:59 +08:00`. No claim of platform-control-plane physical erasure is made.

## 4. Versioned disconnected display

The new display package does not overwrite the historical Epoch 4–120 CSV/PNG/Word. Every CSV row carries its attempt ID, epoch label, source-artifact SHA-256, run-provenance digest, and `cross_attempt_comparable=false`. The plot makes two independent line calls and inserts a labeled blank boundary at Epoch 3/4; there is no cross-boundary interpolation, smoothing, AUC, or trend fit.

- CSV: `deliverables/TASK20_VCCSA_NON_T0_EPOCH1_3_ATTEMPT2_WITH_EPOCH4_120_ATTEMPT_BOUNDARY_20260802.csv`, SHA-256 `e98f0fa5877ea6ddb6b278e81d06d920802e6bd666ff8085f48d7e253475176f`.
- PNG: same prefix with `.png`, SHA-256 `fad4b68656141ce416e04324db74aca5c6633cc317bda24e8220b66a50680fcc`.
- SVG: same prefix with `.svg`, SHA-256 `38f9616ca1961c7ccbd1be545955ae6e78a18d8699e9e7f04fb11566a20ca5a7`.
- Generator: `scripts/plot_vccsa_attempt_boundary.py`, SHA-256 `903b3eed931002d418130b0ebb912eb815f16a5eb5a0483809bd2bea58aec10e`.

The historical full run used multiple runtime instances. Its CSV `run_instance_digest` is therefore a synthetic provenance digest bound to the historical final-bundle manifest SHA-256, not a false claim of one physical GPU instance. Attempt2 uses the digest of its non-secret bound host-key/GPU/endpoint triple.

## 5. Failure evidence retained

Failures were not deleted or rewritten as success:

1. Initial dependency/environment restoration attempts and a zero-step launch caused by the unextracted label archive failed; the failure bundle was retained before the corrected engineering retry.
2. The nine-metric sidecar initially failed closed on the malformed raw opinion-label row; the target contract was then made explicit and tested.
3. An early per-epoch checksum list included itself; it was rejected and regenerated with a deterministic self-exclusion rule.
4. A local monitor timed out while the remote large-file copy continued; completion was accepted only after the remote copy stopped and all hashes verified.
5. The first post-run fixity command used the wrong manifest field name and stopped before replacing the final record. The corrected exact pass succeeded.
6. The first regenerated final checksum list accidentally included its temporary checksum file; `sha256sum -c` exposed the error. The list was regenerated excluding all `SHA256SUMS*` files and then passed in full.

## 6. Non-secret submitted artifacts and immutable limitations

The run manifest is `experiments/task20-vccsa-epoch1-3-recovery-attempt2/run-manifest.json` (SHA-256 `9c029559f101edee158bab702ac8fd0dedf794f20a8b2feade1c32c0272b96a9`). The final Task20 script/test bundle digest is `d189175655803bd2274731490b956fd5bfaf6fbca6321f26eea2f6e67f6c4c5b` under the manifest's stated path/hash scheme.

This work does not change G1–G3, Task20 formal-core closure, Task30/40/50, the paper SSOT, or any historical hash-bound handoff. It cannot support a T0 result, G3 result, unified-baseline result, Task50 result, paper performance claim, no-leakage claim, or resolved I3D-license/revision/rights-holder identity claim. I3D external license, official revision, and rights-holder package identity/fixity remain `UNKNOWN`.

## 7. Review request

`REQUEST_00_TASK20_EPOCH1_3_RECOVERY_REVIEW`: please independently verify the bound attempt, non-secret hashes, execution-guard semantics, private ledger/fixity assertions, display boundary, failures, and permanent evidence limitations. Task20 does not self-approve this submission.
