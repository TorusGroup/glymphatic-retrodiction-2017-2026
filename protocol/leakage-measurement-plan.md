# Leakage Measurement Plan — Public Specification (Sanitized)

> **Expedition:** exp-retrodiction (glymphatic neuroscience 2017-2026)
> **Phase:** Protocol design (pre-seal)
> **Date:** 2026-04-22
> **Release note:** This document describes the leakage taxonomy and the multi-layer detection strategy used in the paper's leakage audit. The specific agent prompts, heuristic thresholds, and detection-agent architecture are proprietary to TorusGroup and are not released. The released artifacts (multi-model Gemini audit results, DOI audit script, per-prediction scoring rationale) are sufficient to verify the reported audit outcomes.

---

## 1. Operational definition of leakage

**Leakage** is the phenomenon of the hypothesis-generation model using knowledge of literature published *after* the temporal cutoff while operating under instruction to rely only on corpus ≤ cutoff.

### 1.1 Leakage taxonomy

Seven detectable leakage types were defined pre-seal:

| Type | Description | Detection difficulty |
|------|-------------|-----------------------|
| **L1** — Direct citation leak | Explicitly cites a paper dated ≥ cutoff+1 | Trivial (automated date verification) |
| **L2** — Paraphrased leak | Paraphrases a post-cutoff finding without citation | Difficult (semantic comparison) |
| **L3** — Terminological leak | Uses terminology that only emerged post-cutoff | Medium (vocabulary lists + independent-model audit) |
| **L4** — Conceptual leak | Post-cutoff concept disguised as synthesis | Difficult (expert-level or multi-model audit) |
| **L5** — Overreach | Claim based on ≤ cutoff citation but extrapolates beyond what the citation supports | Medium (claim-vs-excerpt verification) |
| **L6** — Linguistic leak | Temporal language ("recently", "now known", "emerging") | Trivial (regex) |
| **L7** — Secondary contamination | Cites a pre-cutoff review whose own references include post-cutoff material | Difficult (reference-chain analysis) |
| **L8** — Methodological leak | Predicted experimental design matches a specific post-cutoff paper's setup too precisely to be *a priori* | Hard (requires specific expertise or a capable independent auditor) |

*Note: L8 was added during Phase 3.8 after the multi-model audit detected exactly this pattern in PRED-GLY-011. The original pre-registered plan covered L1–L7.*

### 1.2 Leakage is a quantitative concern

Zero leakage is impossible. The goal is to measure and minimize:

- **Target:** `leakage_rate ≤ 5%` (pre-registered hard gate)
- **Formula:** `leakage_rate = |claims with detected contamination| / |total claims|`
- A "claim" is one distinct factual assertion, typically one per bullet or 1-3 per paragraph.

---

## 2. Multi-layer detection strategy

The audit is organized in three layers, each attacking a different subset of leakage types with a different method:

### Layer 1 — Factual DOI verification

- **Method:** for every anchor DOI in every sealed prediction, resolve via Crossref (primary) and PubMed E-utilities (fallback). A publication date > cutoff counts as an L1 leak.
- **Script:** `audit/layer1-doi/audit_dois.py` (released)
- **Result for this expedition:** 48/48 anchors ≤ 2017, 0% factual leakage
- **Attacks:** L1

### Layer 2 — Independent-model adversarial audit (multi-model)

- **Method:** three Gemini models (primary: `gemini-3.1-pro-preview`, cross-validator: `gemini-2.5-pro`, legacy baseline: `gemini-2.5-flash`) classify each prediction as CLEAN / SUSPECT / LEAKED with free-text reasoning. Flags are adjudicated by convergence across the two most capable independent models plus manual check against Layer 1.
- **Script:** `audit/layer2-multimodel/run_gemini_audit_api.py` (released; accepts any model name)
- **Result for this expedition:** 1 TRUE POSITIVE (PRED-GLY-011, L8 methodological leakage); 3 Flash false positives (ALPS date) and 3 Pro 2.5 false positives rejected by higher-capability models
- **Attacks:** L2, L3, L4, L8

The specific prompt used by each independent-model audit session is embedded in the released script (see `run_gemini_audit_api.py`). This is the audit prompt — the hypothesis-*generation* prompts are separate and remain proprietary.

### Layer 3 — Self-consistency (same-model second pass)

- **Method:** a fresh session of the generation model re-scores each prediction in a leakage-hunter role. This catches some L3/L4 leaks but suffers from same-model bias.
- **Result for this expedition:** 0/16 flagged — confirming the known limitation and reinforcing the necessity of the Layer 2 multi-model cross-audit.
- **Attacks:** L2, L3, L4 (partial, with known limitations)

---

## 3. Convergence rule

A prediction is **invalidated post-seal** when *both*:
1. At least two independent models (Layer 2) flag it with converging rationale, **and**
2. Manual adjudication against Layer 1 (factual DOIs) does not reveal the flag as a false positive.

A prediction is **re-validated post-seal** (reversal of a provisional invalidation) when:
1. The two most capable independent models (Layer 2) both classify it as CLEAN, **and**
2. The flag that drove the original invalidation came from a lower-capability model whose reasoning was subsequently rejected by higher-capability models.

The single-model Flash audit that produced an ambiguous flag on PRED-GLY-009 (leading to a provisional Phase 3.7 invalidation) was reversed in Phase 3.8 under this rule; simultaneously, PRED-GLY-011 was invalidated via the same rule in the opposite direction. See `audit/leakage-audit-report.md` for full adjudication.

---

## 4. Pre-registered publishing rule

If `leakage_rate > 10%` the protocol commits to publishing the result as a methodology failure rather than concealing. The actual measured rate for this expedition is 6.25% (above the 5% target, below the 10% failure threshold) — reported transparently.

---

## 5. Known limitations

- **LLM temporal reasoning fragility**: for biomarkers whose publication date sits early in their adoption curve (e.g., ALPS index, published 2017 but widely adopted 2020-2024), LLM auditors over-weight popularization salience. Capability-scaling reduces but does not eliminate this failure mode — hence the multi-tier audit.
- **Same-model bias**: Layer 3 has known limits and is retained primarily as a sanity check, not as a primary detection mechanism.
- **Methodological leakage (L8)**: was not part of the original pre-registered taxonomy (L1–L7); was introduced during Phase 3.8 in response to the PRED-011 finding. Future applications should explicitly pre-register L8 as a detection target.
- **Single-model audit at any capability tier is insufficient**: the multi-model audit in Phase 3.8 demonstrated that capability-scaling simultaneously reveals missed true positives and reveals false positives produced at lower tiers. Future replications should use at least two independent capable models plus a factual verification baseline.

---

*Leakage Measurement Plan Public Specification v1.0 · 2026-04-23 · Prometheus Lab · TorusGroup*
