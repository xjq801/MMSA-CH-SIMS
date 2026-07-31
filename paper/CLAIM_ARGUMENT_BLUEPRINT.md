# T-AFFC Claim and Argument Blueprint

> Version: 0.1.0  
> Status: ACTIVE_CONTROL_DOCUMENT / NO_FORMAL_RESULTS  
> Research SSOT: `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.21  
> Manuscript: `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.0

## 1. Paper thesis

The paper does **not** argue that content-to-audience affect distribution forecasting is a new task. Its central thesis is conditional and falsifiable:

> Under a strict publication-time information boundary, training-only response supervision and historical reaction evidence may improve content-to-audience affect distribution forecasting, but a publishable reliability claim requires the system to identify and avoid harmful retrieval under pre-registered distribution shifts and matched-coverage selective evaluation.

The strongest potential contribution is the evidence chain for benefit-aware reaction memory, not the presence of a teacher, memory, router, rejection head, or distribution output by itself.

## 2. Argument chain

| Step | Proposition | Evidence needed | If unsupported |
|---|---|---|---|
| P1 | The estimand is observable and bounded | Construct definition, HUMAN_GOLD provenance, response counts, label uncertainty | Narrow the construct or stop |
| P2 | Evaluation reflects deployment-time information | T0 policy, physical isolation, split/index audits, E0 rejection tests | Protocol claim fails |
| P3 | Privileged responses add train-time value | H1/E3, strong content-only and KD controls, mismatch negative control | Remove privileged-effect claim |
| P4 | Historical reactions help selectively rather than indiscriminately | H2/E2/E4/E7, OOF utility, strong router controls, negative-transfer statistics | Downgrade to ordinary retrieval or null result |
| P5 | Supported effects survive meaningful shifts | H3/E5/E6, two HUMAN_GOLD roles, Video2Reaction dual track, calibration/selective risk | Limit claim to in-domain evidence |

The introduction motivates P1–P5; the method operationalizes P2–P4; the experiments attempt to falsify P2–P5; the discussion may interpret only propositions that survive.

## 3. Claim contracts

| Claim | Current state | Minimum evidence for support | Falsifier/downgrade | Manuscript destinations |
|---|---|---|---|---|
| C1 strict-T0 protocol/evidence | TO_VERIFY | Two HUMAN_GOLD datasets; content-unit split; target/future isolation; train-only index; zero blocking leakage findings | Target response/future information enters input/index, or one main dataset is not reproducible | Abstract context, Intro contribution 1, Sec. 3, Sec. 5.2–5.3, Sec. 6.1 |
| C2 privileged-response supervision | TO_VERIFY | Strong content-only, hard/soft, ordinary KD, privileged KD, teacher upper bound, mismatch control; five seeds; native-unit CI; calibration | No stable gain, calibration harm, random-split-only gain, or extra-budget confound | Intro contribution 2, Sec. 4.3, Sec. 5.4–5.5, Sec. 6.2 |
| C3 benefit-aware reaction memory | TO_VERIFY | OOF utility; no/random/lexical/kNN/learned retrieval; fixed/similarity/entropy/SelectiveNet controls; matched coverage; pollution tests; negative-transfer reduction | Learned retrieval not above ordinary retrieval, utility leaks, router not above strong controls, or OOD harm not avoided | Title only if supported, Intro contribution 3, Sec. 4.4–4.6, Sec. 6.3/6.5 |
| C4 reliability under shift | TO_VERIFY | Pre-registered group/topic/time/platform/cross-data shifts; calibration, AURC/risk–coverage; two HUMAN_GOLD roles; failures disclosed | Benefit disappears or reverses under shifts, external evidence is silver-only, or coverage is incomparable | Abstract result, Intro contribution 4, Sec. 5.3, Sec. 6.4–6.5, Discussion |

Only `SUPPORTED` and `SUPPORTED_LIMITED` states may produce affirmative result claims. `REFUTED` must remain visible as a negative result if the experiment was pre-registered and scientifically material.

## 4. Section-to-evidence map

