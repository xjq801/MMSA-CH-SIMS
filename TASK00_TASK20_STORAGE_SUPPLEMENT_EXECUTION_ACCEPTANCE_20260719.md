# 00 Task20 restricted-storage supplement execution acceptance

Date: 2026-07-19  
Decision: `SC-20260719-03`  
Reviewed submission: `main@229dbcd0b38cd13ecb945c63c94f31feab91f687`  
Authority: `SC-20260719-02` and `TASK00_VCCSA_RESTRICTED_STORAGE_AND_IMAGE_SUPPLEMENT_AUTHORIZATION_20260719.md`

## Decision

`TASK20_STORAGE_SUPPLEMENT_EXECUTION=ACCEPTED_FOR_REPORTED_MATBOX_BACKUP_AND_CONFIG_MIRROR`

This accepts the reported execution of the authorized private MatBox I3D backup and separate non-sensitive configuration mirror. It does not amend historical contracts.

## Independently reviewed record

The reviewed tracked record is `WORK_LOG.md`, WR-20260719-005, committed in `229dbcd`. It reports:

- MatBox I3D target binding digest: `2c9b6bedc811c90ecfd230d1fd03d7b236e29d9a9b49f38be7c8415f50ca9e58`.
- Private ACL summary: directory `0700`, owner-only; copied files `0600`; static encryption and platform control plane remain `UNKNOWN_PLATFORM_CONTROL_PLANE`.
- Source-to-target fixity: `count=8210`, `bytes=2283804928`, and `missing=[]`, `extra=[]`, `size_mismatch=[]`, `sha256_mismatch=[]`; content-tree SHA-256=`592eb698694388f3ab169c924f88e470daa64d5b496ff007cec390f7d1ada925`.
- Separate configuration-mirror digest: `f2d4841dcda36c912d5b94984fd823c1cb64caf08753d10af440c71ef855551c`, directory `0700`, files `0600`, reported to contain only a dependency lock and Python-version record.

00 has independently inspected this tracked submission and its consistency with the S13 authorization. 00 did not access the private MatBox target, raw endpoint, credentials, or restricted files; the target-side fixity and ACL observations are therefore accepted as task20-reported evidence, not a direct 00 remote rerun.

## Status and boundaries

- `RUNTIME_SNAPSHOT=DEFERRED_NOT_STARTED`; it is not accepted as created or verified.
- `A30_SEED_3407_TRAINING=REPORTED_ACTIVE_NOT_COMPLETED`; no metric, completion, recovery, or training-result claim is accepted here.
- Retention is restricted material until minimum-evidence acceptance plus 30 calendar days; visible-layer deletion must later be documented. Platform-side retention/control-plane behavior remains UNKNOWN.
- `tmp/` remains task20-owned, ignored and untracked. It was neither read nor staged by 00.
- This decision preserves `AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY` and `FORMAL_EVIDENCE_ELIGIBILITY=INELIGIBLE`. It does not promote anything to T0, G3 main evidence, unified baselines, Task50, or paper claims.
- I3D license, official revision, and rightsholder package identity/fixity remain UNKNOWN. Any rightsholder denial or 8210 coverage/hash drift remains `ASSET_INVALIDATED_DO_NOT_REPORT`.

## Gate evidence and limitation

Task20 recorded `validate_work_log` PASS (133 records) and `run_preparation_checks` with `blocking_checks=[]`. In 00's current local checkout, both project Python 3.8 virtual environments are drifted (their configured interpreter is absent), while the bundled Python lacks PyYAML; 00 therefore did not falsely rerun the preparation gate. Work-log structure can be independently checked with the bundled interpreter.

## Allowed next action

Task20 may continue the already-authorized exploratory run and, only at a safe pause or completion, create and separately record a private runtime snapshot under S13. It must record any snapshot binding/fixity, final run status, retention deadline and later visible-layer deletion verification without exposing restricted content or secrets.
