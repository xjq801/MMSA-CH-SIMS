---
artifact: T-AFFC manuscript single source of truth
artifact_version: 0.1.0
manuscript_status: MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS
target_venue: IEEE Transactions on Affective Computing
article_type: Original Research Article
language: English
research_ssot: T-AFFC master plan v1.21
claim_source: CLAIM_EVIDENCE_MATRIX.md v1.3
protocol_source: experiment-protocol-v2.md FROZEN_v2
created: 2026-07-31
result_freeze: NOT_AVAILABLE
submission_ready: false
---

# Reliable Content-to-Audience Affect Distribution Forecasting under Unavailable Target Responses and Distribution Shift

> **Living-manuscript notice.** This Markdown file is the authoritative source for the paper text. It is not a submission draft yet. All empirical claims remain unavailable until the corresponding entries in `CLAIM_EVIDENCE_MATRIX.md` are supported by frozen Task 50 evidence. Word, LaTeX, PDF, and supplementary versions must be generated from this file and must not diverge from it.

> **Working-name notice.** “CARM” is an internal working name. It must not enter the final title, abstract, or claimed contribution until the naming and prior-art audit is closed.

## Document-control legend

- `[LOCKED]`: definition or boundary frozen by the research SSOT.
- `[RESULT-GAP:*]`: may be replaced only by a frozen result artifact and statistical audit.
- `[CITATION-GAP:*]`: requires a verified scholarly source; never replace from memory.
- `[DECISION-GAP:*]`: requires a recorded design or editorial decision.
- `[NOT-APPLICABLE:*]`: experiment is structurally inapplicable and must not be presented as a failure.
- `[DROP-IF-UNSUPPORTED:*]`: text or claim must be removed if its evidence gate fails.

## Authors

`[DECISION-GAP:AUTHOR_LIST_AND_ORDER]`

Affiliations, corresponding author, ORCID identifiers, and contribution roles must be frozen before submission. Authorship follows actual scholarly contribution rather than project access, seniority, or tool use.

## Abstract

`[RESULT-GAP:FINAL_ABSTRACT_150_TO_250_WORDS_SINGLE_PARAGRAPH]`

The final abstract must contain, in this order: the construct and practical problem; the reliability gap left by the closest direct prior; the strict T0 setting; the privileged-response teacher, train-only reaction memory, and benefit-aware reliability mechanism at the level actually supported; the two HUMAN_GOLD evaluation roles and the Video2Reaction comparison role; the principal five-seed effect with uncertainty; calibration/selective-risk evidence; and a bounded conclusion. It must be self-contained, contain no citations or undefined abbreviations, and make no task-first, module-first, all-viewer, or unsupported superiority claim.

## Index Terms

Audience reaction forecasting; affect distribution learning; privileged information; retrieval-augmented prediction; selective prediction.

## 1. Introduction

### 1.1 Problem and construct

Digital content can elicit heterogeneous publicly expressed reactions even when the content itself conveys a seemingly unambiguous affective tone. Predicting only a dominant class therefore suppresses disagreement that may be consequential for content analysis, recommendation, and human–AI interaction. We study the prediction of a probability distribution over affective reactions for a previously unseen content item at publication time.

The estimand is deliberately narrow. It is the **publicly expressed induced-reaction distribution among the sampled responders or commenters**, not the latent emotional state of every viewer and not the emotion expressed by the content creator. This distinction is essential because responding is selective, platform-mediated, and only imperfectly related to private affect. `[LOCKED:CONSTRUCT_BOUNDARY]`

### 1.2 What is already known

Prior work has established datasets and models for content-induced emotion, label-distribution learning, and audience-reaction prediction `[CITATION-GAP:INDUCED_AFFECT_AND_LDL]`. Most importantly, Video2Reaction is the closest direct prior: it demonstrates the feasibility of mapping video content to induced audience-reaction distributions and provides a direct benchmark and modeling reference `[CITATION-GAP:VIDEO2REACTION]`. We therefore do not claim to introduce this task, the use of reaction distributions, or content-to-audience forecasting.

### 1.3 The unresolved reliability problem

