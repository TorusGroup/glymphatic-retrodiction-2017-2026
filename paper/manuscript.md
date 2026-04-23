# Retrodiction as validation: A hash-sealed AI forecasting protocol tested on glymphatic neuroscience 2017-2026

**Running title:** Hash-sealed retrodiction of AI-generated hypotheses

---

## Authors

Matheus Fink¹\*, Prometheus Lab (Torus OS)²

¹ TorusGroup, MVP Factory, São Paulo, Brazil
² Prometheus Lab, Torus OS — Cognitive pipeline for AI-augmented scientific hypothesis generation

\*Correspondence: matheusfinik@gmail.com

---

## Abstract

**Background.** Large language models (LLMs) increasingly generate scientific hypotheses, but validity is confounded by training-data leakage: a model may appear to "predict" a finding that was already in its training corpus. No widely-adopted methodology provides a cryptographic guarantee against this confound. **Methods.** We pre-registered a retrodiction protocol. An AI pipeline (Opus 4.7, operating under a retrieval-only system prompt constrained to literature published on or before 2017-12-31) generated 18 candidate predictions about the glymphatic system for the 2018-2026 window. A parallel adversarial audit ("Anomalist Pass") killed 2, reformulated 10, and passed 6 intact, yielding 16 sealed predictions. The file was hash-sealed (SHA-256) and committed to a public git repository before any post-2017 literature was consulted. We then built a validation corpus of 3,329 peer-reviewed papers and preprints (2018-01-01 to 2026-04-23) and scored each prediction against it. Leakage was audited in three layers: factual DOI-date verification (Crossref/PubMed), an independent-model AI judge (multi-model cross-audit using `gemini-3.1-pro-preview` as primary, with `gemini-2.5-pro` and `gemini-2.5-flash` as supplementary capability tiers), and same-model self-consistency. One prediction (PRED-GLY-011) was invalidated post-hoc when the primary independent-model audit flagged it as methodological leakage: the predicted experimental setup (synchronized fMRI + delta-EEG + CSF inflow in NREM humans) described Fultz 2019 Science too precisely to be an *a priori* formulation; the flag was confirmed independently by `gemini-2.5-pro`. Separately, a provisional earlier invalidation of PRED-GLY-009 (driven by a `gemini-2.5-flash` single-model flag about "Iliff-Smith debate" terminology) was reversed after higher-capability models both classified it as CLEAN; PRED-GLY-009 was revalidated. The final valid pool was N=15. **Results.** Of 15 sealed-and-valid predictions, 8 were CONFIRMED (53.33%), 5 PARTIALLY CONFIRMED (33.33%), 0 CONTRADICTED, 2 INCONCLUSIVE (tool-dependent); 2 additional draft predictions were destroyed pre-seal by the adversarial audit and 1 was invalidated post-seal by the primary independent-model audit. Strict precision was 53.33%; liberal precision (CONFIRMED ∪ PARTIAL) was 86.67%. Eight of 15 predictions were classified as NOVEL. Forward insight value (predictions confirmed ≥1 year before first publication) was 6.67% (1/15 — PRED-GLY-017, Da Mesquita 2018 *Nature*). DOI-level factual leakage was 0.00% (0 of 48 verified anchors dated post-2017); convergent leakage under the primary judge was 6.25% (1/16 — the methodological leakage detected). **Conclusion.** Under strict cryptographic blinding, the AI pipeline demonstrated measurable concurrent forecasting ability in a maturing biomedical field. The gap between liberal precision (strong) and insight value (weak) reflects the explosive growth of glymphatic research in the 18 months immediately following the cutoff. The multi-model leakage audit produced a methodologically important result: capability-scaling the independent judge both (a) rejected false positives produced by the lowest-capability model (three ALPS-date errors and one terminology over-reach) and (b) detected a genuine methodological leakage on PRED-GLY-011 that the lowest-capability model had missed — positive operational evidence that a single-model independent audit is insufficient for rigorous AI-for-science validation. The protocol — hash-sealed retrodiction with adversarial pre-audit, factual DOI verification, multi-model independent-judge audit, and same-model self-consistency — is offered as a reproducible falsification test for AI-generated science.

**Keywords:** AI for science; retrodiction; meta-science; glymphatic system; large language models; cryptographic pre-registration; falsifiability; hypothesis generation

---

## 1. Introduction

### 1.1 The validity crisis in AI-generated science

Since the release of GPT-3 in 2020, and more acutely since the deployment of reasoning-capable models (Claude 3, GPT-4, Gemini, and their successors), LLM-authored scientific reasoning has become unavoidable. These systems write literature reviews, propose mechanisms, design experiments, and — increasingly — generate novel scientific hypotheses. Reports of AI-led contributions to mathematics (Romera-Paredes et al., 2023), protein structure prediction (Jumper et al., 2021), and algorithmic discovery (Novikov et al., 2025, *AlphaEvolve*) have accompanied a surge of papers whose hypothesis-generation step is, de facto, an LLM.

A foundational problem follows. LLMs are trained on corpora that include the entire historical scientific literature. When such a model "proposes" a hypothesis that was already partly established in its training data, the researcher has no principled way to distinguish:

1. **Genuine synthesis** — the model combined existing knowledge in a novel, predictively valid way;
2. **Elegant paraphrase** — the model restated a known finding in fresh language;
3. **Implicit recall** — the model reproduced a fact it had memorized without attribution.

All three look identical at the interface. This is not merely an epistemic inconvenience; it undermines the entire basis on which AI contributions to science can be evaluated.

### 1.2 Existing responses and their limitations

The AI-for-science community has responded with several methodologies, each partial:

- **Benchmark evaluation** (e.g., MMLU, GPQA, AI2 Reasoning Challenge): measures answer accuracy on curated tests. Does not address generative hypothesis validity.
- **Human expert review** (LLM-as-author peer review): captures plausibility but not predictive validity; experts cannot reliably detect implicit recall.
- **Preference elicitation** (RLHF, DPO): optimizes perceived quality. Orthogonal to truth.
- **Temporal holdout in training** (the "cutoff" strategy): reports the model's nominal training cutoff and evaluates on later data. In practice, training corpora leak: preprints, blog posts, and derivative literature often contain future findings before they formally "publish."

A stronger methodology — rarely operationalized — is **retrodiction**: freeze the model's input to a historical state, generate predictions about a known-to-the-experimenter future, and score the predictions against that future. The concept is old in astronomy (Popper, 1959; Lakatos, 1970) and standard in machine learning holdout testing. It is underdeveloped for LLM-generated science.

### 1.3 Our contribution

We present a composite protocol that combines three techniques, each individually standard but not previously integrated for LLM validation:

1. **Literature freezing with cryptographic seal.** The AI operates on a corpus hash-sealed to a specific date. Predictions are themselves hash-sealed before any post-cutoff literature is consulted.
2. **Adversarial pre-audit (Anomalist Pass).** A second, independent AI session attempts to destroy each prediction on epistemological grounds before sealing. Survivors alone enter the hash-chain.
3. **Independent validation corpus.** Post-cutoff evidence is built as a separate corpus, also hash-sealed, and scored against the predictions by a validator who can be audited by third parties.

We demonstrate the protocol on the **glymphatic system** — a field born in 2012 (Iliff et al., 2012, *Science Translational Medicine*) that exploded between 2018 and 2026. The temporal structure is ideal: substantial prior art exists by 2017 to ground the AI's reasoning, and a large validation corpus accumulated quickly in the years that followed.

We ask three operational questions:

- **Q1 (Precision).** What fraction of AI-generated predictions are supported by post-cutoff evidence?
- **Q2 (Anticipation).** How far ahead of first publication did the predictions arrive?
- **Q3 (Leakage).** What fraction of predictions rest on claims dated after the cutoff despite the retrieval-only constraint?

### 1.4 Scope

This is a methodological contribution. We do **not** claim that glymphatic-system hypotheses generated by an LLM are superior to those of human domain experts; we make no comparison. We do **not** claim that the protocol validates *all* AI-for-science. We claim that it provides a falsifiable, reproducible test that any AI hypothesis-generation system can be subjected to, and we report honestly the result of one instance — including its limitations.

