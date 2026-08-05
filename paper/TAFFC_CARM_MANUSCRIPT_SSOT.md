---
artifact: T-AFFC manuscript single source of truth
artifact_version: 0.1.3
manuscript_status: MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS
target_venue: IEEE Transactions on Affective Computing
article_type: Original Research Article
language: English
research_ssot: T-AFFC master plan v1.23
claim_source: CLAIM_EVIDENCE_MATRIX.md v1.4
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

The final abstract must contain, in this order: the construct and practical problem; the reliability gap left by the closest direct prior; the strict T0 setting; train-only reaction memory, finite-response posterior net benefit, and the benefit-aware reliability mechanism at the level actually supported; the two HUMAN_GOLD evaluation roles and the Video2Reaction comparison role; the principal five-seed effect with uncertainty; calibration/selective-risk evidence; and a bounded conclusion. It must be self-contained, contain no citations or undefined abbreviations, and make no task-first, module-first, all-viewer, causal, or unsupported superiority claim.

## Index Terms

Audience reaction forecasting; affect distribution learning; retrieval-augmented prediction; uncertainty quantification; selective prediction.

## 1. Introduction

### 1.1 Problem and construct

Digital content can elicit heterogeneous publicly expressed reactions even when the content itself conveys a seemingly unambiguous affective tone. Predicting only a dominant class therefore suppresses disagreement that may be consequential for content analysis, recommendation, and human–AI interaction. We study the prediction of a probability distribution over affective reactions for a previously unseen content item at publication time.

The estimand is deliberately narrow. It is the **publicly expressed induced-reaction distribution among the sampled responders or commenters**, not the latent emotional state of every viewer and not the emotion expressed by the content creator. This distinction is essential because responding is selective, platform-mediated, and only imperfectly related to private affect. `[LOCKED:CONSTRUCT_BOUNDARY]`

Operationally, each target is a dataset-native content unit paired with a finite set of eligible human responses. CSMV aggregates human-labeled comments within a video, whereas LAI-GAI aggregates consenting participants' induced-affect ratings within an image. The resulting distribution therefore describes the observed response sample under the dataset's collection and eligibility rules. It is neither a population-prevalence estimate nor evidence that non-responding viewers experienced the same affect. Response counts and within-item uncertainty are retained so that unequal support is visible rather than absorbed into a single hard label.

### 1.2 What is already known

Prior work has established datasets and models for content-induced emotion, label-distribution learning, and audience-reaction prediction `[CITATION-GAP:INDUCED_AFFECT_AND_LDL]`. Most importantly, Video2Reaction is the closest direct prior: it demonstrates the feasibility of mapping video content to induced audience-reaction distributions and provides a direct benchmark and modeling reference `[CITATION-GAP:VIDEO2REACTION]`. We therefore do not claim to introduce this task, the use of reaction distributions, or content-to-audience forecasting.

### 1.3 The unresolved reliability problem

The remaining question is whether such predictions remain trustworthy when the target item has no observable responses at inference time and differs from the training distribution. Three failure mechanisms make this setting nontrivial. First, response text is highly predictive but unavailable for a new target and can silently leak the label if treated as a test-time input. Second, historical reactions retrieved from superficially similar content can be harmful when similarity does not imply similar audience response. Third, an accurate average prediction may still be overconfident on shifted domains, low-quality inputs, or cases with conflicting historical evidence.

These failures cannot be resolved by reporting a higher score on a random split. They require an information-bound protocol, group-disjoint and out-of-distribution evaluation, train-only provenance for every retrieved neighbor, and reliability measurements that expose when the model should down-weight evidence or abstain.

### 1.4 Research question and approach

This study asks:

> Under a strict publication-time information boundary, can a model determine when train-only historical reaction evidence has credible net benefit, and otherwise fall back or abstain without increasing negative transfer under distribution shift?

We investigate a content-only predictor that never reads target responses, a reaction memory restricted to training or strictly earlier cases, and a benefit-aware mechanism that estimates both point and posterior net benefit relative to content-only prediction. The mechanism uses publication-time query features, neighbor disagreement, response support, domain distance, and model diagnostics to choose among using memory, falling back to content-only prediction, and abstaining. Each component is tied to an observable failure mode and a falsification test rather than being treated as novel by composition.

### 1.5 Contributions

The final contribution list must remain within the master plan’s three contribution families:

1. **Protocol and evidence contribution (C1).** We establish a strict T0 evaluation in which target responses and future interactions are physically isolated, reaction labels are aggregated at the native content-unit level, and retrieval indices contain training or earlier cases only. `[DROP-IF-UNSUPPORTED:C1_REQUIRES_TWO_HUMAN_GOLD_DATASETS_AND_ZERO_BLOCKING_LEAKAGE_FINDINGS]`
2. **Credible net-benefit memory contribution (C2).** We test whether train-only historical reaction memory with out-of-fold point and finite-response posterior benefit targets reduces retrieval-induced negative transfer relative to ordinary retrieval, fixed fusion, point-utility routing, and strong selective baselines. `[RESULT-GAP:C2_CREDIBLE_NET_BENEFIT_AND_COVERAGE_MATCHED_EVIDENCE]`
3. **Uncertainty and reliability evidence under shift (C3).** We evaluate response disagreement, finite-sample target uncertainty, model or transfer uncertainty, calibrated empirical-distribution prediction regions, selective risk, and failure modes under the applicable pre-registered shifts. `[RESULT-GAP:C3_UNCERTAINTY_OOD_AND_EXTERNAL_VALIDITY]`

At submission, retain only contributions whose claim status is `SUPPORTED` or `SUPPORTED_LIMITED`; a protocol description must not be phrased as empirical superiority.