The remaining question is whether such predictions remain trustworthy when the target item has no observable responses at inference time and differs from the training distribution. Three failure mechanisms make this setting nontrivial. First, response text is highly predictive but unavailable for a new target and can silently leak the label if treated as a test-time input. Second, historical reactions retrieved from superficially similar content can be harmful when similarity does not imply similar audience response. Third, an accurate average prediction may still be overconfident on shifted domains, low-quality inputs, or cases with conflicting historical evidence.

These failures cannot be resolved by reporting a higher score on a random split. They require an information-bound protocol, group-disjoint and out-of-distribution evaluation, train-only provenance for every retrieved neighbor, and reliability measurements that expose when the model should down-weight evidence or abstain.

### 1.4 Research question and approach

This study asks:

> Under a strict publication-time information boundary, can training-only response supervision and historical reaction evidence improve content-to-audience affect distribution forecasting without increasing negative transfer or selective risk under distribution shift?

We investigate a response-privileged teacher that can use training comments, a content-only student that never reads target responses, a reaction memory restricted to training or strictly earlier cases, and a benefit-aware reliability mechanism that estimates whether retrieval is likely to improve over the content-only prediction. The mechanism may fuse, down-weight, or reject retrieved evidence using only publication-time query features, neighbor disagreement, domain or temporal distance, and modality-quality signals. Each component is tied to an observable failure mode and a falsification test rather than being treated as novel by composition.

### 1.5 Contributions

The final contribution list must remain within the master plan’s three contribution families:

1. **Protocol and evidence contribution (C1).** We establish a strict T0 evaluation in which target responses and future interactions are physically isolated, reaction labels are aggregated at the native content-unit level, and retrieval indices contain training or earlier cases only. `[DROP-IF-UNSUPPORTED:C1_REQUIRES_TWO_HUMAN_GOLD_DATASETS_AND_ZERO_BLOCKING_LEAKAGE_FINDINGS]`
2. **Privileged-supervision and benefit-aware memory contribution (internal claims C2–C3).** We test whether training-time response information can improve a content-only student without creating target-response dependence at inference, and whether train-only historical reaction memory with a benefit-aware router reduces retrieval-induced negative transfer relative to ordinary retrieval, fixed fusion, and strong selective baselines. `[RESULT-GAP:C2_FIVE_SEED_EFFECT_AND_CALIBRATION]` `[RESULT-GAP:C3_NEGATIVE_TRANSFER_AND_COVERAGE_MATCHED_EVIDENCE]`
3. **Reliability evidence under shift (internal claim C4).** We evaluate distribution error, calibration, selective risk, and failure modes under group, topic, temporal, platform, cross-dataset, and applicable missing-input shifts. `[RESULT-GAP:C4_OOD_AND_EXTERNAL_VALIDITY]`

At submission, retain only contributions whose claim status is `SUPPORTED` or `SUPPORTED_LIMITED`; a protocol description must not be phrased as empirical superiority.

## 2. Related Work

### 2.1 Content-induced affect and audience-reaction distributions

Synthesize work on induced affect, viewer-response prediction, comment-derived reaction labels, and label-distribution learning. Separate the emotion expressed *in* content from affect induced *by* content and from reactions publicly expressed *about* content. `[CITATION-GAP:INDUCED_AFFECT_AND_LDL]`

Video2Reaction must be presented as the closest direct prior, not as a tangential dataset. Both studies map content to audience-reaction distributions. The distinction is the scientific objective: the present study centers on unavailable target responses, strict information provenance, distribution shift, retrieval harm, calibration, and selective reliability. `[CITATION-GAP:VIDEO2REACTION]`

### 2.2 Learning with privileged response information

Position the response teacher within learning using privileged information, generalized distillation, and privileged multimodal distillation `[CITATION-GAP:LUPI_GD_M2PKD]`. Teacher–student learning and distillation are established techniques; the paper may claim only evidence about their behavior under the present strict T0 construct and datasets.

### 2.3 Historical reaction memory and retrieval-augmented prediction

