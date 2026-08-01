# Task 10 Manuscript Section Completion — 2026-08-01

> Review request owner: Task 00 total control  
> Task: `10-M1–M2 数据与协议`  
> Research SSOT: `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21  
> Initial Git baseline after `git fetch origin`: `d213c25`; shared `main` advanced through unrelated Task 20/00 commits to `8b57b2a` and remained equal to `origin/main` before Task 10 staging  
> Manuscript state: `MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS`  
> Gate state preserved: G1=`PASS`; G2 protocol/data=`PASS_WITH_LIMITATIONS`; asset admissibility=`DEFERRED_ACCEPTED_RISK`; G3=`PASS_WITH_LIMITATIONS`; C1--C4=`TO_VERIFY`

## 1. Controlled scope completed

The Task 10 data/protocol layer has been added to `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.1 without resolving result gates or upgrading any claim.

| Manuscript location | Controlled addition | Primary evidence |
|---|---|---|
| Sec. 1.1 | Bounded the estimand to sampled public/elicited responders; distinguished the observed distribution from silent viewers and population prevalence; retained response support and uncertainty | Master plan §§0.9, 2.1; `DATA_CARD_DATASET_V1.md`; `DATASHEET_DATASET_V1.md` |
| Sec. 3.1 | Distinguished categorical comment aggregation from the frozen LAI-GAI 12-dimensional rating map; fixed video/image as native statistical units | `experiment-protocol-v2.md` §§2--3; `data/manifests/lai-gai-label-provenance-v1.manifest.json` |
| Sec. 3.2--3.3 | Specified T0/T+Delta separation, prohibited post-publication signals, physical label-tier isolation, split-before-index, train-only indexing, and `LEAKAGE_BLOCKED` consequences | `T0_INPUT_POLICY.md`; `experiment-protocol-v2.md` §§1, 6, 8; `M2_LEAKAGE_AUDIT.md` |
| Sec. 3.4 | Fixed CSMV to frozen I3D visual sequences; fixed LAI-GAI to image-domain HUMAN_GOLD evidence; preserved Video2Reaction silver-label and non-pooling boundaries | Master plan §§0.4--0.5, 0.8.1, 4; `DATA_SOURCE_LEDGER.md` |
| Sec. 5.2 | Added dataset-native counts, label provenance, evidence roles, license-layer separation, I3D non-redistribution, and HUMAN_GOLD/silver asymmetry | `DATA_SOURCE_LEDGER.md`; `DATA_CARD_DATASET_V1.md`; `DATA_RELEASE_BOUNDARY.md` |
| Sec. 5.3 | Added the frozen CSMV and LAI-GAI split counts, grouping rules, leakage-gate coverage, and honest unavailable/not-built boundaries | `data/manifests/split-v1.manifest.json`; `data/manifests/lai-gai-split-v1.manifest.json`; `M2_LEAKAGE_AUDIT.md` |
| Sec. 5.7 | Fixed native-unit paired inference and prohibited comments, raters, folds, or seeds as independent sample units; prohibited absolute cross-dataset metric comparison | Master plan §7.3; `experiment-protocol-v2.md` §§2, 4 |
| Sec. 8 | Added responder-selection and HUMAN_GOLD/silver limitations while retaining I3D accepted-risk and non-generalization boundaries | `DATA_CARD_DATASET_V1.md`; `PRIVACY_STATEMENT.md`; `DATA_RELEASE_BOUNDARY.md` |
| Data Availability | Replaced the generic data placeholder with the currently supportable release/non-release boundary and retained the unresolved final archive decision | `DATA_SOURCE_LEDGER.md`; `DATA_RELEASE_BOUNDARY.md`; `PLATFORM_TERMS_STATEMENT.md` |
| Ethics, Privacy, and Responsible Use | Added data minimization, LAI-GAI consent/data-use filtering, prohibited uses, withdrawal/fixity response, and a retained institutional-decision gap | `PRIVACY_STATEMENT.md`; `PLATFORM_TERMS_STATEMENT.md`; LAI-GAI label-provenance manifest |
| Supplement S1/S2 | Specified lineage/license/fixity fields and deterministic split/leakage evidence, including unavailable dimensions and fail-closed tests | Task 10 manifests, Data Card/Datasheet, `M2_LEAKAGE_AUDIT.md` |

## 2. Claims supportable at this stage

Only descriptive protocol and provenance statements are supported:

- the estimand is the observed distribution of publicly expressed or elicited induced reactions among retained responders, not all viewers' latent affect;
- CSMV and LAI-GAI are distinct HUMAN_GOLD evidence sources with video and image as their native units;
- CSMV formal input is the fixed I3D visual sequence, with audio structurally unavailable and target comments prohibited at T0;
- LAI-GAI prompt/target-generation fields are provenance rather than truth and are excluded from the default input;
- HUMAN_GOLD, silver, and unlabeled evidence are physically separated;
- the current formal splits and leakage gates are documented, while CSMV chronological/topic/publisher claims remain unavailable;
- I3D internal use is an accepted risk, not closed license evidence or redistribution authority.

These statements do **not** upgrade C1. C1--C4 remain `TO_VERIFY` until the frozen experiment and statistical evidence required by the claim matrix exists.

## 3. Citation handling

No citation gap was replaced. The existing six citation slots remain because this batch did not have locator-backed, sentence-level support records satisfying the citation contract. In particular, no source identity or venue status was inferred from memory, and Video2Reaction remains the closest/direct prior under its existing citation gap.