## 2. Related Work

### 2.1 Content-induced affect and audience-reaction distributions

Synthesize work on induced affect, viewer-response prediction, comment-derived reaction labels, and label-distribution learning. Separate the emotion expressed *in* content from affect induced *by* content and from reactions publicly expressed *about* content. `[CITATION-GAP:INDUCED_AFFECT_AND_LDL]`

Video2Reaction must be presented as the closest direct prior, not as a tangential dataset. Both studies map content to audience-reaction distributions. The distinction is the scientific objective: the present study centers on unavailable target responses, strict information provenance, distribution shift, retrieval harm, calibration, and selective reliability. `[CITATION-GAP:VIDEO2REACTION]`

### 2.2 Learning from finite response distributions

Review label-distribution learning, ambiguous-label modeling, Dirichlet-multinomial uncertainty, and finite-annotator or finite-response estimation `[CITATION-GAP:FINITE_RESPONSE_DISTRIBUTION_UNCERTAINTY]`. A posterior over an empirical response target is a measurement model, not evidence that the latent affect of all viewers has been identified.

### 2.3 Historical reaction memory and retrieval-augmented prediction

Review retrieval-augmented affective or multimodal prediction, ordinary nearest-neighbor retrieval, and mechanisms that use related examples when an input modality is incomplete `[CITATION-GAP:RAMER_AND_RETRIEVAL]`. The central distinction to test is not the presence of retrieval but whether a model can anticipate retrieval utility from T0-available evidence and avoid harmful neighbors.

### 2.4 Calibration, uncertainty, and selective prediction

Review probabilistic calibration, selective classification, risk–coverage evaluation, and missing-input reliability `[CITATION-GAP:CALIBRATION_SELECTIVE_MISSING]`. Predictive entropy, response disagreement, retrieval uncertainty, and model uncertainty must not be treated as interchangeable without an explicit estimand and validation.

### 2.5 Positioning summary

| Dimension | Direct audience-reaction forecasting | Finite-response modeling | Retrieval/selective prediction | This study |
|---|---:|---:|---:|---:|
| Predicts a reaction distribution | Established | Sometimes | Sometimes | Yes |
| Target responses prohibited at inference | Varies | Compatible | Varies | Enforced and audited |
| Historical reaction index is train-only | Not central | Not central | Varies | Enforced and audited |
| Retrieval harm is an explicit estimand | Limited | No | Sometimes | Required |
| Group/OOD calibration and selective risk | Limited/varies | Rare | Established generally | Joint evaluation target |

This table describes research emphases and must be updated after the final citation audit; it is not a universal novelty claim.

## 3. Problem Formulation and Information Boundary

### 3.1 Native content units and reaction distributions

Let \(i\) index a dataset-native content unit: a video, image, or post. Its publication-time content representation is \(x_i\), its admissible static metadata and quality indicators are \(m_i\), and its eligible human responses are \(\{r_{ij}\}_{j=1}^{n_i}\). For a dataset with categorical response labels, the empirical target distribution over \(K\) affect categories is

\[
y_{ik}=\frac{1}{n_i}\sum_{j=1}^{n_i}\mathbb{1}(r_{ij}=k), \qquad
\mathbf{y}_i\in\Delta^{K-1}.
\]

For an induced-rating dataset, the canonical map is defined by that dataset rather than forced through the categorical estimator. In LAI-GAI, the eligible 1--7 ratings are averaged separately for each of 12 induced-affect dimensions, the scale floor is removed, and the resulting nonnegative vector is normalized:

\[
\bar{a}_{ik}=\frac{1}{n_{ik}}\sum_j a_{ijk},\qquad
y_{ik}=\frac{\max(\bar{a}_{ik}-1,0)}{\sum_{k'=1}^{K}\max(\bar{a}_{ik'}-1,0)}.
\]

The per-item response count, per-dimension support, sample standard deviation, standard error, response histogram, and provenance are retained because empirical distributions with different response support have different uncertainty. Dataset-specific label spaces are not pooled. The native content unit, not the individual response, rater, fold, or random seed, is the split, resampling, and inferential unit.

### 3.2 Strict T0 prediction

At T0, the model predicts

\[
\hat{\mathbf{y}}_i = f(x_i,m_i;\theta)
\]

before target responses, final engagement, recommendation outcomes, or other post-publication signals are available. Target responses may construct isolated dev/test labels but may never enter model input, retrieval candidates, feature fitting, calibration fitting beyond the designated development protocol, or model selection after test access.

The optional \(T+\Delta\) early-response task is disabled unless publication times, response timestamps, and a reproducible observation window are independently recovered and frozen. It requires separate fields, splits, configurations, and result tables; it cannot be inferred from file order or mixed with T0 evidence. The current CSMV release has no publication-time protocol, so no chronological-safety claim is made.

### 3.3 Admissible information

| Information | Train | Dev | Test inference |
|---|---:|---:|---:|
| Publication-time content representation | Yes | Yes | Yes |
| Frozen static metadata/quality indicators | If audited | If audited | If audited |
| Responses of the same target item | Training target/posterior construction only | Label construction only | No |
| Responses from training or strictly earlier cases | Memory construction | Retrieval if index remains train-only | Retrieval if index remains train-only |
| Future engagement or future comments | No | No | No |
| Test labels or test-derived selection signals | No | No | No |

Any violation is a blocking protocol failure rather than a performance caveat.