Review retrieval-augmented affective or multimodal prediction, ordinary nearest-neighbor retrieval, and mechanisms that use related examples when an input modality is incomplete `[CITATION-GAP:RAMER_AND_RETRIEVAL]`. The central distinction to test is not the presence of retrieval but whether a model can anticipate retrieval utility from T0-available evidence and avoid harmful neighbors.

### 2.4 Calibration, uncertainty, and selective prediction

Review probabilistic calibration, selective classification, risk–coverage evaluation, and missing-input reliability `[CITATION-GAP:CALIBRATION_SELECTIVE_MISSING]`. Predictive entropy, response disagreement, retrieval uncertainty, and model uncertainty must not be treated as interchangeable without an explicit estimand and validation.

### 2.5 Positioning summary

| Dimension | Direct audience-reaction forecasting | Privileged learning | Retrieval/selective prediction | This study |
|---|---:|---:|---:|---:|
| Predicts a reaction distribution | Established | Sometimes | Sometimes | Yes |
| Target responses prohibited at inference | Varies | Compatible | Varies | Enforced and audited |
| Historical reaction index is train-only | Not central | Not central | Varies | Enforced and audited |
| Retrieval harm is an explicit estimand | Limited | No | Sometimes | Required |
| Group/OOD calibration and selective risk | Limited/varies | Rare | Established generally | Joint evaluation target |

This table describes research emphases and must be updated after the final citation audit; it is not a universal novelty claim.

## 3. Problem Formulation and Information Boundary

### 3.1 Native content units and reaction distributions

Let \(i\) index a dataset-native content unit: a video, image, or post. Its publication-time content representation is \(x_i\), its admissible static metadata and quality indicators are \(m_i\), and its eligible human responses are \(\{r_{ij}\}_{j=1}^{n_i}\). The empirical target distribution over \(K\) affect categories is

\[
y_{ik}=\frac{1}{n_i}\sum_{j=1}^{n_i}\mathbb{1}(r_{ij}=k), \qquad
\mathbf{y}_i\in\Delta^{K-1}.
\]

The response count \(n_i\) and provenance are retained because empirical distributions with different response counts have different sampling uncertainty. The native content unit, not the individual response or random seed, is the split, resampling, and inferential unit.

### 3.2 Strict T0 prediction

At T0, the model predicts

\[
\hat{\mathbf{y}}_i = f(x_i,m_i;\theta)
\]

before target responses, final engagement, recommendation outcomes, or other post-publication signals are available. Target responses may construct isolated dev/test labels but may never enter model input, retrieval candidates, feature fitting, calibration fitting beyond the designated development protocol, or model selection after test access.

### 3.3 Admissible information

| Information | Train | Dev | Test inference |
|---|---:|---:|---:|
| Publication-time content representation | Yes | Yes | Yes |
| Frozen static metadata/quality indicators | If audited | If audited | If audited |
| Responses of the same target item | Teacher/label construction only | Label construction only | No |
| Responses from training or strictly earlier cases | Memory construction | Retrieval if index remains train-only | Retrieval if index remains train-only |
| Future engagement or future comments | No | No | No |
| Test labels or test-derived selection signals | No | No | No |

Any violation is a blocking protocol failure rather than a performance caveat.

### 3.4 Scope across datasets

CSMV is the primary video mechanism dataset and uses frozen I3D visual sequences; it does not support claims of raw-video end-to-end learning or audio–visual fusion. LAI-GAI is the second HUMAN_GOLD cross-domain image dataset and supports independent distribution, calibration, and OOD evidence but not response-teacher experiments when isomorphic comments are absent. Video2Reaction is evaluated through a fair CSMV adaptation track and a separately reported native silver-label external track. Dataset-specific estimands and label spaces are not pooled merely to increase sample size.

## 4. Method

### 4.1 Overview

The method is organized around four evidence paths:

1. a content-only predictor that defines the deployment baseline;
2. a response-privileged teacher used only during training;
3. a train-only memory containing historical content and reaction summaries;
4. a reliability mechanism that decides whether retrieved evidence should be fused, attenuated, or rejected.

The final architecture figure must encode information provenance, not merely neural modules. Every arrow crossing from responses to the deployed predictor must be labeled “training only,” and every memory item must expose its split and time eligibility.

