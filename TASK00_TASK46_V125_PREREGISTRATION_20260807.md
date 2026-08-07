# Task46 v1.25 预注册（草案冻结，确认集仍封存）

## 预注册身份

- route: IEEE T-AFFC CARM
- task: candidate Task46, `PLANNED_NOT_CREATED`
- dataset: CSMV, original train only
- primary cluster: source_group
- seeds: `1364847620, 426925854, 1839464886, 1138176833, 484191872`
- posterior: `Dirichlet(c+0.5)`, 200 deterministic draws; `Dirichlet(c+1)` sensitivity
- primary policy coverage: `0.90` non-abstaining answer coverage; action set `USE_MEMORY/FALLBACK_CONTENT/ABSTAIN`
- formal test: forbidden; Task50: not created

## Target chain

`Q`: Can strict-T0 evidence predict transferable historical-reaction utility and turn it into safer policy decisions?  
`E`: posterior utility distribution of `Delta=JSD(theta,f0)-JSD(theta,fH)` under source-group-disjoint OOF.  
`Y`: `p_tau`, `mu`, `m+`, `m-`, `Q05/CVaR`, proper loss, calibration, ranking and final paired JSD.  
`F`: valid cross-group null, same-budget baselines, content-only dominance, policy JSD non-improvement, risk-budget violation or full fallback.  
`A`: stop, downgrade to measurement/negative result, or (only after all gates) continue to ordered policy/P5 evidence.

Primary `tau=0` and `tau_h=0` are frozen directional thresholds; no post-confirm threshold selection is allowed. Any nonzero SESOI sensitivity must be selected from FIT-only declared JSD resolution before P3 closure.

## Inputs and exclusions

Allowed: frozen T0 content state; train-only retrieval geometry; train-neighbor response support and disagreement; expert interaction and OOD distance derived without query reactions.  
Forbidden: query response count/comment/label, true Delta or posterior target, future interaction, confirmation statistics, formal-test information, old DEV/DIAG_CONFIRM results, or any target-derived feature.

## Model and baseline family

Constant, content-entropy/similarity/agreement heuristics, same-capacity G0, G1/G2/G3 ablations, full G0—G3 utility predictor, fixed fusion, always-content, always-memory, Task40 point router, generic gate and SelectiveNet are preregistered comparisons. Candidate learners are only HGB/ElasticNet/shallow MLP under identical FIT-only nested CV and fixed trial budget; no MoE, Transformer router, new retriever or seed search.

## Negative control

Cross-source-group support-stratified constrained derangement with bins `[2,4],[5,8],[9,12],[13,16],[17,20]`, 200 fixed permutation seeds, changed-row rate ≥0.95, zero same-source assignment, `|rho|≤0.10`, preserved within-bin marginals and deterministic replay. Synthetic null and FIT sanity must pass before confirmation access.

## Gates

1. `U0_IDENTITY_CONTROL`: roles, hashes, zero access and negative-control validity all pass.
2. `U1_UTILITY_LEARNABILITY`: probability and magnitude proper-loss contrasts versus G0 satisfy predeclared cluster-bootstrap CI and ≥4/5 seed direction; real model exceeds valid null after Holm correction.
3. `U2_POLICY_FREEZE`: calibration, tau/tau_h, SESOI, expected-regret, LCB/CVaR, risk budget, 0.90 coverage, model and baseline family frozen in FIT OOF.
4. `U3_ONE_SHOT_POLICY`: ROUTER_CONFIRM opened once; paired video-level JSD versus strongest matched-coverage control is the primary policy endpoint.
5. `U4_NEGATIVE_TRANSFER`: only after U3 pass; otherwise `NOT_TESTED`.
6. `U5_THREE_SOURCE_P5`: only after U3 and U4 pass; otherwise `NOT_EXECUTED`.

## Reproducibility and amendment rule

All configs, manifests, code commit, environment, seed list, hashes, access events, failures and stderr are retained. A confirmation error may repeat the exact frozen bundle only; no model, threshold, coverage, baseline or metric change is allowed after opening. Any amendment is exploratory and cannot rescue a failed primary gate.