The information boundary is also physical. `HUMAN_GOLD`, `SILVER`, and `UNLABELED` records have separate manifests and loading entry points. Test responses remain label-side artifacts and are unavailable to the student, feature fitting, model selection, and retrieval index. Indices are created only after splitting and may contain training items only; if a future protocol uses time, every candidate must additionally predate its query. A failed ID, source-family, target-response, future-field, fit-scope, or index-membership check marks the run `LEAKAGE_BLOCKED` and makes it ineligible for the manuscript.

### 3.4 Scope across datasets

CSMV is the primary video mechanism dataset: 107,267 human-labeled comments are aggregated over 8,210 video IDs, and the admissible model input is the fixed `float32[T,1024]` I3D visual sequence. It does not support claims of raw-video end-to-end learning, original-frame training, audio--visual fusion, audio gains, or target-comment input. LAI-GAI is the second HUMAN_GOLD cross-domain image dataset: 63,682 eligible human response rows are aggregated over 847 images into a 12-dimensional induced-affect distribution. Its prompt and target generation category are provenance, not truth, and are excluded from the default input. LAI-GAI supports independent distribution, marginal finite-response, calibration, and OOD evidence but not reaction-memory routing when isomorphic response-history fields are absent. Video2Reaction is evaluated through a fair CSMV adaptation track and a separately reported native `SILVER_LLM_HUMAN_VERIFIED` external track. Dataset-specific estimands, input contracts, statistical units, and label spaces are not pooled merely to increase sample size or to compare absolute metric values across datasets.

## 4. Method

### 4.1 Overview

The method is organized around four evidence paths:

1. a content-only predictor that defines the deployment baseline;
2. a finite-response posterior that represents uncertainty in the observed target distribution;
3. a train-only memory containing historical content and reaction summaries;
4. a reliability mechanism that decides whether retrieved evidence should be used, rejected in favor of content-only prediction, or abstained from.

The final architecture figure must encode information provenance, not merely neural modules. Every arrow crossing from response aggregates to training targets or memory must be labeled “training only,” and every memory item must expose its split and time eligibility. The deployed model never reads target responses.

### 4.2 Content-only expert

The content-only expert maps admissible content features to a reaction distribution:

\[
\mathbf{p}^{S}_i = \operatorname{softmax}(h_\theta(e_\theta(x_i,m_i))).
\]

Encoder choice, freezing or parameter-efficient adaptation, distribution head, and sequence pooling are frozen before formal test evaluation. `[DECISION-GAP:FINAL_STUDENT_ARCHITECTURE_AND_BUDGET]`

### 4.3 Finite-response posterior target

For a categorical response-count vector \(\mathbf{c}_i\), the development contract uses a symmetric Jeffreys prior:

\[
\boldsymbol{\theta}_i\mid\mathbf{c}_i\sim
\operatorname{Dirichlet}(\mathbf{c}_i+0.5).
\]

A uniform-prior sensitivity analysis replaces 0.5 with 1. The posterior represents uncertainty caused by the finite observed response sample; it is not a posterior for all viewers. CSMV supports exact reconstruction of integer category counts from its frozen aggregate distribution and response support. LAI-GAI preserves only per-dimension marginal histograms in the canonical artifact, so it supports marginal response thinning but not reconstruction of joint 12-dimensional respondent vectors.

### 4.4 Train-only audience-reaction memory

The memory contains eligible training cases:

\[
\mathcal{M}_{train}=\{(\mathbf{z}_j,\mathbf{y}_j,\mathbf{q}_j,d_j,t_j)\mid j\in\mathcal{I}_{train}\},
\]

where \(\mathbf{z}_j\) is a content representation, \(\mathbf{q}_j\) records label confidence or response support, \(d_j\) is a domain descriptor, and \(t_j\) is time when available. For temporal protocols, a candidate must additionally satisfy \(t_j<t_i\). Test items, target responses, and post-query outcomes are forbidden from the index.

The retriever returns \(K\) neighbors and an aggregated reaction estimate \(\mathbf{p}^{M}_i\). Retrieval methods include random, lexical, representation nearest-neighbor, and learned variants under a matched candidate pool and budget. `[DECISION-GAP:MEMORY_REPRESENTATION_K_AND_AGGREGATION]`

### 4.5 Point and credible net-benefit routing

The key mechanism hypothesis is that similarity alone is insufficient: retrieval should be used only when it is likely to improve over the content-only prediction. On training data, out-of-fold predictions define a utility target such as

\[
u_i = \ell(\mathbf{y}_i,\mathbf{p}^{S,OOF}_i)
      - \ell(\mathbf{y}_i,\mathbf{p}^{M,OOF}_i),
\]

or its fusion-specific analogue. Positive utility indicates that retrieval reduces loss. Utility targets must be generated by five-fold group cross-fitting; in-sample or test-derived utility is prohibited.

For posterior draws \(\boldsymbol{\theta}^{(s)}_i\), define \(u_i^{(s)}\) by replacing the empirical target with the draw, then compute

\[
b_i=\Pr(u_i>0\mid\mathbf{c}_i),\qquad
\ell_i=Q_{0.05}(u_i\mid\mathbf{c}_i).
\]

The point router predicts expected utility. The credible router uses \(b_i\) or \(\ell_i\) and may choose memory only when improvement remains credible after finite-response uncertainty. Their architecture, inputs, candidate pool, optimization budget, and coverage are matched.

The router receives only T0-admissible features:

\[
\alpha_i, s_i = \rho_\psi(
\operatorname{sim}_i,\operatorname{disp}_i,
\operatorname{dist}^{domain}_i,\operatorname{dist}^{time}_i,
\operatorname{quality}_i,\operatorname{uncertainty}^{S}_i).
\]