### 4.2 Content-only student

The student maps admissible content features to a reaction distribution:

\[
\mathbf{p}^{S}_i = \operatorname{softmax}(h_\theta(e_\theta(x_i,m_i))).
\]

Encoder choice, freezing or parameter-efficient adaptation, distribution head, and sequence pooling are frozen before formal test evaluation. `[DECISION-GAP:FINAL_STUDENT_ARCHITECTURE_AND_BUDGET]`

### 4.3 Response-privileged teacher

For training items only, a teacher has access to admissible content and training responses:

\[
\mathbf{p}^{T}_i = g_\phi(x_i,\{r_{ij}\}_{j=1}^{n_i}).
\]

The student objective may combine empirical-distribution supervision and teacher distillation:

\[
\mathcal{L}_{student}
= \mathcal{L}_{dist}(\mathbf{y}_i,\mathbf{p}^{S}_i)
+ \lambda_{KD}\mathcal{L}_{KD}(\mathbf{p}^{T}_i,\mathbf{p}^{S}_i).
\]

`[DECISION-GAP:LOSS_FAMILY_TEMPERATURE_AND_LAMBDA]` The teacher is an upper-bound and supervision mechanism, not a deployable system. A mismatched-response negative control tests whether any gain comes from relevant privileged information rather than extra optimization signal or parameter count.

### 4.4 Train-only audience-reaction memory

The memory contains eligible training cases:

\[
\mathcal{M}_{train}=\{(\mathbf{z}_j,\mathbf{y}_j,\mathbf{q}_j,d_j,t_j)\mid j\in\mathcal{I}_{train}\},
\]

where \(\mathbf{z}_j\) is a content representation, \(\mathbf{q}_j\) records label confidence or response support, \(d_j\) is a domain descriptor, and \(t_j\) is time when available. For temporal protocols, a candidate must additionally satisfy \(t_j<t_i\). Test items, target responses, and post-query outcomes are forbidden from the index.

The retriever returns \(K\) neighbors and an aggregated reaction estimate \(\mathbf{p}^{M}_i\). Retrieval methods include random, lexical, representation nearest-neighbor, and learned variants under a matched candidate pool and budget. `[DECISION-GAP:MEMORY_REPRESENTATION_K_AND_AGGREGATION]`

### 4.5 Benefit-aware reliability routing

The key mechanism hypothesis is that similarity alone is insufficient: retrieval should be used only when it is likely to improve over the content-only prediction. On training data, out-of-fold predictions define a utility target such as

\[
u_i = \ell(\mathbf{y}_i,\mathbf{p}^{S,OOF}_i)
      - \ell(\mathbf{y}_i,\mathbf{p}^{M,OOF}_i),
\]

or its fusion-specific analogue. Positive utility indicates that retrieval reduces loss. Utility targets must be generated by cross-fitting; in-sample or test-derived utility is prohibited.

The router receives only T0-admissible features:

\[
\alpha_i, s_i = \rho_\psi(
\operatorname{sim}_i,\operatorname{disp}_i,
\operatorname{dist}^{domain}_i,\operatorname{dist}^{time}_i,
\operatorname{quality}_i,\operatorname{uncertainty}^{S}_i).
\]

Here \(\alpha_i\) controls fusion and \(s_i\) is a selective score. The predictive distribution is

\[
\hat{\mathbf{y}}_i=(1-\alpha_i)\mathbf{p}^{S}_i+\alpha_i\mathbf{p}^{M}_i,
\]

with optional abstention under a pre-registered coverage or risk budget. `[DECISION-GAP:ROUTER_TARGET_FUSION_AND_ABSTENTION_RULE]`

The router is compared at matched coverage against fixed fusion, similarity thresholds, predictive-entropy thresholds, and a SelectiveNet-style baseline. It supports a method claim only if it identifies harmful retrieval and reduces negative transfer beyond those controls.

### 4.6 Uncertainty and selective outputs

