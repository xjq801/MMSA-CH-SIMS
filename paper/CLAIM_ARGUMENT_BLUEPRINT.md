# T-AFFC Claim and Argument Blueprint

> Version: 0.1.1  
> Status: ACTIVE_CONTROL_DOCUMENT / NO_FORMAL_RESULTS  
> Research SSOT: `TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md` v1.23  
> Manuscript: `paper/TAFFC_CARM_MANUSCRIPT_SSOT.md` v0.1.3

## 1. Paper thesis

The paper does **not** argue that content-to-audience affect distribution forecasting is a new task. Its central thesis is conditional and falsifiable:

> Under a strict publication-time information boundary, train-only historical reaction evidence may improve content-to-audience affect distribution forecasting, but a publishable reliability claim requires posterior evidence that the benefit is credible despite finite response samples and that harmful retrieval is avoided under matched-coverage evaluation.

The strongest potential contribution is the evidence chain for credible net-benefit reaction memory, not the presence of memory, a router, rejection head, posterior, or distribution output by itself. Task 30 privileged-teacher development is an archived non-pass and is outside the active claim set.

## 2. Argument chain

| Step | Proposition | Evidence needed | If unsupported |
|---|---|---|---|
| P1 | The estimand is observable and bounded | Construct definition, HUMAN_GOLD provenance, response counts, label uncertainty | Narrow the construct or stop |
| P2 | Evaluation reflects deployment-time information | T0 policy, physical isolation, split/index audits, E0 rejection tests | Protocol claim fails |
| P3 | Historical reactions have selectable headroom | H2a/E2, mismatch analysis, content/memory/fixed-fusion oracle | Stop before router if absent |
| P4 | Posterior net benefit identifies harmful history beyond point estimates | H2b/E4/E7, OOF point/posterior utility, strong router controls, response thinning, negative-transfer statistics | Downgrade to point routing, ordinary retrieval, or null result |
| P5 | Separately validated uncertainty supports bounded reliability | H2c/E5/E6, two HUMAN_GOLD roles, Video2Reaction conditional dual track, coverage and region size | Remove decomposition/region or limit to in-domain evidence |

The introduction motivates P1–P5; the method operationalizes P2–P4; the experiments attempt to falsify P2–P5; the discussion may interpret only propositions that survive.

## 3. Claim contracts

| Claim | Current state | Minimum evidence for support | Falsifier/downgrade | Manuscript destinations |
|---|---|---|---|---|
| C1 strict-T0 protocol/evidence | TO_VERIFY | Two HUMAN_GOLD datasets; content-unit split; target/future isolation; train-only index; zero blocking leakage findings | Target response/future information enters input/index, or one main dataset is not reproducible | Abstract context, Intro contribution 1, Sec. 3, Sec. 5.2–5.3, Sec. 6.1 |
| C2 credible net-benefit reaction memory | TO_VERIFY | Natural mismatch and oracle headroom; five-fold group OOF point/posterior utility; no/random/lexical/kNN/learned retrieval; fixed/similarity/entropy/OOD/generic/SelectiveNet/point-router controls; 90% matched coverage; response thinning; negative-transfer reduction | Oracle absent, utility leaks, posterior router not above point/generic controls, benefit unstable to thinning, or OOD harm not avoided | Title only if supported, Intro contribution 2, Sec. 4.4–4.5, Sec. 6.2/6.5 |
| C3 three-source uncertainty and bounded reliability | TO_VERIFY | Separate response-disagreement, finite-sample and model/transfer observables; one-source ablations; 80/90/95% empirical coverage plus region size; applicable grouped/external shifts | Sources not distinguishable, region miscoverage, external evidence silver-only, or coverage incomparable | Abstract result, Intro contribution 3, Sec. 4.6, Sec. 5.3, Sec. 6.3–6.5, Discussion |
| H1-R archived privileged-teacher development | RETIRED_FROM_ACTIVE_CLAIM_SET_DEVELOPMENT_NOT_PASSED | Frozen Task 30 development package only; formal test absent | Never promote to formal support or formal refutation | Historical boundary and limitations only |

Only `SUPPORTED` and `SUPPORTED_LIMITED` states may produce affirmative result claims. `REFUTED` must remain visible as a negative result if the experiment was pre-registered and scientifically material.

## 4. Section-to-evidence map