Here \(\alpha_i\) controls fusion and \(s_i\) is a selective score. The action set is frozen as `USE_MEMORY`, `FALLBACK_CONTENT`, and `ABSTAIN`. The predictive distribution when memory is used is

\[
\hat{\mathbf{y}}_i=(1-\alpha_i)\mathbf{p}^{S}_i+\alpha_i\mathbf{p}^{M}_i,
\]

with optional abstention under a pre-registered coverage or risk budget. `[DECISION-GAP:ROUTER_TARGET_FUSION_AND_ABSTENTION_RULE]`

The router is compared at matched coverage against fixed fusion, similarity thresholds, predictive-entropy thresholds, out-of-domain diagnostics, generic learned gates, a SelectiveNet-style baseline, and the point-utility router. It supports a method claim only if it identifies harmful retrieval and reduces negative transfer beyond those controls.

### 4.6 Uncertainty and selective outputs

The system outputs a reaction distribution, three separately validated diagnostics, a selective score, and provenance for the retrieved evidence. Group disagreement is checked against held-out or split-half responses; finite-sample uncertainty is checked by response thinning and posterior sensitivity; model or transfer uncertainty is checked against ensemble disagreement and natural group-held-out error. A development calibration subset defines empirical-distribution prediction regions at 80%, 90%, and 95% target coverage. Region coverage and size are reported together and do not establish population-level psychological validity.

### 4.7 Training and inference

Provide pseudocode with two physically separated phases:

- **Training:** fit the content expert; create out-of-fold point and posterior utility targets; build train-only memory; fit point and credible routers; freeze all selection and calibration rules.
- **Inference:** encode target content; retrieve only eligible historical cases; compute routing signals; predict or abstain; never read target responses.

`[DECISION-GAP:FINAL_ALGORITHMS_AND_COMPLEXITY]`

## 5. Experimental Design

### 5.1 Research questions

- **RQ1 / C1:** Does the strict T0 protocol yield auditable, leakage-free evidence on two HUMAN_GOLD datasets?
- **RQ2 / C2:** Can posterior-aware net-benefit routing reduce retrieval-induced negative transfer beyond point-utility routing and strong generic selectors?
- **RQ3 / C3:** Do separately validated response, finite-sample, and model/transfer uncertainty support calibrated empirical-distribution prediction regions and selective reliability under applicable shifts?

### 5.2 Datasets and evidence roles

| Dataset/track | Native unit | Label role | Input role | Eligible claims |
|---|---|---|---|---|
| CSMV/MSA-CRVI | 8,210 videos | HUMAN_GOLD distribution aggregated from 107,267 human-labeled comments; integer category counts are exactly reconstructable from aggregate labels and support | Frozen `float32[T,1024]` I3D visual sequence; no audio or target-comment input | Primary H2a/H2b mechanisms, finite-response posterior, strict T0, video-level OOD |
| LAI-GAI | 847 images | HUMAN_GOLD 12-dimensional distribution aggregated from 63,682 eligible induced-rating rows; marginal response histograms retained | Image; generation prompt and target category excluded by default | Group/sample uncertainty, marginal response thinning, calibration and OOD; reaction-memory routing not applicable by design |
| Video2Reaction A | CSMV video | Same CSMV HUMAN_GOLD label | Same T0 input and budget as CSMV baselines | Fair closest-prior comparison |
| Video2Reaction B | Native movie/video unit | SILVER_LLM_HUMAN_VERIFIED | Publicly recoverable native features only | Limited external validation; separate table |
| NEmo+ | News item/condition | HUMAN responses if access audit passes | Paired text/image/text+image | Optional H4 paired-modality mechanism |
| CUC-IGPE-v2 | Post/video | SILVER or unlabeled stress evidence | Legally recoverable T0 inputs | Chinese/platform stress test only |

CSMV and LAI-GAI are the two principal HUMAN_GOLD evidence sources, but they play different roles and are not described as two video datasets. The CSMV annotation layer is documented separately from code, platform media, and feature assets; the annotation license cannot be extended to TikTok media or I3D features. LAI-GAI's image/metadata and rating components are documented as CC BY 4.0 in the frozen source ledger. Video2Reaction-native labels remain silver despite human quality checks, and CUC-IGPE-v2 remains silver or unlabeled stress evidence. Report provenance, license layer, revision, response counts, exclusions, and fixity separately for every source. The fixed I3D package is internal accepted-risk material and is not redistributable unless rights are independently resolved.

### 5.3 Splits and shift protocols

The principal splits are created before fitting or indexing and are grouped by dataset-native content and known source families. For CSMV, 8,210 internal video IDs are collapsed to 8,008 source-video families before assignment. The formal `group_by_video_v1` split contains 5,698/837/1,675 train/development/test videos; the stricter source-family-plus-hashtag-component split contains 7,211/327/672. CSMV has no released publication timestamps or native topic field, so a chronological split and a native topic-held-out split are not claimed. Publisher grouping is likewise unavailable rather than presumed safe.

For LAI-GAI, source item, cultural/age/sex variants, identical prompts, exact-image hashes, and perceptual near duplicates are merged into 379 groups before the frozen 594/127/126 image split. These grouping rules keep known exact and near-duplicate relations within a split. The automated M2 gate reports zero blocking findings for ID and source-group intersections, same-video comment grouping, prohibited target/future fields, fit scope, and the current train-only-index contract. The index and time checks are presently `PASS_NOT_BUILT` and `NOT_APPLICABLE_NO_TIME_SPLIT`, respectively; neither status proves a future index or temporal protocol safe. Formal shift protocols may include only applicable group or movie, hashtag, source or publisher, time, platform, and cross-dataset shifts after their own pre-registration and audit. A random split may appear only as a diagnostic contrast, never as the primary generalization claim.