The system outputs a reaction distribution, an uncertainty or disagreement summary whose meaning is explicitly defined, a selective score, and provenance for the retrieved evidence. Calibration and selection are evaluated separately: improved average divergence does not establish calibrated probabilities, and improved coverage–risk performance does not establish population-level psychological validity.

### 4.7 Training and inference

Provide pseudocode with two physically separated phases:

- **Training:** fit content model and teacher; create out-of-fold utility labels; build train-only memory; fit router; freeze all selection and calibration rules.
- **Inference:** encode target content; retrieve only eligible historical cases; compute routing signals; predict or abstain; never read target responses.

`[DECISION-GAP:FINAL_ALGORITHMS_AND_COMPLEXITY]`

## 5. Experimental Design

### 5.1 Research questions

- **RQ1 / C1:** Does the strict T0 protocol yield auditable, leakage-free evidence on two HUMAN_GOLD datasets?
- **RQ2 / C2:** Does response-privileged supervision improve the content-only student’s distribution error or calibration?
- **RQ3 / C3:** Can benefit-aware reaction memory reduce retrieval-induced negative transfer beyond ordinary retrieval and strong routing baselines?
- **RQ4 / C4:** Are any gains maintained under pre-registered distribution shifts and selective-risk evaluation?

### 5.2 Datasets and evidence roles

| Dataset/track | Native unit | Label role | Input role | Eligible claims |
|---|---|---|---|---|
| CSMV/MSA-CRVI | Video | HUMAN_GOLD aggregated comments | Frozen I3D visual sequence; no audio claim | Primary H1/H2 mechanisms, strict T0, video-level OOD |
| LAI-GAI | Image | HUMAN_GOLD individual reactions | Image; prompt/target category excluded by default | Cross-domain distribution, calibration, OOD |
| Video2Reaction A | CSMV video | Same CSMV HUMAN_GOLD label | Same T0 input and budget as CSMV baselines | Fair closest-prior comparison |
| Video2Reaction B | Native movie/video unit | SILVER_LLM_HUMAN_VERIFIED | Publicly recoverable native features only | Limited external validation; separate table |
| NEmo+ | News item/condition | HUMAN responses if access audit passes | Paired text/image/text+image | Optional H4 paired-modality mechanism |
| CUC-IGPE-v2 | Post/video | SILVER or unlabeled stress evidence | Legally recoverable T0 inputs | Chinese/platform stress test only |

Report provenance, licenses, revisions, response counts, exclusions, and fixity in the data statement. The restricted I3D package is internal accepted-risk material and is not redistributable unless rights are independently resolved.

### 5.3 Splits and shift protocols

The principal splits are grouped by native content unit and audited for duplicates, source families, publishers, and target-response overlap. Formal shift protocols include applicable group or movie, topic or hashtag, source or publisher, time, platform, and cross-dataset shifts. A random split may appear only as a diagnostic contrast, never as the primary generalization claim.

### 5.4 Baselines

The baseline suite includes:

1. label-prior, topic-prior, majority, and empirical-distribution predictors;
2. legacy 48-dimensional models with CatBoost, histogram gradient boosting, and LightGBM;
3. official CSMV baselines and the author-released VC-CSA path, with NON_T0 exploratory results excluded from formal evidence;
4. Video2Reaction-style direct fine-tuning and label-distribution learning through the two-track contract;
5. frozen modern content encoders with MLP, late-fusion, and minimal cross-attention heads where inputs are actually available;
6. hard-label, soft-label, ordinary distillation, privileged distillation, and teacher upper-bound controls;
7. no retrieval, random retrieval, lexical retrieval, representation k-nearest neighbors, learned retrieval, and relevant retrieval-augmented affect baselines;
8. fixed fusion, similarity threshold, predictive-entropy threshold, and SelectiveNet-style selective controls.

All trainable baselines use the same split, admissible inputs, evaluator, model-selection rule, and comparable tuning budget.

### 5.5 Ablations and negative controls