## 4. Intentionally unresolved slots

- all Abstract result content;
- all Sec. 6 Results content and numerical tables;
- Sec. 7 evidence-based interpretation;
- Sec. 9 Conclusion;
- final C1--C4 states and contribution wording;
- final archive locators and public release version;
- the applicable institutional ethics determination;
- the verified IEEE reference list and all sentence-level citation-support decisions;
- final code repository/archive statement, author list, CRediT, conflicts, funding, acknowledgments, and AI-use disclosure.

## 5. Open risks and limitations

1. The fixed I3D package's asset-level license, stable official revision, rightsholder package identity, and external fixity attestation remain unresolved. `DEFERRED_ACCEPTED_RISK` permits the recorded internal research scope only; it does not permit redistribution or official-authorization language.
2. Video2Reaction-native intake, revision, file hashes, media recovery, and movie-disjoint audit remain Task 50 work. Its native labels remain `SILVER_LLM_HUMAN_VERIFIED`.
3. CUC-IGPE-v2 consent, platform permission, and redistribution rights remain unresolved; it stays local silver/unlabeled stress evidence.
4. Commenter/responder selection, platform ranking/moderation, and finite response support limit population interpretation.
5. Automated leakage tests reject enumerated failure signatures but do not prove that all semantic near-duplicates, source events, or future leakage have been exhaustively detected.
6. CSMV lacks a released publication-time protocol, native topic field, and publisher identity for the corresponding split claims.

## 6. Scope not touched

- The master plan, G1--G3 states, `CLAIM_EVIDENCE_MATRIX.md`, and CARM method definition were not modified.
- Abstract results, Sec. 4 Method, Sec. 6 Results, Sec. 7 Discussion, and Sec. 9 Conclusion were not filled.
- No Task 20 result, single-seed value, smoke result, NON_T0 result, or leakage-accepted exploratory value was inserted.
- No model was trained, no index was built, no data was downloaded, and no Task 20/30/40/50 interface was changed.
- The untracked `NEmoP/`, `__MACOSX/`, and `tmp/` directories were not read, modified, or staged.

## 7. Evidence fixity at content completion

| Artifact | SHA-256 |
|---|---|
| `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` | `5e697a8c722cb5e79d4bcfd015c4e848fa948e2d5dcae07f8132562f281a27bb` |
| `experiment-protocol-v2.md` | `53a08ff90608c982c700759683566fb0a52216ebeed33f185b2406373ba4d976` |
| `T0_INPUT_POLICY.md` | `287356695d0be3b6cbbd5760ee926e43dde90437abf4bfcd920b3c1276cea1d5` |
| `DATA_SOURCE_LEDGER.md` | `abe0adfb7ad2fa16d5bf8135416ad06a581c944a1b9fe8c01b7abfbb6c903770` |
| `DATA_CARD_DATASET_V1.md` | `e65f9febf879a6a2670d86633728c8b1bacb2e4b9a76a4dfd5c5f1a30edba494` |
| `DATASHEET_DATASET_V1.md` | `6721b0e6d3f2468ec287dfc16d5cd1f43e348bb58cf9de99435b374f769c8811` |
| `data/manifests/dataset-v1.manifest.json` | `1b8ba9f5c4b801f9530b4e97c8f6b777db4562bce37b24d63aa341b64e3e806e` |
| `data/manifests/split-v1.manifest.json` | `6a15f992b9e5839d6f21b4a6d40619f48bb14445b18a0c1814024794f56b6780` |
| `data/manifests/lai-gai-label-provenance-v1.manifest.json` | `198b9930596074af01ed3d37db92a3fd57db9cca1bfb9d2d96e8c3e581cd94cd` |
| `data/manifests/lai-gai-split-v1.manifest.json` | `07ba017e9d192361de24feb8682d957ba7c83c73ac9206df5990f9017c47fae9` |
| `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.1 | `9d95dc0a7ee01ecdc1232bdd45b2c8b818dd7ebea868f3b8c33a52953b15a941` |

## 8. Validation record before final Git handoff

- Required `.\.venv\Scripts\python.exe` entry for the manuscript, work-log, and preparation validators: **FAILED, exit 101**, because the project launcher points to a missing Python 3.8 base interpreter. The failure is retained and was not repaired or suppressed in this manuscript-only task.
- Bundled-workspace Python fallback running the identical `scripts/validate_manuscript_ssot.py`: **PASS, exit 0**; `manuscript_bytes=43849`, `blueprint_bytes=13806`, `citation_slots=6`, `result_gates=18`.
- Bundled-workspace Python fallback running `scripts/validate_work_log.py` before the Task 10 log append: **PASS, exit 0**; 232 entries, zero errors, latest existing entry `WR-20260801-003`.
- An existing Anaconda Python with the required YAML/NumPy dependencies running `scripts/run_preparation_checks.py`: **exit 1 with `blocking_checks=[historical_environment]`**. The Task 10 data/protocol checks, M2 release, I3D sequence protocol, label-tier isolation, LAI-GAI freeze, secret scan, and template checks all passed; the remaining failure reports the separate historical/formal environment as not ready under that interpreter. No environment dependency was installed or changed.
- `git diff --check`: **PASS, exit 0** at content-completion check.

The Task 10 work record preserves the pre-commit validation state. The final Task 10 response records the actual commit and push outcome after those actions occur.