### 5.4 Baselines

The planned baseline suite includes:

1. label-prior, topic-prior, majority, and empirical-distribution predictors;
2. legacy 48-dimensional models with CatBoost, histogram gradient boosting, and LightGBM;
3. official CSMV baselines and the author-released VC-CSA path, with NON_T0 exploratory results excluded from formal evidence;
4. Video2Reaction-style direct fine-tuning and label-distribution learning through the two-track contract;
5. frozen modern content encoders with MLP, late-fusion, and minimal cross-attention heads where inputs are actually available;
6. content-only, memory-only, fixed-fusion, and oracle-selection development references;
7. no retrieval, random retrieval, lexical retrieval, representation k-nearest neighbors, learned retrieval, and relevant retrieval-augmented affect baselines;
8. similarity, predictive-entropy, OOD, generic learned, SelectiveNet-style, point-utility, and credible-net-benefit selectors.

The current Task 20 evidence distinguishes four baseline identities rather than treating every executed program as a comparable result. `OFFICIAL_REPRODUCTION_ATTEMPT` denotes an attempt to execute an official or author-released path under its native contract; it does not imply a successful or T0-compatible reproduction. The historical VC-CSA attempt against the former official main branch was superseded by the post-snapshot erratum after an author implementation was located. That implementation consumes target comments and uses a comment-level split, so its author-setting path is `AUTHOR_ORIGINAL_SETTING_NON_T0`; the later 120-epoch run remains leakage-accepted NON_T0 exploratory evidence and is permanently ineligible for formal tables, model selection, G3 evidence, or paper claims. No VC-CSA performance value is reported here.

`REIMPLEMENTATION_STRONG_BASELINE` denotes the frozen-I3D temporal-attention implementation evaluated through the common Task 20 contract. It is the only Task 20 strong content-only baseline with a formal single-seed engineering run, and that run is not five-seed inferential evidence. `LEGACY_NATIVE_COMPATIBILITY` denotes the re-executed 48-dimensional CatBoost, histogram-gradient-boosting, and LightGBM pipelines on their native silver binary task; these runs preserve backward compatibility but are not comparable to the T0 distribution-forecasting endpoint. `REFERENCE_MODEL` denotes an architecture named for contextual comparison but unavailable under the frozen input contract: CLIP, SigLIP, and VideoMAE features are `NOT_AVAILABLE_IN_FROZEN_T0_PROTOCOL`. Because only one T0 content modality was available, late fusion, minimal cross-attention, and E1 modality-increment tests are `NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY`, not failed or omitted experiments.

All formally comparable trainable baselines must use the same split, admissible inputs, evaluator, model-selection rule, and 12-trial maximum tuning budget. Task 30 privileged-teacher development is an archived negative boundary and is not an active baseline family or formal result. Memory, retrieval, router, and rejection development belongs to Task 40; formal five-seed comparisons and paired native-unit uncertainty remain Task 50 work. `[RESULT-GAP:FORMAL_BASELINE_TABLE_WITH_FIVE_SEED_UNCERTAINTY]`

### 5.5 Ablations and negative controls

| Experiment | Intervention | Failure mechanism tested |
|---|---|---|
| E0 | Leakage and alignment rejection tests | Invalid evidence entering evaluation |
| E1 | Single admissible input vs all available inputs | Unsupported modality-gain claims |
| E2 | Content–reaction mismatch, oracle headroom, then vary retriever | Whether selectable memory benefit exists before routing |
| E3 | Archived Task 30 teacher boundary; no active formal experiment | Prevent retired privileged-supervision results from entering claims |
| E4 | Point vs credible benefit targets; remove router/rejection; compare strong selectors | Posterior-aware harm avoidance vs point estimates or thresholding |
| E5 | Applicable natural/random missing input | Graceful degradation |
| E6 | Group/topic/source/time/platform/cross-data shift | Distribution-shift reliability |
| E7 | Random, wrong-domain, low-quality, or reduced memory | Negative transfer and provenance controls |
| E8 | Compatible dominant-class/legacy tasks | Backward comparability without replacing distribution evidence |
| E9 | Parameters, memory, latency, and runtime | Practical cost |

Target-response or future-information injection is not an ablation expected to improve performance; the evaluator must reject it.

### 5.6 Metrics

The frozen evaluator reports nine video-level metrics. Jensen–Shannon divergence (JS; primary), soft-target negative log-likelihood (NLL), the Brier score, and Earth Mover's distance (EMD) are minimized. JS is computed per video and then averaged. NLL is the cross-entropy of the predicted distribution against the empirical target distribution. The Brier score is the sum of squared probability errors across classes. EMD is the normalized cumulative-distribution discrepancy over the frozen class-index order; it is therefore an operational ordered-label metric and must not be interpreted as a semantic transport distance unless that order is substantively justified.

Macro-F1 and Balanced Accuracy are maximized and provide dominant-emotion compatibility views by applying `argmax` to both target and predicted distributions. Expected calibration error (ECE) and adaptive calibration error (ACE) are minimized. Both compare maximum predicted probability with dominant-class correctness: ECE uses 15 fixed equal-width confidence bins, whereas ACE uses up to 15 equal-count groups. These dominant-class confidence diagnostics do not establish full-distribution calibration.