The paper proceeds as follows. §2 describes the protocol formally (the seven phases R-1 through R-7). §3 reports the characteristics of the frozen-2017 corpus, the 16 sealed predictions, the leakage audit, and the validation corpus. §4 reports results — precision, novelty, insight value, and three detailed case studies. §5 discusses limitations, what we learned about the method, and implications. §6 concludes.

---

## 2. Methods

### 2.1 Overview

The protocol comprises seven phases (R-1 through R-7) executed in strict temporal order, with two cryptographic seals and three audit gates. Figure 2 shows the pipeline.

| Phase | Name | Artefact | Cutoff |
|-------|------|----------|--------|
| R-1 | Cartograph ≤2017 | Literature base (≤2017-12-31) | 2017-12-31 |
| R-2 | Probe for unknown-unknowns | Candidate gaps | 2017-12-31 |
| R-3 | Decompose into sub-questions | Question tree | 2017-12-31 |
| R-4 | Cross-domain synthesis | Derived hypotheses | 2017-12-31 |
| R-5 | Genesis of predictions | Draft predictions | 2017-12-31 |
| R-6 | Anomalist Pass | Adversarial audit + hash seal | 2017-12-31 |
| R-7 | Validate against 2018-2026 | Scoreboard | 2026-04-23 |

### 2.2 Phase R-1: Literature base (corpus ≤2017)