| Experiment | Intervention | Failure mechanism tested |
|---|---|---|
| E0 | Leakage and alignment rejection tests | Invalid evidence entering evaluation |
| E1 | Single admissible input vs all available inputs | Unsupported modality-gain claims |
| E2 | Remove memory; vary retriever | Retrieval benefit vs ordinary similarity |
| E3 | Remove teacher/distillation; mismatch responses | Relevant privileged supervision vs extra signal |
| E4 | Remove router/rejection; compare strong selectors | Router mechanism vs thresholding |
| E5 | Applicable natural/random missing input | Graceful degradation |
| E6 | Group/topic/source/time/platform/cross-data shift | Distribution-shift reliability |
| E7 | Random, wrong-domain, low-quality, or reduced memory | Negative transfer and provenance controls |
| E8 | Compatible dominant-class/legacy tasks | Backward comparability without replacing distribution evidence |
| E9 | Parameters, memory, latency, and runtime | Practical cost |

Target-response or future-information injection is not an ablation expected to improve performance; the evaluator must reject it.

### 5.6 Metrics

Jensen–Shannon divergence is the primary distribution metric, accompanied by negative log-likelihood and Earth Mover’s/Wasserstein distance. Dominant-emotion compatibility is reported with Macro-F1 and Balanced Accuracy. Reliability is assessed using Brier score, ECE/ACE, risk–coverage curves, and AURC. Retrieval diagnostics include Recall@K or nDCG@K where relevance is valid, neighbor reaction consistency, retrieval-induced negative-transfer rate, and the proportion of harmful retrievals avoided by the router.

Metric direction, aggregation level, class support, binning choices, and undefined-case handling must be specified before results are viewed.

### 5.7 Statistical analysis

Formal comparisons use at least five random seeds and paired bootstrap 95% confidence intervals at the dataset-native content-unit level. Seeds and responses within one item are not independent sample units. Primary comparisons, multiplicity correction, model-selection rules, coverage targets, and equivalence/noninferiority margins—if used—must be pre-registered. Report effect sizes and uncertainty, not p-values alone.

### 5.8 Implementation and reproducibility

Report software versions, hardware, parameter counts, optimizer, learning-rate schedule, batch size, early stopping, search budget, calibration fitting, memory size, retrieval latency, training time, and peak memory. Every run must have a manifest linking data revision, split, configuration, seed, code commit, prediction file, and metric artifact. `[RESULT-GAP:FINAL_REPRODUCIBILITY_TABLE]`

## 6. Results

> This section is intentionally non-empirical until `results-freeze-v1` exists. Do not insert development-run, single-seed, NON_T0, leakage-accepted exploratory, or test-guided values.

### 6.1 Protocol validity and baseline credibility

`[RESULT-GAP:C1_G1_G2_G3_AND_E0_EVIDENCE]`

Required reporting: dataset-unit counts; excluded items and reasons; all leakage-test outcomes; replay determinism; strongest fair baseline; and limitations of any official-code comparison.

### 6.2 Response-privileged supervision

`[RESULT-GAP:C2_E3_FIVE_SEED_PAIRED_RESULTS]`

Required reporting: content-only, hard/soft label, ordinary distillation, privileged distillation, teacher upper bound, and mismatched-response control; distribution and calibration metrics; effect sizes with native-unit confidence intervals.

### 6.3 Reaction memory and benefit-aware routing

`[RESULT-GAP:C3_E2_E4_E7_FIVE_SEED_PAIRED_RESULTS]`

Required reporting: no/random/lexical/nearest-neighbor/learned retrieval; fixed and adaptive fusion; matched-coverage selective controls; utility-prediction quality; negative-transfer rate; harmful-retrieval avoidance; and failure cases.

### 6.4 Distribution shift and external validity

`[RESULT-GAP:C4_E5_E6_VIDEO2REACTION_DUAL_TRACK]`

Report every pre-registered shift, including negative findings. CSMV, LAI-GAI, and Video2Reaction-native metrics must remain in dataset-specific tables. A result on silver labels cannot be used to upgrade a HUMAN_GOLD claim.

### 6.5 Calibration and selective prediction

`[RESULT-GAP:C3_C4_CALIBRATION_AND_RISK_COVERAGE]`

Required reporting: full-coverage calibration, coverage-matched risk, AURC, operating points chosen without test labels, and whether abstention concentrates on shifted, low-quality, or high-disagreement cases.