AURC-JS is minimized. For each video, the selective risk is its JS divergence and confidence is the maximum predicted probability. Predictions are ordered from high to low confidence, equal-confidence items enter coverage together, and the area summarizes mean retained JS risk as coverage increases. AURC-JS is neither an AUROC nor a binary-classification ranking statistic; its rejection score is one minus maximum class probability. Retrieval diagnostics such as Recall@K or nDCG@K are added only where relevance is valid. Formal aggregate values and paired uncertainty remain unavailable until the Task 50 result freeze. `[RESULT-GAP:FINAL_METRIC_VALUES_AND_NATIVE_UNIT_UNCERTAINTY]`

### 5.7 Statistical analysis

Formal comparisons use at least five random seeds and paired bootstrap 95% confidence intervals at the dataset-native content-unit level: video for CSMV, image for LAI-GAI, and video or movie only when justified by the frozen Video2Reaction-native protocol. Comments, raters, folds, and seeds are repeated observations or training variations, not independent inferential units. Cross-dataset absolute metric comparisons are not used because label spaces, domains, inputs, and target construction differ. Primary comparisons, multiplicity correction, model-selection rules, coverage targets, and equivalence/noninferiority margins—if used—must be pre-registered. Report effect sizes and uncertainty, not p-values alone.

Task 40 development uses the frozen seeds `1364847620`, `426925854`, `1839464886`, `1138176833`, and `484191872`, with separate development-selection and development-calibration partitions. CSMV response thinning uses 2, 4, 8, and all available responses with 200 resamples; cross-thinning comparisons use the common `n>=8` subset. LAI-GAI uses 8, 16, 32, and all responses per marginal dimension. The primary method comparison is content-unit JSD at 90% answer coverage; the primary reliability comparison is negative-transfer rate for credible routing versus the strongest eligible point-utility or generic router. Formal test remains unmaterialized until Task 50.

### 5.8 Implementation and reproducibility

Task 20 used an independently locked baseline environment with Python 3.8.9, PyTorch 2.4.1+cu121, CUDA 12.1, Transformers 4.30.2, FAISS 1.7.4, scikit-learn 1.3.2, CatBoost 1.2.10, LightGBM 4.5.0, and NumPy 1.24.4. The recorded reference host used an RTX 3070 Ti, float32 arithmetic, and no automatic mixed precision. Final method runs must separately report their own hardware and environment rather than inheriting this baseline host description.

One configuration schema, run-manifest schema, prediction schema, data loader, and evaluator govern the Task 20 baselines. Prediction rows bind the sample ID and split to the frozen class order, target and predicted distributions, confidence, rejection score, model ID, and configuration ID. Fitting, normalization, indexing, and feature-dependent selection are train-only; development data may tune hyperparameters and select a checkpoint; test data are hidden during selection and evaluated once under the pre-registered seed rule without adaptation. Every model family receives at most 12 trials. For the frozen-I3D MLP and temporal-attention families, the registered grid combines three hidden widths, two dropout values, and two learning rates, with at most 200 epochs and patience 20; development JS is minimized, followed by NLL, Brier score, and parameter count as deterministic tie-breakers.

The run manifest links the data and split revisions, admissible asset-risk decision, configuration, seed, fit scope, code revision, prediction artifact, and metric artifact. A same-environment, same-seed replay of the temporal-attention baseline produced byte-identical development predictions, metrics, selection records, trial records, model state, and standardizer state. This is evidence of engineering determinism within that frozen environment, not cross-hardware reproducibility or statistical stability. The handoff and G3 packages bind tracked evidence by SHA-256, while restricted I3D features, comments, credentials, local paths, and other reversible assets are excluded from redistribution. Report final parameter counts, optimizer and schedule, batch size, calibration fitting, training time, peak memory, and eligible artifact locators only after the formal result freeze. `[RESULT-GAP:FINAL_REPRODUCIBILITY_TABLE]`

## 6. Results

> This section is intentionally non-empirical until `results-freeze-v1` exists. Do not insert development-run, single-seed, NON_T0, leakage-accepted exploratory, or test-guided values.

### 6.1 Protocol validity and baseline credibility

`[RESULT-GAP:C1_G1_G2_G3_AND_E0_EVIDENCE]`

The current protocol evidence supports infrastructure credibility but not a performance claim. The independently reviewed Task 20 package records `G3=PASS_WITH_LIMITATIONS`, a common split/input/evaluator contract, fail-closed E0 checks for split leakage, duplicate or misaligned sample IDs, invalid probability distributions, and index-scope violations, and a 22-artifact hash-bound handoff. The evaluator and baseline package passed the recorded Task 20 test suite, and the temporal-attention implementation passed a same-environment, same-seed deterministic replay. These checks establish that the frozen baseline machinery can reject specified invalid inputs and replay one registered run; they do not establish exhaustive leakage coverage, multi-seed or cross-hardware stability, or comparative performance.

Baseline credibility is correspondingly scoped. The temporal-attention result is a single-seed strong reimplementation, the legacy models are native-task compatibility checks, unavailable modern encoders are reference models without results, and the VC-CSA author-setting run is protocol-mismatched NON_T0 exploratory evidence excluded from this paper's quantitative claims. Dataset-unit counts, exclusions, complete E0 outcomes, strongest fair baseline values, five-seed uncertainty, and paired native-unit comparisons remain gated on frozen Task 50 artifacts. No development, exploratory, or single-seed performance number is promoted into this section.

### 6.2 Credible net-benefit memory routing

`[RESULT-GAP:C2_E2_E4_E7_FIVE_SEED_PAIRED_RESULTS]`

Required reporting: content-only, memory-only, fixed fusion, no/random/lexical/nearest-neighbor/learned retrieval; oracle headroom; generic, point-utility and credible-net-benefit routers; matched-coverage selective controls; utility-prediction quality; negative-transfer rate; posterior and thinning sensitivity; harmful-retrieval avoidance; and failure cases.