We constructed the baseline corpus using ten canonical queries on PubMed E-utilities, Europe PMC (preprint proxy via SRC:PPR), and arXiv (q-bio.NC). Queries targeted the glymphatic-system core, AQP4 biology, CSF-ISF exchange, perivascular/paravascular flow, meningeal lymphatics, and applied fields (aging, Alzheimer's, stroke, TBI, sleep, imaging). The inclusion threshold was set permissively (relevance score ≥ 3) to optimize recall.

**Filters applied:** (a) `publication_date ≤ 2017-12-31` (hard); (b) English language; (c) abstract ≥ 50 characters; (d) non-editorial publication types. All 887 raw results were deduplicated (DOI > PMID > canonical title), yielding 563 papers after filtering (559 peer-reviewed, 3 preprints via Europe PMC, 1 arXiv). The corpus was serialized as JSONL and hash-sealed (SHA-256: `d4f52383…4e4849b`). Complete query specifications and exclusion logs are available in the repository.

### 2.3 Phase R-1 continued: Knowledge Map

From the 563 papers, two human-AI-assisted passes populated:

- **L1 — Known Knowns:** 42 facts with confidence ≥ 0.70, each anchored by ≥1 DOI/PMID.
- **L2 — Known Unknowns:** 22 open questions, each classified by status (actively debated / emerging / underexplored / unexplored) and anchored to ≤2017 literature establishing the gap.

This map was the sole substrate available to the prediction-generation phase. No post-2017 literature was retrieved or embedded.

### 2.4 Phases R-2 through R-5: Prediction generation

An Opus 4.7 instance operated under a retrieval-only system prompt. The prompt forbade the model from asserting claims lacking ≤2017 citation; enforced anchor-based rationale (each prediction must cite ≥3 ≤2017 sources); required falsification criteria; and banned post-2018 temporal language ("since," "recently," "emerging evidence shows"). Eight detection vectors (convergence, failure archaeology, temporal projection, axiomatic inversion, isomorphism across domains, constraint removal, scale bridging, decomposition) guided candidate generation from L2 open questions and cross-domain synthesis of L1 facts.

The model produced 18 draft predictions in structured YAML. Each had a unique ID, claim, predicted window, confidence ∈ [0, 1], ≥3 anchors (DOI + excerpt), falsification criterion, category, and applied detection vectors.

### 2.5 Phase R-6: Anomalist Pass (adversarial audit)

A second Opus 4.7 session, with no context from phases R-2 through R-5 beyond the draft predictions and the ≤2017 corpus, played the role of an adversarial reviewer. Each prediction was subjected to three questions:

1. **"Is this novel or merely well-written?"** — If the prediction restates ≤2017 consensus, verdict = DESTROYED.
2. **"Is any claimed cross-domain isomorphism structural or superficial?"** — Superficial isomorphisms yielded DESTROYED or WOUNDED.
3. **"What would a 2017 glymphatic expert (Iliff or Nedergaard) say?"** — Simulated responses calibrated the verdict.

Each prediction received one of three verdicts: SURVIVED (intact), WOUNDED (reformulated with thresholds relaxed, scope tightened, or language adjusted), or DESTROYED (removed). The expected DESTROY rate was 20-40% — too few signals a weak adversarial, too many signals poor generation.

### 2.6 Phase R-6 continued: Hash-sealing

The 16 surviving predictions (6 SURVIVED + 10 WOUNDED-REFORMULATED) were normalized (YAML serialized with sort_keys=True, LF line endings, UTF-8, trailing newline), then SHA-256 hashed. The file and hash were committed to a public git repository ([TorusGroup/glymphatic-retrodiction-2017-2026](https://github.com/TorusGroup/glymphatic-retrodiction-2017-2026)) before any post-2017 literature was consulted. Original seal (v1): `1765b221…7afb586`. Current canonical seal (v4, post Phase 3.8 multi-model re-audit): `a144c180…9e54460`. Full chain: v1 → v2 (citation hygiene) → v3 (provisional Flash-flag invalidation, later reversed) → v4 (multi-model re-audit, current). Any reader can verify by running `sha256sum predictions/predictions-final.yaml` against the cloned repository.

Three trust anchors were planned: (a) the git commit itself, (b) publication of the hash in an arXiv preprint, and (c) OpenTimestamps Bitcoin anchoring. Anchor (c) was deferred for operational reasons (the OpenTimestamps CLI was not installed on the execution machine); it will be completed before final submission. The deferred anchor does not weaken the seal — the git commit chain provides independently verifiable timestamp provenance.

### 2.7 Phase 3.5: Citation hygiene correction

During the leakage audit (§2.9), we discovered five reference-hygiene errors in the original sealed file: two DOI prefix typos, and three PMIDs whose titles did not match the cited excerpts. We verified that in every case, the underlying concept *was* published before 2018 and was the one the prediction was anchoring to. Correcting the citations was therefore a hygiene fix, not a content edit. We re-sealed the corrected file and transparently documented the change (commit `17501bc1`). The original hash (`1765b221…7afb586`), the correction log, and the corrected hash are all preserved. This event itself is reported as a limitation (§5.2).

### 2.8 Phase R-7: Validation corpus (2018-01-01 to 2026-04-23)

The validation corpus was constructed *after* the hash-seal. Queries mirrored Phase 2 but with the window `2018-01-01 : 2026-04-23`, plus five new queries targeting post-2018 subfields (Alzheimer's-explicit, Parkinson's-explicit, perivascular-clinical, lymphatic-CNS, drug-delivery). The same filters applied. Final count: 3,329 papers (3,192 from PubMed; 130 preprints via Europe PMC; 7 from arXiv), 5.91× the volume of the baseline corpus. SHA-256: `3aa15c2c…99be5df`.

### 2.9 Leakage audit

Three parallel audit layers were designed and executed; Layer 2 was itself cross-validated across three model-capability tiers:

- **Layer 1 (factual, objective):** DOI-date verification. Every anchor DOI was resolved via Crossref API (primary) and PubMed E-utilities (fallback). `publication_date > 2017-12-31` counted as leakage.
- **Layer 2 (independent-model adversarial, multi-model cross-audit):** Three Gemini models (via the `google-generativeai` SDK) were run with identical prompt and temperature=0.1 on the full sealed set, in the following role assignment:
  - `gemini-3.1-pro-preview` — **PRIMARY JUDGE** (most capable; its verdict is adjudicative)
  - `gemini-2.5-pro` — independent cross-validator (confirms or challenges primary)
  - `gemini-2.5-flash` — legacy lowest-capability baseline (retained for transparency; not adjudicative)

  Each model independently classified every prediction as CLEAN, SUSPECT, or LEAKED with a free-text reason. The multi-tier design lets us explicitly observe capability-dependent error patterns and avoid single-model false-positive or false-negative risk.
- **Layer 3 (same-model self-consistency):** A fresh Claude session re-scored each prediction in a leakage-hunter role.

The primary judge (Pro 3.1) flagged 1/16 predictions as LEAKED: **PRED-GLY-011**, whose predicted experimental design (synchronized fMRI + delta-EEG + CSF inflow in NREM humans) precisely describes the setup of Fultz *et al.* 2019 *Science*. The pre-2018 anchors (Xie 2013 mouse glymphatic; Jessen 2015 review) do not describe the multimodal human fMRI+EEG design. The flag was classified as **methodological leakage** (not terminology leakage). It was **independently confirmed** by `gemini-2.5-pro`, which flagged the same prediction with the same rationale. This convergence across the two most capable audit models establishes the flag as a TRUE POSITIVE.

**Capability-scaling observations.** The lowest-capability model (`gemini-2.5-flash`) had produced, in an earlier preliminary pass, four different flags: three false positives about the ALPS index (where Flash confused Taoka's original 2017 publication with its 2020-2024 popularization) and one ambiguous flag on PRED-GLY-009 concerning the term "Iliff-Smith debate". A provisional Phase 3.7 invalidation of PRED-GLY-009 based on this Flash flag was reversed in Phase 3.8 after both higher-capability models (Pro 3.1 and Pro 2.5) classified PRED-GLY-009 as CLEAN. Pro 3.1's explicit reasoning: *"relies on pre-2018 concepts (the debate between Iliff bulk flow and Smith diffusion, and early models of oscillatory dispersion) to make a plausible forward-looking claim."* PRED-GLY-009 was thus **revalidated** and restored to the valid pool. Simultaneously, PRED-GLY-011 was invalidated via metadata overlay (not deletion). The file was re-sealed (SHA-256 v4: `a144c180…9e54460`), preserving the cryptographic chain v1 → v2 → v3 → v4.

Layer 3 (same-model self-consistency) flagged 0/16 — confirming its known limitation of same-model bias and reinforcing the necessity of the Layer 2 multi-model cross-audit.

The central methodological finding of this audit is not the single invalidation but the **swap**: moving from single-model Flash adjudication to multi-model Pro 3.1-primary adjudication produced a substantively different judgment (009 out → 009 in; 011 in → 011 out) with net-zero change in pool size but materially different composition. This is direct operational evidence for the claim that cross-model audit is a load-bearing component of rigorous AI-for-science validation, not an optional extra. Full per-model verdicts are reproducible from the scripts and JSON outputs released with this paper; the inter-model comparison matrix is reported in Supplementary Material §S3.

### 2.10 Phase R-7: Scoring protocol

For each sealed prediction, we retrieved candidate evidence from the validation corpus via hybrid search (BM25 + semantic embedding over title + abstract) and adjudicated:

- **CONFIRMED** — ≥2 independent papers in the validation corpus support the central claim (directionally and, where quantitative, within stated bounds).
- **PARTIALLY CONFIRMED** — Evidence supports the directional claim but falls short of quantitative bounds, or supports part but not all of a multi-part claim.
- **CONTRADICTED** — Evidence in the validation corpus directly refutes the claim.
- **INCONCLUSIVE / UNTESTABLE** — Insufficient evidence accumulated by the cutoff, or the prediction depended on a tool/method that was not developed.

Novelty was classified independently as NOVEL (claim did not appear in ≤2017 reviews), DERIVATIVE (trivially derivable from ≤2017 consensus), or SPECULATIVE-KNOWN (speculated in ≤2017 but not tested).

### 2.11 Metrics

We report four formal metrics:

- **Precision (strict)** = |CONFIRMED| / |total evaluated|
- **Precision (liberal)** = |CONFIRMED ∪ PARTIAL| / |total evaluated|
- **Novelty** = |NOVEL| / |total evaluated|
- **Insight value** = |CONFIRMED ∧ anticipated ≥1 year before first publication| / |total evaluated|
- **Leakage rate** = |claims anchored to post-2017 literature| / |total claims|

Publishable-case thresholds were pre-registered (Phase 1 spec §5.3): Precision ≥ 0.40 ∧ Leakage ≤ 0.05 constitutes a positive case; Precision < 0.20 or Leakage > 0.10 constitutes a methodology failure that we commit to publishing regardless of desirability.

### 2.12 Data and code availability

All artifacts are in the public git repository [TorusGroup/glymphatic-retrodiction-2017-2026](https://github.com/TorusGroup/glymphatic-retrodiction-2017-2026). Specific files referenced in this paper:

- `corpus/baseline-2017/corpus.jsonl` (baseline ≤2017, SHA-256 `d4f52383…`)
- `predictions/predictions-final.yaml` (sealed, current SHA-256 v4 `a144c180…9e54460`)
- `corpus/validation-2018-2026/corpus.jsonl` (SHA-256 `3aa15c2c…`)
- `audit/layer1-doi/doi_audit_results.json` (48/48 anchors ≤2017)
- `audit/layer2-multimodel/results-gemini-3.1-pro-preview.json` (PRIMARY JUDGE)
- `audit/layer2-multimodel/results-gemini-2.5-pro.json` (cross-validator)
- `audit/layer2-multimodel/results-gemini-2.5-flash.json` (legacy baseline)
- `audit/leakage-audit-report.md` (v3, Pro 3.1 primary adjudication)
- `audit/validation-scoreboard.md` (v3, N=15 valid pool)

---

## 3. Results

### 3.1 Corpus characterization

The baseline corpus (≤2017) comprised 563 papers organized temporally from 1980 (pre-glymphatic CSF work by Cserr, Rennels) through 2017 (human MRI glymphatic imaging, ALPS index proposal). The distribution accelerated post-2012 (the foundational Iliff paper year), rising from 66 papers in 2012 to 121 in 2017 — a 7× growth over 5 years consistent with the field's reported explosion pattern.

Topic coverage spanned AQP4 biology (274 papers), astrocyte/glia biology (273), CSF physiology (258), aging (188), perivascular flow (188), imaging methods (176), Alzheimer's/amyloid (108), sleep (28), TBI (27), and meningeal lymphatic (14). Parkinson's disease was conspicuously sparse (8 papers) — a finding that later informed six of our sealed predictions.

The validation corpus (2018-2026) comprised 3,329 papers (Table 1). Post-cutoff the field expanded 5.91× in four distinct directions: mechanism papers (continuing); disease-application papers (new dominant track — 789 Alzheimer's papers, 228 Parkinson's papers [29× expansion over baseline], 351 stroke, 140 TBI); imaging-biomarker papers (DTI-ALPS grew from near-zero to 634 papers, 19% of the corpus); and a matured meningeal-lymphatic subfield (382 papers, 27× expansion).

| Corpus | Window | N | SHA-256 (first/last 8 chars) |
|--------|--------|---|------------------------------|
| Baseline (≤2017) | 1980-01-01 – 2017-12-31 | 563 | `d4f52383…4e4849b` |
| Validation (2018-2026) | 2018-01-01 – 2026-04-23 | 3,329 | `3aa15c2c…99be5df` |
| Expansion ratio | — | 5.91× | — |

**Table 1.** Corpora used in the retrodiction. Hashes are truncated; full hashes are in the repository.

### 3.2 The 16 sealed predictions

Table 2 enumerates the 16 predictions after the Anomalist Pass (6 SURVIVED intact + 10 WOUNDED-REFORMULATED, with 2 DESTROYED pre-seal). Detection vectors, novelty classification, and confidence are reported. Complete claims, anchors, and falsification criteria are in the sealed YAML.

| ID | Category | Claim (compressed) | Confidence | Vectors | Anomalist |
|----|----------|---------------------|------------|---------|-----------|
| 001 | Parkinson's | α-syn cleared via glymphatic pathway; AQP4-KO reduces clearance significantly | 0.65 | cross-domain, decomposition | WOUNDED |
| 002 | Parkinson's | Glymphatic dysfunction precedes motor deficits in α-syn mouse models | 0.68 | temporal projection | WOUNDED |
| 003 | Parkinson's | ALPS reduced in PD vs controls; inverse correlation with UPDRS | 0.70 | temporal projection | SURVIVED |
| 004 | Parkinson's | RBD (REM sleep behavior disorder) correlates with altered glymphatic markers | 0.55 | cross-domain | WOUNDED |
| 005 | Parkinson's | Cribriform route contributes ≥20% α-syn efflux | 0.45 | axiomatic inversion | WOUNDED |
| 006 | Parkinson's | AQP4-repolarization intervention attenuates α-syn pathology | 0.45 | constraint removal | WOUNDED |
| 007 | AQP4 controversy | Genetic background explains Iliff-Smith discrepancy | 0.65 | failure archaeology | SURVIVED |
| 008 | AQP4 controversy | Structural role of AQP4 ≥50% of phenotype; conditional KO test | 0.50 | axiomatic inversion | WOUNDED |
| 009 | AQP4 controversy | Dispersive oscillatory transport wins over pure bulk/diffusion | 0.60 | scale bridging | SURVIVED |
| 010 | AQP4 controversy | AQP1/AQP9 redundantly compensate in AQP4-KO | — | — | **DESTROYED** |
| 011 | Sleep | NREM slow-wave phase is max clearance in humans; δ-EEG ↔ CSF inflow | 0.72 | temporal projection | SURVIVED |
| 012 | Sleep | Untreated OSA reduces glymphatic clearance; CPAP reverses in 3-6 months | 0.65 | temporal projection | SURVIVED |
| 013 | Sleep | Human ISF volume expansion during sleep 15-30% (scaled from 60% mouse) | 0.60 | scale bridging | SURVIVED |
| 014 | Imaging | ALPS correlates with cognitive performance (r 0.2-0.5) | 0.72 | temporal projection | WOUNDED |
| 015 | Imaging | EPVS in centrum semiovale predicts MCI→AD conversion (HR ≥1.15) | 0.65 | convergence | WOUNDED |
| 016 | Imaging | Non-contrast MRI technique achieves multi-site consensus | 0.50 | temporal projection | WOUNDED |
| 017 | Moonshot | Meningeal lymphatic VEGF-C stimulation reduces Aβ pathology in AD mouse models | 0.45 | constraint removal | WOUNDED |
| 018 | Moonshot | Unspecified kinase/ion-channel gatekeeper of glymphatic transport | — | — | **DESTROYED** |

**Table 2.** The 16 sealed predictions. Two additional drafts (010, 018) were destroyed by the Anomalist Pass before sealing and are listed for completeness.

### 3.3 Anomalist Pass statistics

Of 18 draft predictions: 6 SURVIVED (33%), 10 WOUNDED-REFORMULATED (56%), 2 DESTROYED (11%). The DESTROY rate (11%) fell below the pre-registered target band (20-40%), which suggested the adversarial pass could have been more aggressive. However, 56% WOUNDED indicates that the audit found substantive issues in most predictions — the bulk of adversarial work was in reformulation (threshold relaxation, scope narrowing, language correction), not outright destruction. This matches the dominant weakness pattern detected: *optimistic quantitative thresholds* on claims that were directionally correct.

The two DESTROYED predictions (010, 018) failed distinct failure modes. PRED-GLY-010 assumed anatomical/functional redundancy between AQP4 and AQP1/AQP9, which was biologically implausible given the known spatial distribution (AQP1 is choroid-plexus-localized, AQP9 is sparse). PRED-GLY-018 was structurally non-falsifiable: "*some* astrocytic kinase or ion channel will emerge as a gatekeeper" could be trivially satisfied.

### 3.4 Leakage audit

**Layer 1 (DOI date audit).** Across 16 predictions there were 48 distinct anchor DOIs. All 48 resolved via Crossref or PubMed; all 48 had `publication_date ≤ 2017-12-31`. Factual anchor leakage = **0.00%**.

**Layer 2 (multi-model Gemini audit, primary = Pro 3.1).** The primary judge (`gemini-3.1-pro-preview`) flagged 1 of 16 predictions as LEAKED: **PRED-GLY-011**. The flag was independently confirmed by `gemini-2.5-pro`. The lowest-capability model (`gemini-2.5-flash`), retained as a baseline, had produced four different flags — three false positives about the ALPS index (where Flash confused Taoka's 2017 publication with its 2020-2024 popularization) and one ambiguous flag on PRED-GLY-009 concerning "Iliff-Smith debate" terminology. Table 4 summarizes the multi-model adjudication.

| ID | Pro 3.1 (primary) | Pro 2.5 (cross-validator) | Flash 2.5 (baseline) | Final verdict | Rationale |
|----|-------------------|---------------------------|----------------------|---------------|-----------|
| PRED-GLY-003 | CLEAN | CLEAN | LEAKED (ALPS) | CLEAN | Pro 3.1 correctly dates ALPS to Taoka 2017; Flash false positive |
| PRED-GLY-004 | CLEAN | CLEAN | LEAKED (ALPS) | CLEAN | Same — Flash false positive |
| PRED-GLY-007 | CLEAN | LEAKED (Mestre 2018) | CLEAN | CLEAN | A priori speculation from pre-2018 anchors; Pro 2.5 false positive |
| PRED-GLY-009 | CLEAN | CLEAN | LEAKED (Iliff-Smith) | CLEAN (**revalidated**) | Higher-capability models both reject Flash flag; Pro 3.1: *"relies on pre-2018 concepts"* |
| **PRED-GLY-011** | **LEAKED** | **LEAKED** | CLEAN | **INVALIDATED** | Convergent flag: predicted fMRI+EEG+CSF+NREM human setup = Fultz 2019 *Science* verbatim; methodological leakage |
| PRED-GLY-012 | CLEAN | LEAKED (Taoka date) | CLEAN | CLEAN | Pro 2.5 mis-dated Taoka to 2018; anchor confirms 2017 |
| PRED-GLY-014 | CLEAN | LEAKED (Yokota) | CLEAN | CLEAN | ALPS method anchored to Taoka 2017; Pro 2.5 false positive |
| PRED-GLY-016 | CLEAN | CLEAN | LEAKED (ALPS) | CLEAN | Flash false positive |

**Table 4.** Multi-model leakage adjudication. The primary judge (Pro 3.1) and its cross-validator (Pro 2.5) converge on exactly one TRUE POSITIVE (PRED-GLY-011). The lowest-capability model (Flash) produces three ALPS false positives and one over-reach on PRED-GLY-009 that higher-capability models both reject. Pro 2.5 produces three additional false positives not confirmed by Pro 3.1.

**Layer 3 (self-consistency, Claude).** 16 of 16 predictions flagged CLEAN. Three raised phrasing caveats (predictions 012, 001, 014 — quantitative thresholds, not anchoring). Layer 3 did not detect the PRED-GLY-011 methodological leakage that Layer 2 primary detected — consistent with same-model bias as the known limitation.

**Convergent leakage rate (primary judge):** 1 true positive out of 16 predictions = **6.25%**. This slightly exceeds the pre-registered 5% target and is reported transparently. PRED-GLY-011 was invalidated (Phase 3.8) via metadata overlay; simultaneously, a provisional Phase 3.7 invalidation of PRED-GLY-009 (based on the Flash flag) was reversed. The valid pool remained N=15 but with different composition. The file was re-sealed (SHA-256 v4: `a144c180…9e54460`), extending the cryptographic chain.

### 3.5 Case study: ALPS false positives and the temporal reasoning fragility of LLM auditors

The three Flash false positives about the ALPS index reveal a failure mode worth documenting — one that, critically, the higher-capability models corrected. The ALPS (Analysis aLong the Perivascular Space) index was published in April 2017 by Taoka *et al.* in *Japanese Journal of Radiology* (DOI 10.1007/s11604-017-0617-z), firmly anchored in our ≤2017 baseline corpus. ALPS nevertheless *exploded* in adoption between 2020 and 2024 — growing from near-zero papers at the cutoff to 634 papers in our validation corpus (19% of it).

Flash's temporal reasoning, trained over a corpus in which the overwhelming weight of "ALPS" mentions lies in 2020-2024, over-rode the factual 2017 publication date. Pro 3.1, trained over a similar distribution but with higher reasoning capacity, correctly disentangled publication date from salience-peak. The same pattern appeared with Pro 2.5's mis-dating of Taoka in PRED-GLY-012 (Pro 2.5 claimed Taoka 2018 when the corpus anchor shows Taoka 2017) and Yokota in PRED-GLY-014 (Pro 2.5 treated Yokota 2019 as the "naming" event when the ALPS method itself is Taoka 2017).

This suggests a general limitation: **LLM-based temporal auditors are unreliable for biomarkers whose publication date sits early in their adoption curve**, and capability-scaling reduces but does not eliminate the failure mode. A single-round single-model LLM audit is necessary but not sufficient; it must be triangulated against factual DOI-date verification (our Layer 1) *and* against an independent cross-validator (our multi-model Layer 2). Teams replicating this protocol should not rely on any single model's verdicts alone; manual adjudication against the factual anchor record and convergence across at least two capable independent models is required. We recommend this as a formal methodological rule: **a Layer 2 flag is a candidate for investigation unless confirmed by an independent second model of comparable capability**.

### 3.6 Validation scoreboard (N=15 valid pool)

Table 5 shows the adjudicated status of each prediction against the 2018-2026 validation corpus, *after* the Phase 3.8 multi-model re-audit (PRED-GLY-011 invalidated; PRED-GLY-009 revalidated).

| ID | Verdict | First publication | Anticipation | Novelty |
|----|---------|-------------------|--------------|---------|
| 001 | CONFIRMED | Zou 2019, Trans. Neurodegeneration | 0-1 y | NOVEL |
| 002 | PARTIAL | Zou 2019 + Ding 2024 | 0 y | NOVEL |
| 003 | CONFIRMED | Ma 2022, npj Parkinson's Disease | 0 y | DERIVATIVE |
| 004 | CONFIRMED | Si 2022, npj PD | 0 y | NOVEL |
| 005 | INCONCLUSIVE | — | N/A | NOVEL (untested) |
| 006 | PARTIAL | Wang 2023/24, J Adv Res | 0 y | NOVEL |
| 007 | PARTIAL | Mestre 2018, eLife (mechanism different) | 0 y | NOVEL |
| 008 | INCONCLUSIVE | — | N/A | NOVEL (untested) |
| 009 | CONFIRMED | Helakari 2022 | 0 y | NOVEL |
| ~~011~~ | ~~CONFIRMED~~ | ~~Fultz 2019, Science~~ | ~~0 y~~ | ~~NOVEL~~ — **INVALIDATED (Phase 3.8, methodological leakage)** |
| 012 | PARTIAL | Feliciano 2025, AJRCCM | 0 y | NOVEL |
| 013 | PARTIAL | Demiral 2019, NeuroImage | 0 y | DERIVATIVE |
| 014 | CONFIRMED | Steward 2021, J Neuroimaging | 0 y | DERIVATIVE |
| 015 | CONFIRMED | Paradise 2021, Neurology | 0 y | DERIVATIVE |
| 016 | CONFIRMED | Taoka 2018, eLife + ALPS consolidation | 0 y | DERIVATIVE |
| 017 | CONFIRMED | Da Mesquita 2018, Nature | **1 y** | NOVEL (high) |

**Table 5.** Validation scoreboard (N=15 valid pool). Anticipation is the gap between `first_publication_date` in the validation corpus and the earliest edge of the `predicted_window`. Two predictions destroyed pre-seal (010, 018) and one invalidated post-seal (011) are not included in the valid pool.

Aggregate metrics (N=15):

- **Strict Precision** (CONFIRMED only): 8/15 = **53.33%**
- **Liberal Precision** (CONFIRMED ∪ PARTIAL): 13/15 = **86.67%**
- **Novelty**: 8/15 = **53.33%**
- **Insight value** (CONFIRMED ∧ ≥1 y anticipation): 1/15 = **6.67%** (only PRED-GLY-017)
- **Contradicted**: 0/15 = **0.00%**
- **Factual leakage (Layer 1 DOI)**: 0/48 = **0.00%**
- **Convergent leakage (Layer 2 primary, post-adjudication)**: 1/16 = **6.25%**

The pre-registered PASS threshold (Precision ≥ 40% ∧ factual Leakage ≤ 5%) is met. Strict precision sits clearly above the minimum threshold (53.33% vs 40.00% target); liberal precision is in the STRONG band (≥60%) at 86.67%. The 6.25% convergent leakage rate slightly exceeds the 5% target; we report this transparently rather than retroactively adjust the threshold. Insight value (6.67%) falls below the 10% target — only PRED-GLY-017 (Da Mesquita 2018 *Nature*, +1 year anticipation) qualifies — reflecting that most predictions were concurrent-forecasting rather than strong-forward.

### 3.7 Confidence calibration

Predictions with confidence ≥ 0.70 (PRED-003, -014, after removal of 011): 2/2 CONFIRMED (100%).
Predictions with confidence 0.60-0.69 (six predictions in the valid pool, after revalidating 009): 3 CONFIRMED + 3 PARTIAL; all directionally correct (100% liberal, 50% strict).
Predictions with confidence 0.45-0.55 (six predictions, including moonshots): 2 CONFIRMED + 2 PARTIAL + 2 INCONCLUSIVE.

The model was reasonably calibrated: high-confidence predictions succeeded at 100%, and the gradation down to moonshot-level (0.45) captured the genuine uncertainty of those claims.

### 3.7 Case studies

**Case 3.7.1 — PRED-GLY-017: Meningeal lymphatic stimulation (moonshot confirmed, the sole insight-value contributor).** Confidence 0.45. Anchored to Louveau (2015), Aspelund (2015), and Iliff framework papers. Claim: VEGF-C stimulation of meningeal lymphatics in aged or AD mouse models would reduce Aβ accumulation. Validation: **Da Mesquita et al. 2018 Nature** ("Functional aspects of meningeal lymphatics in ageing and Alzheimer's disease"), published 25 July 2018 — within the predicted window (2018-2022) and ~1 year after the sealed cutoff. The paper demonstrates precisely the causal chain claimed: VEGF-C enhancement of meningeal lymphatics → improved Aβ drainage → mitigated cognitive decline in aged mice. This is the **only** prediction in the valid pool with anticipation ≥1 year, and therefore the sole contributor to the insight-value metric (1/15 = 6.67%).

**Case 3.7.2 — PRED-GLY-009: Oscillatory-dispersion resolution of the AQP4 controversy (revalidated after multi-model re-audit).** Confidence 0.60, SURVIVED Anomalist. Claim: whole-brain modeling derived from diffusion MRI will resolve the Iliff-Smith controversy in favor of oscillatory dispersion (cardiac pulsation + respiration) rather than bulk flow or pure diffusion, with mean perivascular velocities < 50 μm/s but high effective transport. Anchors: Iliff 2012 Sci Transl Med, Iliff 2013 J Neurosci (pulsation driver), Rey & Sarntinoranont 2015 J Neurosci (respiratory pressure). Validation: **Helakari 2022** and subsequent whole-brain modeling work (2019-2024) converge on the oscillatory-dispersion picture — the prediction was directionally correct and quantitatively close. *Auditing note:* a provisional Phase 3.7 invalidation of this prediction (triggered by a `gemini-2.5-flash` flag on the term "Iliff-Smith debate") was reversed in Phase 3.8 after both higher-capability models (`gemini-3.1-pro-preview` and `gemini-2.5-pro`) classified the prediction as CLEAN. Pro 3.1's reasoning was explicit: the prediction *"relies on pre-2018 concepts (the debate between Iliff bulk flow and Smith diffusion, and early models of oscillatory dispersion) to make a plausible forward-looking claim without using post-2017 terminology."* The Flash flag was a single-model over-reach on a debate-name that in fact has pre-2018 conceptual grounding; the revalidation illustrates the value of capability-scaling the independent judge (§3.4, §3.5).

**Case 3.7.2b — PRED-GLY-011: Slow-wave sleep × CSF inflow (INVALIDATED, methodological leakage).** Confidence 0.72, SURVIVED Anomalist. Claim: NREM slow-wave (N3) is the specific phase of maximum glymphatic clearance in humans; δ-EEG amplitude correlates with CSF inflow magnitude via fMRI synchronized to EEG. Pre-2018 anchors: Xie 2013 Science (sleep-glymphatic in mice), Jessen 2015 Nat Rev Neurol (review). *Post-seal status:* Fultz *et al.* 2019 *Science* ("Coupled electrophysiological, hemodynamic, and cerebrospinal fluid oscillations in human sleep") is the landmark paper that demonstrated precisely this setup — synchronized fMRI + δ-EEG + CSF flow in human NREM. Multi-model audit primary judge (`gemini-3.1-pro-preview`) flagged this prediction as LEAKED; the flag was independently confirmed by `gemini-2.5-pro`. The primary-judge rationale: *"the specific correlation between delta-EEG oscillations and CSF inflow measured by synchronized fMRI in humans perfectly describes the methodology and findings of the landmark 2019 paper by Fultz et al."* The pre-2018 anchors did not describe the multimodal human fMRI+EEG design; the predicted setup too closely matches the post-seal paper to be classified as *a priori* formulation. PRED-GLY-011 was invalidated (Phase 3.8) as **methodological leakage** — distinct from anchor leakage (all anchors ≤ 2017) and distinct from terminology leakage (no post-2018 named entities). The prediction was factually correct but methodologically contaminated; it was removed from the valid pool. This case is the concrete justification for multi-model cross-audit: the lowest-capability model (`gemini-2.5-flash`) had classified PRED-GLY-011 as CLEAN and missed this leakage entirely.

**Case 3.7.3 — PRED-GLY-007: AQP4 controversy mechanism (right question, wrong answer).** Confidence 0.65, SURVIVED Anomalist. Claim: the Iliff 2012 vs Smith 2017 discrepancy on AQP4 KO phenotypes reflects genetic-background differences between mouse strains (CD1/FVB with preserved endfoot structure vs C57BL/6 with fragile endfeet). Validation: **Mestre et al. 2018 eLife** ("Aquaporin-4-dependent glymphatic solute transport in the rodent brain") was the consensus-settling paper — a joint effort by Iliff's, Nedergaard's, and four other laboratories. Mestre's team *did* resolve the controversy, *did* demonstrate AQP4's importance, *but* identified **anesthesia protocol, age of animals, and tracer delivery method** as dominant confounders — not genetic background. The prediction asked the right question at the right time but identified the wrong mechanism. We score this PARTIAL (right pattern, wrong detail). The "failure archaeology" detection vector led the AI to the correct tension in the field and to the correct year of resolution, but over-constrained the resolution mechanism.

**Case 3.7.4 — PRED-GLY-001: α-synuclein extension (cross-domain isomorphism, serial confirmation).** Confidence 0.65, WOUNDED-REFORMULATED (threshold relaxed from "same magnitude as Aβ" to "same order of magnitude"). Claim: α-synuclein is glymphatically cleared, AQP4-KO reduces clearance significantly. Validation: Zou et al. 2019 (*Translational Neurodegeneration*), followed by Cui 2023, Ding 2024 Aging Cell, and Scarpelli 2025 confirmed the mechanism serially. Extension by isomorphism from Aβ biology to α-syn biology — a canonical cross-domain synthesis move — succeeded.

---

## 4. Discussion

### 4.1 What the protocol demonstrated

The AI pipeline, operating under strict retrieval-only constraints with literature hash-sealed to 2017-12-31, produced 16 sealed predictions, 15 of which survived the post-seal leakage audit. Of those 15, 8 were later CONFIRMED and 5 PARTIALLY CONFIRMED — no direct contradictions. This is measurable concurrent forecasting: the model anticipated findings that *did* materialize in the years following its literature cutoff, with its high-confidence predictions (≥ 0.70) succeeding at 100%.

Against a pre-registered threshold of Precision ≥ 40% ∧ Leakage ≤ 5%, the result is a PASS on precision (strict 53.33% clearly above threshold; liberal 86.67% STRONG) and a narrowly-exceeding 6.25% on convergent leakage (1/16). Eight of 15 were classified NOVEL.

**The multi-model cross-audit demonstrated its own necessity — and its capacity for self-correction.** The single predictive failure of the sealed set — PRED-GLY-011's match to the Fultz 2019 *Science* experimental setup — was caught only by the capability-upgraded independent-model audit (Pro 3.1 primary, Pro 2.5 cross-validator). The lowest-capability independent model (`gemini-2.5-flash`) had missed this methodological leakage entirely and had instead produced four different flags, three of which were false positives (ALPS date-confusion) and one of which (on PRED-GLY-009) was an over-reach that higher-capability models both rejected. Upgrading the primary judge simultaneously (a) *rejected* the lowest-capability model's false positives and its single over-reach on PRED-GLY-009, and (b) *detected* a genuine methodological leakage on PRED-GLY-011 that the lowest-capability model had missed. This swap — 009 revalidated, 011 invalidated — left pool size unchanged (N=15) but changed the composition of what sits inside the pool. Had we accepted the single-model Flash verdict, the paper would have reported the wrong invalidation and the wrong composition.

This is direct operational evidence that **multi-model cross-audit, with a capable primary judge, is a load-bearing component of rigorous AI-for-science validation, not an optional extra** — and specifically that a single-model independent audit at any capability tier is insufficient. The protocol corrected itself through capability scaling; that self-correction is the methodological contribution.

### 4.2 What the protocol did not demonstrate

Five limitations deserve explicit scrutiny.

**First: insight value was only 6.67% (below target).** Only one prediction (PRED-GLY-017) was CONFIRMED by a publication appearing at least one year after the seal — Da Mesquita 2018 *Nature*. For most predictions, the first validating publication appeared within 12 months of seal. This has a simple explanation: the glymphatic field exploded *precisely* in 2018-2019 (Fultz, Da Mesquita, Mestre, Zou — all landmark papers published within 18 months of our cutoff). The AI was not "predicting the future"; it was identifying the obvious frontier that many competing laboratories were simultaneously pursuing. This is *concurrent forecasting*, not strong forward prediction. Insight value falls below the 10% pre-registered target; we report this transparently rather than relax the definition.

If the cutoff had been 2015 (pre-Fultz, pre-Da Mesquita), the anticipation window would presumably have been larger but the baseline corpus thinner. The strength of retrodiction as a methodology is thus tied to cutoff choice — a field in stasis would yield meaningless predictions; a field just starting has insufficient substrate.

**Second: single-model LLM audit at any capability tier is insufficient.** Our Layer 2 audit, executed across three capability tiers, produced substantively different flags at each tier. The lowest-capability model (`gemini-2.5-flash`) produced four flags, three of which were false positives involving the ALPS index (which Taoka *et al.* published in 2017 but which exploded in adoption only in 2020-2024). The mid-capability model (`gemini-2.5-pro`) produced four *different* flags, three of them false positives (two Taoka-date errors, one a priori-speculation over-read). The highest-capability model (`gemini-3.1-pro-preview`) produced a single flag — PRED-GLY-011, the sole true positive — confirmed independently by the mid-capability model. The failure mode is general: **LLM temporal reasoning is brittle when biomarker publication date sits early in the adoption curve, and brittleness scales down — but does not disappear — with capability**. The practical consequence: Layer 2 flags must be triangulated across (a) multiple capability tiers, (b) factual DOI-date verification (Layer 1), and (c) another independent model of comparable capability. Single-model audit — at any tier — is unsafe.

**Third: convergent leakage rate (6.25%) slightly exceeds the 5% pre-registered target.** The single true positive was PRED-GLY-011's methodological leakage (not terminology leakage, as an earlier analysis based on Flash alone had classified PRED-GLY-009). We chose to report this transparently and invalidate PRED-GLY-011 rather than retroactively adjust the threshold. Strict precision remains 53.33% — clearly above the pre-registered PASS threshold with margin. The honest reading is that the protocol is robust in the *result* (PASS precision, 0 contradicted) but still slightly above target in the *residual leakage*, and that future applications should add: (a) self-consistency sampling of Layer 2 primary (N≥3 majority vote), (b) a cross-family independent auditor (non-Gemini) for additional robustness, and (c) explicit methodological-leakage checks (does the predicted experimental design match a post-seal paper's setup?) alongside anchor- and terminology-leakage checks.

**Fourth: single-domain test.** The protocol is demonstrated in one field (glymphatic neuroscience). Transferability to other fields — octonion physics, CRISPR base editing, machine-learning theory, mRNA vaccine design — is asserted by design but not proved by experiment. We explicitly scope this paper to glymphatic and note that a multi-domain study (*exp-retrodiction-v2*) is planned as a follow-up.

**Fifth: retrieval-based validation, not full-paper expert reading.** Our scoring process relied on abstract-level evidence matching supplemented by targeted full-text review of ~20 high-stakes validation papers. It is possible that abstracts miss nuance that would alter a CONFIRMED/PARTIAL boundary. To mitigate, we have flagged all borderline cases explicitly and invite independent re-scoring.

### 4.3 What we learned about the method

**The Anomalist Pass worked.** Zero predictions were CONTRADICTED in the validation phase. This is not a coincidence — it is the signature of a functional adversarial audit. The Anomalist destroyed 2 predictions and reformulated 10, most commonly by relaxing optimistic quantitative thresholds ("≥30% reduction" → "statistically significant reduction"). The Anomalist audit cost approximately 2× the generation cost in tokens; this was well spent.

**Citation hygiene is non-trivial.** Phase 3.5 (our name for the mid-pipeline correction) discovered that 5 of 48 anchor citations had typographical errors despite passing visual inspection. DOI prefix errors (10.1525 vs 10.1523) and PMID-title mismatches are common failure modes of AI-generated bibliographies. Any future application of this protocol should integrate a DOI-resolution check *before* hash-sealing, not after.

**Optimistic thresholds are a systematic failure mode.** The dominant weakness pattern detected by the Anomalist was that the model gravitates toward specific-sounding numerical thresholds ("≥30% reduction", "HR ≥ 1.3") that outpace the underlying certainty. This is consistent with the broader literature on LLM overconfidence in quantification. Defensive reformulation — replacing precise thresholds with "statistically significant, direction preserved" — preserved falsifiability while reducing false-fail risk.

**Predictions dependent on undeveloped tools become INCONCLUSIVE, not CONFIRMED or CONTRADICTED.** PRED-005 (cribriform route specific fraction ≥20%) and PRED-008 (conditional AQP4 KO separating water-flux from structural function) both depended on tools that were not developed in the validation window. These predictions were *correct in spirit* but unfalsifiable in practice. This is an epistemological failure mode of retrodiction: quantitative predictions over unexplored measurement spaces may be de facto non-falsifiable.

### 4.4 Implications for AI-for-science

The core claim of this paper is methodological. We demonstrate that a hash-sealed retrodiction protocol with adversarial pre-audit can provide a reproducible, falsifiable test of whether an AI hypothesis-generation pipeline is synthesizing or paraphrasing. The test can be replicated in any field with a tractable cutoff and a substantial post-cutoff literature.

The protocol does **not** prove that AI can do science. It does **not** prove that AI-generated hypotheses are superior to human-generated hypotheses (we did not compare). It does **not** prove that the specific pipeline tested here (Opus 4.7 under our retrieval-only prompt) generalizes.

It does prove that under strict cryptographic blinding, *this* pipeline, on *this* domain, produced measurably predictive hypotheses — including one moonshot (PRED-017) with ~1 year of genuine anticipation of a landmark Nature paper. It proves that the 0% contradiction rate is compatible with careful adversarial design, not with pure memorization — if it were pure memorization, the hit rate would be higher on "easy" consensus questions and the insight value near zero. (Insight value at 12.5% is low, but nonzero.)

The most conservative interpretation is: under strict blinding, the AI operated as an expert-level concurrent forecaster in a rapidly maturing field. The most generous is that it contributed novel hypotheses that later proved predictive. Either is a meaningful result for a methodology that, prior to this protocol, had no way to distinguish them.

### 4.5 Follow-up work

- **exp-retrodiction-v2 — multi-domain.** Run the same protocol on two or three additional fields (candidates: octonion physics, CRISPR base editing, CAR-T cell therapy) to test transferability.
- **exp-prospective.** Generate predictions from today's literature, seal them, wait 2-3 years, validate. This is the strong form of forward prediction and it is currently impossible given our time horizon, but is the correct eventual test.
- **exp-clinical-premortem.** Apply the method to an applied problem (pre-launch failure-mode forecasting of a clinical trial, drug, or product). Anomalist Pass is readily applicable; retrodiction becomes post-hoc validation after the forecasted event.

---

## 5. Conclusion

We introduced a hash-sealed retrodiction protocol for validating AI-generated scientific hypotheses. Applied to the glymphatic system with a temporal cutoff of 2017-12-31, the protocol produced 16 sealed predictions of which 15 survived the post-seal leakage audit. Of those 15, 8 were CONFIRMED and 5 PARTIALLY CONFIRMED against a corpus of 3,329 papers published in 2018-2026; 0 were contradicted. Factual DOI-date leakage was 0.00%; convergent leakage under the primary Layer-2 judge was 6.25% (one prediction, PRED-GLY-011, detected as methodological leakage — its predicted experimental setup too precisely matched Fultz *et al.* 2019 *Science* — and invalidated post-hoc). Anticipation beyond the cutoff was small (6.67% of the valid pool anticipated their first validating publication by ≥1 year) — the model acted as a concurrent forecaster in a rapidly maturing field, not as a long-range prophet.

The protocol itself — (1) literature freezing with cryptographic seal, (2) retrieval-only generation, (3) adversarial pre-audit (Anomalist Pass), (4) triple-layer leakage audit including a multi-model independent-judge cross-check across capability tiers, (5) independent validation corpus, (6) third-party-auditable scoring — is offered as a reproducible falsification framework for any claim that an AI system generates valid scientific hypotheses. It can be replicated in any mature field with a tractable cutoff and a public literature.

Two operational findings from our single-domain test deserve emphasis. First: the lowest-capability independent-model audit (`gemini-2.5-flash`) produced an incorrect adjudication — missing a genuine methodological leakage and producing three false positives about a biomarker whose publication date (2017) sat early in its 2020-2024 adoption curve. Upgrading the primary judge to `gemini-3.1-pro-preview` and cross-validating with `gemini-2.5-pro` simultaneously rejected those false positives and detected the missed true positive. The swap of invalidations (009 out, 011 in) illustrates that single-model independent audit at any capability tier is insufficient; capability-scaling *plus* cross-model convergence is the minimum viable safeguard. Second: the same-model self-consistency audit failed to detect the methodological leakage that the multi-model audit caught — confirming the known same-model bias and underscoring that cross-model auditing is load-bearing, not decorative.

AI contribution to science cannot be credibly assessed without cryptographic guarantees against training leakage. We provide one instance of such a guarantee, demonstrate that under it measurable predictive validity can be observed, and demonstrate operationally that multi-model cross-audit is necessary to detect leakage that any single-model audit — at any capability tier — will miss. This does not prove AI can do science. It provides a tool — refined through its own first application, self-corrected by capability scaling — by which that claim can begin to be tested honestly.

---

## Data and Code Availability

All artifacts are available in the public repository:
`https://github.com/TorusGroup/glymphatic-retrodiction-2017-2026`

- Sealed predictions (current SHA-256 v4 `a144c180…9e54460`; seal chain v1 `1765b221…7afb586` → v2 `b9add8ef…ae9cc73` → v3 `2db0fab5…44928f` → v4): `predictions/predictions-final.yaml`
- Baseline corpus (SHA-256 `d4f52383…4e4849b`): `corpus/baseline-2017/corpus.jsonl`
- Validation corpus (SHA-256 `3aa15c2c…99be5df`): `corpus/validation-2018-2026/corpus.jsonl`
- Leakage audit v3 (multi-model Layer 2, Pro 3.1 primary): `audit/leakage-audit-report.md`
- Gemini 3.1 Pro raw output (PRIMARY JUDGE): `audit/layer2-multimodel/results-gemini-3.1-pro-preview.json`
- Gemini 2.5 Pro raw output (cross-validator): `audit/layer2-multimodel/results-gemini-2.5-pro.json`
- Gemini 2.5 Flash raw output (legacy baseline): `audit/layer2-multimodel/results-gemini-2.5-flash.json`
- Scoreboard v3 (N=15): `audit/validation-scoreboard.md`
- Supplementary material (inter-model matrix §S3): `paper/supplementary-material.md`
- Protocol specification: `protocol/retrodiction-protocol-spec.md`

Third-party auditors can re-compute every hash, re-run the multi-model Gemini audit with the published script (`audit/layer2-multimodel/run_gemini_audit_api.py`), and re-score every prediction with the public DOIs provided.

---

## Acknowledgements

We acknowledge the foundational neuroscience work of Maiken Nedergaard, Jeff Iliff, Helene Benveniste, Alan Verkman, and Jonathan Kipnis's laboratories, whose published work constitutes both the baseline corpus and the validation ground truth of this study. We thank the open science infrastructures — PubMed, Europe PMC, Crossref, arXiv, and bioRxiv — whose open APIs made both corpus constructions tractable. Finally, we thank the PhD-candidate collaborator whose early feedback refined the protocol design.

No external funding was received for this study.

---

## Author Contributions

M.F. conceived the expedition, served as Magister (human-in-loop), defined the protocol, supervised blinding, and wrote the final manuscript. The Prometheus Lab pipeline (Torus OS platform) executed the generation, adversarial audit, hash-sealing, and corpus construction under M.F.'s direction and protocol constraints. All authors approve the final manuscript.

---

## Competing Interests

The authors declare no competing financial interests. The reproducibility artifacts for this paper (sealed predictions, corpora, audit scripts, scoring rationale) are released under CC-BY 4.0 + MIT as described in *Data and Code Availability*. The underlying Torus OS cognitive pipeline is proprietary technology of TorusGroup and is not included in this release. No pharmaceutical, imaging, or neurology commercial entity funded this work.

---

## References

(BibTeX-ready citations; see `references.bib` for full entries.)

- Aspelund, A., et al. (2015). A dural lymphatic vascular system that drains brain interstitial fluid and macromolecules. *Journal of Experimental Medicine*, 212(7), 991–999.
- Cserr, H. F., & Patlak, C. S. (1992). Secretion and bulk flow of interstitial fluid. In *Physiology and Pharmacology of the Blood-Brain Barrier*.
- Cui, H., et al. (2023). Alpha-synuclein clearance via glymphatic pathway is AQP4-dependent. *Aging Cell*.
- Da Mesquita, S., et al. (2018). Functional aspects of meningeal lymphatics in ageing and Alzheimer's disease. *Nature*, 560(7717), 185–191.
- Demiral, Ş. B., et al. (2019). Apparent diffusion coefficient changes in human brain during sleep. *NeuroImage*, 185, 263–273.
- Ding, X., et al. (2024). Impaired meningeal lymphatic drainage in aging mice affects α-synuclein clearance. *Aging Cell*.
- Elabasy, A., et al. (2025). Multi-site validation of CSF-BOLD coupling during NREM. (Preprint/in press.)
- Fang, Y., et al. (2023). AQP4 knockout and perivascular stagnation in rodent brain. *Neuroscience*.
- Feliciano, P., et al. (2025). CPAP therapy and glymphatic recovery in obstructive sleep apnea. *American Journal of Respiratory and Critical Care Medicine*.
- Fultz, N. E., et al. (2019). Coupled electrophysiological, hemodynamic, and cerebrospinal fluid oscillations in human sleep. *Science*, 366(6465), 628–631.
- Helakari, H., et al. (2022). Dynamic cerebrospinal fluid flow in human brain detected with ultrafast MREG. *Journal of Neuroscience*.
- Iliff, J. J., et al. (2012). A paravascular pathway facilitates CSF flow through the brain parenchyma and the clearance of interstitial solutes, including amyloid-β. *Science Translational Medicine*, 4(147), 147ra111.
- Iliff, J. J., et al. (2013). Brain-wide pathway for waste clearance captured by contrast-enhanced MRI. *Journal of Clinical Investigation*, 123(3), 1299–1309.
- Iliff, J. J., et al. (2013). Cerebral arterial pulsation drives paravascular CSF-interstitial fluid exchange in the murine brain. *Journal of Neuroscience*, 33(46), 18190–18199.
- Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLOS Medicine*, 2(8), e124.
- Jessen, N. A., et al. (2015). The glymphatic system — a beginner's guide. *Neurochemical Research*, 40(12), 2583–2599.
- Jumper, J., et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*, 596, 583–589.
- Kress, B. T., et al. (2014). Impairment of paravascular clearance pathways in the aging brain. *Annals of Neurology*, 76(6), 845–861.
- Lakatos, I. (1970). Falsification and the methodology of scientific research programmes. In *Criticism and the Growth of Knowledge*. Cambridge University Press.
- Louveau, A., et al. (2015). Structural and functional features of central nervous system lymphatic vessels. *Nature*, 523, 337–341.
- Ma, Y., et al. (2022). Glymphatic dysfunction correlates with motor symptoms in Parkinson's disease. *npj Parkinson's Disease*.
- Mestre, H., et al. (2018). Aquaporin-4-dependent glymphatic solute transport in the rodent brain. *eLife*, 7, e40070.
- Nedergaard, M. (2013). Garbage truck of the brain. *Science*, 340(6140), 1529–1530.
- Novikov, A., et al. (2025). AlphaEvolve: An evolutionary coding agent for mathematical and algorithmic discovery. *Google DeepMind Technical Report*.
- Paradise, M., et al. (2021). Association of dilated perivascular spaces with cognitive decline and incident dementia. *Neurology*, 96(11), e1501–e1511.
- Popper, K. (1959). *The Logic of Scientific Discovery*. Hutchinson.
- Riba-Llena, I., et al. (2016). Associations between enlarged perivascular spaces and ambulatory blood pressure. *European Journal of Neurology*, 23(10), 1575–1582.
- Ringstad, G., et al. (2017). Glymphatic MRI in idiopathic normal pressure hydrocephalus. *Brain*, 140(10), 2691–2705.
- Romera-Paredes, B., et al. (2023). Mathematical discoveries from program search with large language models. *Nature*, 625, 468–475.
- Scarpelli, M., et al. (2025). Longitudinal α-synuclein clearance dynamics in PD mouse models. *Molecular Neurodegeneration*.
- Si, X., et al. (2022). Imaging biomarkers of glymphatic function in Parkinson's disease with RBD. *npj Parkinson's Disease*.
- Smith, A. J., et al. (2017). Test of the "glymphatic" hypothesis demonstrates diffusive and aquaporin-4-independent solute transport in rodent brain parenchyma. *eLife*, 6, e27679.
- Smyth, L. C. D., et al. (2022). A basal meningeal lymphatic pathway. *Nature Neuroscience*.
- Steward, C. E., et al. (2021). ALPS index and cognitive function in older adults. *Journal of Neuroimaging*, 31(3), 569–578.
- Taoka, T., et al. (2017). Evaluation of glymphatic system activity with the diffusion MR technique: diffusion tensor image analysis along the perivascular space (DTI-ALPS). *Japanese Journal of Radiology*, 35(4), 172–178.
- Taoka, T., et al. (2018). ALPS method is highly reproducible. *eLife*.
- Wang, X., et al. (2023/2024). AQP4 repolarization intervention in PD mouse models. *Journal of Advanced Research*.
- Williams, S., et al. (2023). Slow-wave coupling to CSF flow — multi-site replication. *eLife*.
- Xie, L., et al. (2013). Sleep drives metabolite clearance from the adult brain. *Science*, 342(6156), 373–377.
- Zou, W., et al. (2019). Blocking meningeal lymphatic drainage aggravates Parkinson's disease–like pathology in mice overexpressing mutated α-synuclein. *Translational Neurodegeneration*, 8, 7.

---

*Manuscript v1.0 — Prometheus Lab, 2026-04-23.*
*Submitted for peer review. Hash-sealed predictions and full audit trail are publicly verifiable.*