### 6.6 Efficiency and sensitivity

`[RESULT-GAP:E9_AND_PRE_REGISTERED_SENSITIVITY]`

Report parameter count, peak memory, runtime, index size, retrieval latency, and sensitivity to memory size, neighbor count, sequence pooling, and other pre-registered choices.

### 6.7 Main result table shell

| Claim | Primary comparison | Dataset/protocol | Effect and 95% CI | Claim status | Evidence artifact |
|---|---|---|---|---|---|
| C1 | Protocol/evaluator validity | Two HUMAN_GOLD datasets | `[RESULT-GAP]` | TO_VERIFY | `[RESULT-GAP]` |
| C2 | Privileged student vs strongest content-only | CSMV strict T0 | `[RESULT-GAP]` | TO_VERIFY | `[RESULT-GAP]` |
| C3 | Routed memory vs strongest retrieval/selective control | CSMV strict T0 + shifts | `[RESULT-GAP]` | TO_VERIFY | `[RESULT-GAP]` |
| C4 | Best supported model vs strongest fair baseline | Pre-registered OOD/external tracks | `[RESULT-GAP]` | TO_VERIFY | `[RESULT-GAP]` |

## 7. Discussion

### 7.1 Answer to the research question

`[RESULT-GAP:DISCUSSION_BOUND_TO_SUPPORTED_CLAIMS]`

The discussion must answer whether privileged responses, historical reaction evidence, and selective routing improve reliability under the tested information boundary. It must distinguish average predictive improvement, calibration improvement, negative-transfer reduction, and selective-risk improvement.

### 7.2 Mechanistic interpretation

`[RESULT-GAP:MECHANISM_INTERPRETATION_FROM_ABLATIONS_AND_NEGATIVE_CONTROLS]`

Interpret the router only if utility labels, strong controls, coverage matching, and pollution tests support the mechanism. If retrieval improves average performance but the router does not identify harmful cases, describe the method as ordinary retrieval fusion rather than benefit-aware reliability.

### 7.3 Relationship to Video2Reaction and other direct work

`[RESULT-GAP:FAIR_CLOSEST_PRIOR_COMPARISON]`

State the shared task and report protocol-matched evidence. Differences in datasets, labels, recoverable inputs, or budgets must be made explicit. Do not use a native Video2Reaction score as an absolute comparison with CSMV.

### 7.4 Scientific and practical implications

`[RESULT-GAP:BOUNDED_IMPLICATIONS]`

Any implication must be limited to publicly expressed reactions within the evaluated sampling and platform conditions. The system must not be framed as a detector of private mental states or as an unconditional audience-surveillance tool.

### 7.5 Negative and null findings

`[RESULT-GAP:NULL_AND_ADVERSE_RESULTS]`

Report where privileged supervision, memory, routing, or rejection does not help. A null H1, H2, or H3 result triggers the predefined claim downgrade and should be interpreted as evidence about protocol or failure mechanisms, not hidden through selective reporting.

## 8. Limitations and Broader Considerations

1. **Construct validity.** Public comments or elicited responses are an observable sample of expressed reactions, not all viewers’ latent affect.
2. **Selection and platform bias.** Who responds, which responses remain visible, and how a platform ranks content may distort empirical distributions.
3. **Label uncertainty.** Reaction distributions have finite and unequal response counts; silver labels remain distinct from HUMAN_GOLD evidence.
4. **Input and domain scope.** CSMV supports frozen I3D visual representations rather than raw-video or audio–visual claims; LAI-GAI is an image-domain validation set.
5. **Shift coverage.** Tested shifts cannot establish robustness to every future platform, culture, event, or moderation regime.
6. **Retrieval risks.** Similar historical content may carry misleading reaction patterns, spurious domain cues, or privacy-sensitive provenance.
7. **Selective prediction.** Abstention changes coverage and may disproportionately exclude difficult domains; risk–coverage trade-offs must be reported, not concealed.
8. **Asset admissibility.** The fixed I3D package has unresolved external license/revision/rightsholder fixity and is used only under an accepted internal-research risk; it is not redistributed or described as officially authorized.
9. **Reproducibility boundary.** Restricted content or comments may require manifests, access instructions, and processing code rather than redistribution.
10. **Generalization of evidence.** Findings support the exact datasets, constructs, label mappings, and protocols tested; they do not establish psychological ground truth for the general population.