### 6.3 Three-source uncertainty and prediction regions

`[RESULT-GAP:C3_THREE_SOURCE_AND_REGION_RESULTS]`

Required reporting: separate observable checks for group disagreement, finite-response sampling, and model/transfer uncertainty; one-source-at-a-time ablations; empirical coverage and region size at every pre-registered target; and explicit deletion of the decomposition claim if the sources cannot be distinguished.

### 6.4 Distribution shift and external validity

`[RESULT-GAP:C3_E5_E6_VIDEO2REACTION_DUAL_TRACK]`

Report every pre-registered shift, including negative findings. CSMV, LAI-GAI, and Video2Reaction-native metrics must remain in dataset-specific tables. A result on silver labels cannot be used to upgrade a HUMAN_GOLD claim.

### 6.5 Calibration and selective prediction

`[RESULT-GAP:C2_C3_CALIBRATION_AND_RISK_COVERAGE]`

Required reporting: full-coverage calibration, coverage-matched risk, AURC, operating points chosen without test labels, and whether abstention concentrates on shifted, low-quality, or high-disagreement cases.

### 6.6 Efficiency and sensitivity

`[RESULT-GAP:E9_AND_PRE_REGISTERED_SENSITIVITY]`

Report parameter count, peak memory, runtime, index size, retrieval latency, and sensitivity to memory size, neighbor count, sequence pooling, and other pre-registered choices.

### 6.7 Main result table shell

| Claim | Primary comparison | Dataset/protocol | Effect and 95% CI | Claim status | Evidence artifact |
|---|---|---|---|---|---|
| C1 | Protocol/evaluator validity | Two HUMAN_GOLD datasets | `[RESULT-GAP]` | TO_VERIFY | `[RESULT-GAP]` |
| C2 | Credible router vs strongest point/generic router at matched coverage | CSMV strict T0 + response thinning | `[RESULT-GAP]` | TO_VERIFY | `[RESULT-GAP]` |
| C3 | Three-source/region system vs source-matched controls | Applicable HUMAN_GOLD shifts + external tracks | `[RESULT-GAP]` | TO_VERIFY | `[RESULT-GAP]` |

## 7. Discussion

### 7.1 Answer to the research question

`[RESULT-GAP:DISCUSSION_BOUND_TO_SUPPORTED_CLAIMS]`

The discussion must answer whether historical reaction evidence, finite-response posterior benefit, and selective routing improve reliability under the tested information boundary. It must distinguish average predictive improvement, calibration improvement, negative-transfer reduction, and selective-risk improvement.

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

Report where memory, point or credible routing, uncertainty decomposition, prediction regions, or rejection do not help. Task 30 remains an archived development non-pass rather than a formal H1 result. A null H2 or H3 result triggers the predefined claim downgrade and should be interpreted as evidence about protocol or failure mechanisms, not hidden through selective reporting.

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
11. **Responder-selection boundary.** The observed distributions are conditional on who supplied a retained comment or rating. They do not identify the response distribution among silent viewers, and platform deletion, ranking, moderation, and participation incentives may change which reactions are observed.
12. **Gold/silver asymmetry.** `HUMAN_GOLD` denotes independently collected human response labels with auditable provenance; it does not remove sampling or measurement error. `SILVER_LLM_HUMAN_VERIFIED` denotes automated label construction with human quality checks and cannot be promoted to HUMAN_GOLD or pooled into the principal human-label tables.
13. **Baseline-evidence maturity.** The current strongest T0-compatible Task 20 baseline has single-seed engineering evidence only. Five-seed stability, paired bootstrap intervals, and formal comparative claims remain unavailable until Task 50.
14. **Comparator availability and applicability.** CLIP, SigLIP, and VideoMAE inputs were unavailable in frozen T0, while late fusion, minimal cross-attention, and modality-increment E1 were not applicable with one available content modality. These statuses limit comparator breadth and must not be interpreted as negative results.
15. **Official-code comparability.** The author-released VC-CSA setting uses target comments and a comment-level split. Its leakage-accepted 120-epoch exploratory run is NON_T0 and permanently ineligible for the formal baseline table, irrespective of its numerical outcome.
16. **Metric operationalization.** EMD depends on the frozen class-index order, while ECE, ACE, and AURC-JS use maximum-probability confidence and dominant-class correctness or JS risk. They do not by themselves validate a semantic emotion geometry or full-distribution calibration.
17. **Determinism scope.** Byte-identical same-environment, same-seed replay demonstrates a controlled engineering property, not reproducibility across hardware, software stacks, random seeds, or future asset revisions.

## 9. Conclusion

`[RESULT-GAP:CONCLUSION_CONTAINING_ONLY_SUPPORTED_C1_TO_C3]`

The conclusion must restate the reliability question, summarize only supported evidence, identify the conditions under which retrieval or abstention is beneficial, and preserve the construct and asset boundaries. It must introduce no new result, method, dataset, or claim.

## Data Availability

The project will release, subject to anonymity review, the eligible schemas, content-unit split manifests, label-provenance manifests, hash ledgers, deterministic preprocessing and leakage-validation code, configuration contracts, and table/figure regeneration scripts. CSMV annotations are obtained through the dataset's official repository and are tracked at the frozen annotation revision recorded in the source ledger. CSMV platform media, raw comments, user identifiers, URL lists, and the fixed I3D feature package will not be redistributed by this project. The I3D files may be used internally only under the documented accepted-risk decision: their asset-level license, stable official revision, rightsholder package identity, and external fixity attestation remain unresolved, so the decision is neither a license grant nor evidence of official authorization.