| Section | Main job | Claim inputs | Exit test |
|---|---|---|---|
| Title | Name the supported scientific problem, not modules | C3/C4 only if supported | No “first/novel/new”; no unsupported CARM name |
| Abstract | One-paragraph problem–gap–method–evidence–boundary | Final C1–C4 states | Every result traceable; 150–250 words; no citations |
| Introduction | Establish construct, direct prior, reliability gap, RQ, bounded contributions | C1–C4 plan and final states | Contributions match abstract/conclusion |
| Related Work | Position against direct and adjacent work | Citation audit, prior-art matrix | Video2Reaction named closest/direct prior |
| Problem | Freeze estimand and T0 boundary | Protocol v2, data lineage | No target/future ambiguity |
| Method | Define mechanisms and provenance | Task30/40 frozen method | Every module has failure hypothesis/control |
| Experiments | Make falsification credible | Task50 preregistration | Same split/input/budget; native-unit stats |
| Results | Present evidence without interpretation inflation | Frozen metrics/predictions/statistics | No dev/single-seed/exploratory leakage |
| Discussion | Explain what survived and where it fails | Supported/limited/refuted claims | No new result or causal overreach |
| Limitations | Bound construct, assets, domains, and misuse | Risk register/data statements | No hidden accepted risk |
| Conclusion | Answer RQ at supported strength | Final claim matrix | No task-first or all-viewer claim |

## 5. Planned figures and tables

Every visual must support a claim or audit question.

| ID | Artifact | Claim/question served | Source requirement |
|---|---|---|---|
| Fig. 1 | Problem and T0 information boundary | C1: what is prohibited and available | Protocol/source lineage, no result |
| Fig. 2 | Method with training-only response and memory paths | C2/C3 mechanism | Frozen architecture/config |
| Fig. 3 | Benefit-aware routing and OOF utility construction | C3 mechanism validity | Cross-fitting implementation/tests |
| Fig. 4 | Risk–coverage and calibration under shift | C3/C4 reliability | Frozen predictions, five seeds/CI |
| Fig. 5 | Retrieval utility and negative-transfer analysis | C3 harm avoidance | Neighbor audit and paired outcomes |
| Fig. 6 | OOD and cross-dataset effect summary | C4 boundaries | Pre-registered shift results |
| Table 1 | Dataset roles, constructs, labels, inputs, splits | C1 construct/evidence | Manifests and Data Cards |
| Table 2 | Closest-prior and method-position comparison | Novelty boundary | Citation-verified prior-art matrix |
| Table 3 | Main HUMAN_GOLD results | C2–C4 | Results freeze only |
| Table 4 | Memory/router ablations and strong controls | C3 | Results freeze only |
| Table 5 | OOD, missing-input, calibration, selective risk | C4 | Results freeze only |
| Table 6 | Efficiency and reproducibility | Practicality | Run manifests/hardware logs |

If a figure cannot be linked to a claim or audit requirement, it is supplementary or removed.

## 6. Reviewer-attack pre-mortem

| Likely rejection | Evidence-based answer required | Manuscript defense |
|---|---|---|
| “Video2Reaction already proposed the task.” | Direct acknowledgment and protocol-matched comparison | No task-first claim; reliability/OOD question in title and introduction |
| “This is a teacher + retrieval + router module collage.” | Each component maps to a failure mechanism; strong controls; router reduces harmful retrieval | Mechanism-first ablations and negative controls |
| “Comments are not audience emotion.” | Bounded construct, response counts, HUMAN_GOLD/silver separation, selection-bias limits | Construct paragraph and Limitations first-class, not buried |
| “Random splits leak video/comment identity.” | Content-unit grouped splits, duplicate/source audits, physical target-response isolation | E0 and provenance figure |
| “The router is just entropy thresholding.” | Matched-coverage comparison against entropy, similarity, fixed fusion, SelectiveNet | C3 support gate |
| “OOD claims are cherry-picked.” | Pre-registered shifts and all outcomes, including adverse ones | Complete shift matrix and frozen reporting |
| “Five seeds are treated as sample size.” | Native-content-unit paired bootstrap; seeds summarize training variation | Statistical section |
| “Results are not reproducible due to restricted assets.” | Exact manifests/fixity, access instructions, eligible code/splits, explicit non-redistribution | Data/Code Availability and risk disclosure |
| “The model enables affective surveillance.” | Public-expression construct, selective use boundaries, privacy and misuse mitigation | Responsible-use statement |

## 7. Claim blacklist operationalization

The active manuscript must not assert or imply:

- first content/video-to-audience affect prediction;
- first audience-reaction distribution task or benchmark;
- prior work never predicted induced audience affect;
- distribution output itself is novel;
- teacher, memory, router, rejection, or their combination is a module-level first;
- comments represent all viewers’ private emotions;
- state-of-the-art, significant superiority, robust generalization, or reliability before the required statistics and shifts are complete.