## 9. Conclusion

`[RESULT-GAP:CONCLUSION_CONTAINING_ONLY_SUPPORTED_C1_TO_C4]`

The conclusion must restate the reliability question, summarize only supported evidence, identify the conditions under which retrieval or abstention is beneficial, and preserve the construct and asset boundaries. It must introduce no new result, method, dataset, or claim.

## Data Availability

`[DECISION-GAP:FINAL_DATA_AVAILABILITY_STATEMENT]`

The statement must list each dataset’s access route, revision/fixity evidence, redistributable artifacts, restricted artifacts, and reasons for restrictions. It must distinguish public manifests and splits from raw media, comments, fixed I3D features, and private platform material.

## Code Availability

`[DECISION-GAP:ANONYMIZED_REPOSITORY_RELEASE_AND_ARCHIVAL_PLAN]`

At minimum, release eligible split manifests, schemas, evaluation code, configuration files, environment specification, and scripts that regenerate every reported table and figure, subject to licensing and anonymity constraints.

## Ethics, Privacy, and Responsible Use

`[DECISION-GAP:FINAL_ETHICS_AND_PRIVACY_STATEMENT]`

Describe data origin, consent or public-data rationale where applicable, platform terms, de-identification, non-redistributable response text, potential harms of profiling, and safeguards against interpreting predictions as private mental states.

## Author Contributions

`[DECISION-GAP:CREDIT_TAXONOMY_STATEMENT]`

## Conflict of Interest

`[DECISION-GAP:CONFLICT_OF_INTEREST_STATEMENT]`

## Funding

`[DECISION-GAP:FUNDING_STATEMENT]`

## Acknowledgments

`[DECISION-GAP:ACKNOWLEDGMENTS_WITHOUT_COMPROMISING_REVIEW_ANONYMITY]`

## Generative AI and Automated-Tool Disclosure

`[DECISION-GAP:VENUE_COMPLIANT_AI_DISCLOSURE]`

The final disclosure must identify permitted uses of language or coding assistants, material human verification, and the fact that authors remain responsible for accuracy, originality, citations, data, code, and conclusions. Automated tools are not authors.

## References

`[CITATION-GAP:VERIFIED_IEEE_STYLE_REFERENCE_LIST]`

Every reference must pass identifier and claim-support verification. Author-reported venue status must not be upgraded to an archival publication without an official proceedings record.

## Supplementary-Material Plan

- S1. Dataset lineage, license, and fixity tables.
- S2. Split construction and leakage audits.
- S3. Full hyperparameter spaces and model-selection rules.
- S4. Complete five-seed results and native-unit bootstrap intervals.
- S5. Calibration, risk–coverage, and operating-point details.
- S6. Retrieval provenance, pollution controls, and negative-transfer cases.
- S7. Additional OOD, missing-input, and sensitivity results.
- S8. Efficiency, compute, and environmental reporting.
- S9. Reproducibility checklist and artifact manifest.
- S10. Ethics, privacy, data-access, and AI-use disclosures.

## Internal submission gate

This manuscript cannot be marked `SUBMISSION_READY` until all of the following are true:

- C1–C4 have final states with linked evidence; unsupported claims are removed or downgraded.
- G6 and all T-AFFC Go standards have independently passed.
- The two HUMAN_GOLD datasets remain the basis of the principal quantitative claims.
- Video2Reaction has a fair comparison or an accepted, detailed non-executability audit.
- Five-seed, native-content-unit uncertainty, calibration, efficiency, and failure analyses are frozen.
- All `[RESULT-GAP]`, material `[CITATION-GAP]`, and submission-critical `[DECISION-GAP]` markers are resolved.
- Claim-blacklist, citation, consistency, integrity, anonymity, and reproducibility audits pass.
- The current official IEEE T-AFFC author instructions and template are rechecked at submission time.