LAI-GAI images and metadata are available from the official dataset source under its documented CC BY 4.0 terms; this repository tracks the 847-image revision and hashes but does not republish the source images or participant-level rating files. Only de-identified image-level aggregate labels may enter a release after a separate publication-boundary review. Video2Reaction is currently identified at Hugging Face revision `75278468c91c51ff54cf709d61ee881ca5c37c9b`, but intake remains conditional because the dataset card's annotation license and the repository-level license statement are not yet reconciled; its native annotations are silver and underlying media rights remain source-specific. CUC-IGPE-v2 raw and derived records remain local because consent, platform permission, and redistribution rights are unresolved. `[DECISION-GAP:FINAL_ARCHIVE_LOCATORS_AND_RELEASE_VERSION]`

## Code Availability

`[DECISION-GAP:ANONYMIZED_REPOSITORY_RELEASE_AND_ARCHIVAL_PLAN]`

At minimum, release eligible split manifests, schemas, evaluation code, configuration files, environment specification, and scripts that regenerate every reported table and figure, subject to licensing and anonymity constraints.

## Ethics, Privacy, and Responsible Use

This project analyzes existing research datasets and does not recruit new participants. Data minimization is enforced at the repository boundary: tracked artifacts exclude response text, comment and user identifiers, publisher names, raw URLs, cookies or access tokens, media, participant keys, demographic attributes, and device or completion metadata. CSMV response text is confined to the local read-only layer for content-unit aggregation and membership checks; release candidates retain only aggregate distributions, response support, non-reversible work identifiers, and provenance hashes. For LAI-GAI, only rows satisfying the source consent and data-use filters enter aggregation, while participant and Prolific keys and demographic fields remain in the ignored raw layer; the tracked canonical form contains image-level aggregates only.

Public accessibility is not treated as permission to redistribute third-party media or to profile individuals. The project prohibits re-identification, cross-table user linkage, recovery or publication of response text, individual affect diagnosis, political targeting, and automated decisions about people. Predictions are interpreted only as uncertain distributions of publicly expressed or elicited responses within the observed sampling frame, not as private mental states. Platform removal, license withdrawal, identity/fixity drift, or a rightsholder objection invalidates the corresponding manifest and triggers suspension of dependent evidence. The final submission will report the applicable institutional ethics determination and venue-required disclosure without presuming exemption from public availability alone. `[DECISION-GAP:INSTITUTIONAL_ETHICS_DETERMINATION]`

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

- S1. Dataset lineage, license, and fixity tables. For every dataset and evidence track, report the official locator, frozen revision, native unit, label provenance tier, response-support rule, file/manifest hash, license layer, redistribution boundary, and unresolved item. In particular, separate CSMV annotations, code, platform media, and I3D assets; identify LAI-GAI's 847-image and rating revisions; and keep Video2Reaction-native silver evidence distinct from both HUMAN_GOLD datasets.
- S2. Split construction and leakage audits. Provide the deterministic grouping rules and counts for CSMV `group_by_video_v1`, the source-family-plus-hashtag split, and LAI-GAI's 379-group split; document exact/near-duplicate handling, target-response isolation, future-field rejection, fit scope, and index membership. Report unavailable dimensions as unavailable: the current CSMV time and native-topic protocols are not released, and `PASS_NOT_BUILT` for an index is not evidence that a later index is safe. Include executable positive checks and fail-closed negative tests, with any failure marked `LEAKAGE_BLOCKED`.
- S3. Full hyperparameter spaces and model-selection rules. Include the common 12-trial cap; the frozen-I3D MLP/temporal-attention grid of hidden width {128, 256, 512}, dropout {0.1, 0.3}, and learning rate {0.0003, 0.001}; the 200-epoch maximum and patience 20; and the development-selection order of JS, NLL, Brier score, then parameter count. Record train-only fitting and one-time test access explicitly.
- S4. Complete five-seed results and native-unit bootstrap intervals. The Task 20 bootstrap implementation is interface-validation evidence only; formal five-seed paired video-level statistics belong to Task 50 and must be generated from frozen predictions rather than inferred from the single-seed run.
- S5. Calibration, risk–coverage, and operating-point details.
- S6. Retrieval provenance, pollution controls, and negative-transfer cases.
- S7. Additional OOD, missing-input, and sensitivity results.
- S8. Efficiency, compute, and environmental reporting.
- S9. Reproducibility checklist and artifact manifest. Publish eligible configuration, run-manifest, and prediction schemas; probability, split, sample-alignment, and train-only-index failure tests; the evaluator implementation; environment lock; code revision; and SHA-256 ledger. Distinguish same-environment deterministic replay from cross-environment reproduction, and exclude I3D arrays, comments, credentials, machine-local paths, and other restricted or reversible assets.
- S10. Ethics, privacy, data-access, and AI-use disclosures.

## Internal submission gate

This manuscript cannot be marked `SUBMISSION_READY` until all of the following are true:

- C1–C3 have final states with linked evidence; unsupported claims are removed or downgraded.
- G6 and all T-AFFC Go standards have independently passed.
- The two HUMAN_GOLD datasets remain the basis of the principal quantitative claims.
- Video2Reaction has a fair comparison or an accepted, detailed non-executability audit.
- Five-seed, native-content-unit uncertainty, calibration, efficiency, and failure analyses are frozen.
- All `[RESULT-GAP]`, material `[CITATION-GAP]`, and submission-critical `[DECISION-GAP]` markers are resolved.
- Claim-blacklist, citation, consistency, integrity, anonymity, and reproducibility audits pass.
- The current official IEEE T-AFFC author instructions and template are rechecked at submission time.