| Section | Main job | Claim inputs | Exit test |
|---|---|---|---|
| Title | Name the supported scientific problem, not modules | C2/C3 only if supported | No “first/novel/new”; no unsupported CARM name |
| Abstract | One-paragraph problem–gap–method–evidence–boundary | Final C1–C3 states | Every result traceable; 150–250 words; no citations |
| Introduction | Establish construct, direct prior, reliability gap, RQ, bounded contributions | C1–C3 plan and final states | Contributions match abstract/conclusion |
| Related Work | Position against direct and adjacent work | Citation audit, prior-art matrix | Video2Reaction named closest/direct prior |
| Problem | Freeze estimand and T0 boundary | Protocol v2, data lineage | No target/future ambiguity |
| Method | Define mechanisms and provenance | Task40 frozen method; Task30 only archived boundary | Every module has failure hypothesis/control |
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
| Fig. 2 | Method with training-only response aggregates, posterior and memory paths | C2/C3 mechanism | Frozen architecture/config |
| Fig. 3 | Point versus credible routing and OOF posterior utility construction | C2 mechanism validity | Cross-fitting implementation/tests |
| Fig. 4 | Risk–coverage and prediction-region calibration under shift | C3 reliability | Frozen predictions, five seeds/CI |
| Fig. 5 | Retrieval utility, thinning and negative-transfer analysis | C2 harm avoidance | Neighbor audit and paired outcomes |
| Fig. 6 | OOD and cross-dataset effect summary | C3 boundaries | Pre-registered shift results |
| Table 1 | Dataset roles, constructs, labels, inputs, splits | C1 construct/evidence | Manifests and Data Cards |
| Table 2 | Closest-prior and method-position comparison | Novelty boundary | Citation-verified prior-art matrix |
| Table 3 | Main HUMAN_GOLD results | C2–C3 | Results freeze only |
| Table 4 | Memory/router/posterior ablations and strong controls | C2 | Results freeze only |
| Table 5 | OOD, uncertainty, calibration, selective risk | C3 | Results freeze only |
| Table 6 | Efficiency and reproducibility | Practicality | Run manifests/hardware logs |

If a figure cannot be linked to a claim or audit requirement, it is supplementary or removed.

## 6. Reviewer-attack pre-mortem

| Likely rejection | Evidence-based answer required | Manuscript defense |
|---|---|---|
| “Video2Reaction already proposed the task.” | Direct acknowledgment and protocol-matched comparison | No task-first claim; reliability/OOD question in title and introduction |
| “This is retrieval + uncertainty + router module collage.” | Each component maps to a failure mechanism; posterior router must beat point and generic routers; response thinning and negative-transfer controls | Mechanism-first ablations and negative controls |
| “Comments are not audience emotion.” | Bounded construct, response counts, HUMAN_GOLD/silver separation, selection-bias limits | Construct paragraph and Limitations first-class, not buried |
| “Random splits leak video/comment identity.” | Content-unit grouped splits, duplicate/source audits, physical target-response isolation | E0 and provenance figure |
| “The router is just entropy thresholding.” | Matched-coverage comparison against entropy, similarity, fixed fusion, generic gate, SelectiveNet and point-utility routing | C2 support gate |
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
- posterior, memory, router, rejection, or their combination is a module-level first;
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

- **Archived H1-R:** keep Task 30 as a development non-pass; do not treat it as a formal negative result or restore it to the active method.
- **H2 retrieval helps but credible router fails:** describe point routing or ordinary train-only retrieval; remove “credible net benefit” and negative-transfer-avoidance claims.
- **H2 retrieval fails:** center the evidence on why content similarity does not transfer audience reactions; do not add unplanned modules after test access.
- **H3 has no eligible multimodal protocol:** report `NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL`; do not synthesize missing modalities.
- **C3 fails under shift:** limit claims to in-domain prediction and make the shift failure a principal limitation.
- **Video2Reaction cannot be fairly executed:** provide a complete input/label/split/license/resource/budget non-executability audit; do not omit the direct prior.

## 11. Living-paper update cadence

- **Now through Task 40:** write stable definitions, related-work synthesis, method decisions, and experiment preregistration; leave empirical prose gated.
- **Task 50 active:** ingest only quality-controlled intermediate artifacts into internal tables; keep headline claims provisional.
- **Results freeze:** generate tables/figures, resolve claim states, then write Results, Discussion, Conclusion, and final Abstract.
- **Task 60:** run citation, consistency, integrity, anonymity, reproducibility, and adversarial review passes before generating IEEE LaTeX/Word.
- **After any definition change:** update this blueprint and all mapped manuscript sections in the same batch.

## 12. Submission-quality definition

“Top-journal quality” means that every important statement is precise, falsifiable where applicable, supported at the native statistical unit, comparable under a fair protocol, traceable to an artifact, and bounded by construct, data, license, and domain limitations. It does not mean removing uncertainty or writing as if reviewers cannot disagree.