Historical descriptions, explicit negations, and this control document may mention the prohibited concepts only to prevent their use.

## 8. Citation-slot registry

| Slot | Required source class | Candidate verified repository key/source | Status |
|---|---|---|---|
| CIT-INDUCED_AFFECT_AND_LDL | Primary papers on induced affect and label-distribution prediction | CSMV, NEmo+, MVIndEmo plus dedicated LDL sources | PARTIAL |
| CIT-VIDEO2REACTION | Official arXiv record and any verified archival record | arXiv:2607.06875; archival venue status must be rechecked | PARTIAL |
| CIT-LUPI_GD_M2PKD | Primary LUPI, generalized distillation, M2PKD papers | `vapnik2009lupi`, `lopezpaz2016generalizeddistillation`, `aslam2023m2pkd` | READY_FOR_CLAIM_AUDIT |
| CIT-RAMER_AND_RETRIEVAL | Primary retrieval-augmented affect work and nearest-neighbor controls | `fan2024ramer` plus direct updates | PARTIAL |
| CIT-CALIBRATION_SELECTIVE_MISSING | Primary calibration, selective classification, AURC, and missing-modality work | `geifman2017selectiveclassification`, `geifman2019selectivenet`, `traub2024augrc`, `lin2023missmodal`, `wang2023imder` | PARTIAL |
| CIT-VERIFIED_IEEE_STYLE_REFERENCE_LIST | Complete final reference list with identifier and sentence-level support audit | `references/references.bib` plus future verified additions | NOT_READY |

No citation slot is considered final until bibliographic identity and sentence-level claim support are independently verified.

## 9. Result-ingestion contract

A number may enter the manuscript only when all fields below are available:

```yaml
claim_id:
experiment_id:
dataset_and_split:
estimand:
metric_and_direction:
aggregation_unit:
seeds:
point_estimate:
uncertainty_interval:
comparison:
multiple_comparison_rule:
config_id:
code_commit:
prediction_artifact:
statistics_artifact:
review_status:
```

Rules:

1. Development trends, single-seed runs, smoke tests, exploratory NON_T0 runs, and leakage-accepted runs never populate formal result slots.
2. Copy values from a frozen machine-readable result source or generated table, not from chat or handwritten notes.
3. A result paragraph must state unit, protocol, comparator, effect direction, uncertainty, and limitation.
4. If a new result changes a headline claim, update the claim matrix first and then broadcast the change to abstract, contributions, results, discussion, conclusion, figures, and supplement.
5. Null and adverse outcomes are retained if pre-registered or mechanistically important.

## 10. Negative-result downgrade paths

- **H1 fails:** remove privileged-supervision superiority; retain strict protocol and report the teacher as a negative result or upper bound.
- **H2 retrieval helps but router fails:** describe ordinary train-only retrieval; remove “benefit-aware” and negative-transfer-avoidance claims.
- **H2 retrieval fails:** center the evidence on why content similarity does not transfer audience reactions; do not add unplanned modules after test access.
- **H3 has no eligible multimodal protocol:** report `NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`; do not synthesize missing modalities.
- **C4 fails under shift:** limit claims to in-domain prediction and make the shift failure a principal limitation.
- **Video2Reaction cannot be fairly executed:** provide a complete input/label/split/license/resource/budget non-executability audit; do not omit the direct prior.

## 11. Living-paper update cadence

- **Now through Task 40:** write stable definitions, related-work synthesis, method decisions, and experiment preregistration; leave empirical prose gated.
- **Task 50 active:** ingest only quality-controlled intermediate artifacts into internal tables; keep headline claims provisional.
- **Results freeze:** generate tables/figures, resolve claim states, then write Results, Discussion, Conclusion, and final Abstract.
- **Task 60:** run citation, consistency, integrity, anonymity, reproducibility, and adversarial review passes before generating IEEE LaTeX/Word.
- **After any definition change:** update this blueprint and all mapped manuscript sections in the same batch.

## 12. Submission-quality definition

“Top-journal quality” means that every important statement is precise, falsifiable where applicable, supported at the native statistical unit, comparable under a fair protocol, traceable to an artifact, and bounded by construct, data, license, and domain limitations. It does not mean removing uncertainty or writing as if reviewers cannot disagree.
