# Supplementary Material — Retrodiction as Validation

**Paper:** Retrodiction as validation: A hash-sealed AI forecasting protocol tested on glymphatic neuroscience 2017-2026
**Date:** 2026-04-23
**Seal:** `predictions-final.yaml` SHA-256 v4 `a144c1801ef24f4c8b73418a0836b61f9e25411e74329fa492915e5189e54460`

---

## §S1. Cryptographic seal chain (full)

The predictions file underwent four sealing events during the audit lifecycle. Each event produced a distinct SHA-256 hash of `predictions-final.yaml`; the chain is reproducible by independent hashing of each version preserved in git history.

| Version | Event | SHA-256 | Phase |
|---------|-------|---------|-------|
| v1 | Original hash-sealing after Anomalist Pass | `1765b221d1cc12d7c010cb4fe1f18bc987e6aa910d20e47ce609d92fd7afb586` | 3.6 (seal) |
| v2 | Citation hygiene fix (5 typo DOIs corrected) | `b9add8ef681fa02ecce726ba0d1b371013acf060130821377346d9de1ae9cc73` | 3.5 (mid-pipeline correction) |
| v3 | Provisional Flash-flag invalidation of PRED-GLY-009 | `2db0fab5108af2727faa6a39b8da37ba2272664b00a618c2742942191d44928f` | 3.7 (later reversed) |
| **v4** | **Multi-model re-audit: PRED-GLY-011 invalidated, PRED-GLY-009 revalidated** | **`a144c1801ef24f4c8b73418a0836b61f9e25411e74329fa492915e5189e54460`** | **3.8 (current canonical)** |

Each seal is tied to a corresponding git commit. Third-party auditors can verify the chain by cloning the repository and running SHA-256 on each historical version of the YAML.

---

## §S2. DOI verification audit (Layer 1) — full output

Every anchor DOI from the 16 sealed predictions was resolved and date-verified. Full results are in `phase-4-validation/doi_audit_results.json`. Summary:

- **Total DOIs verified:** 48 (across 16 predictions, post-Phase 3.5 citation hygiene fix)
- **Resolution success rate:** 100% (48/48)
- **Publication dates ≤ 2017-12-31:** 48/48 (100%)
- **Publication dates > 2017-12-31:** 0/48 (0.00% factual anchor leakage)
- **Resolution method:** Crossref API primary + PubMed E-utilities fallback + post-hoc typo corrections (`doi_audit_annotations.md`)

The Phase 3.5 citation hygiene fix detected 5 typographical errors in anchor DOIs/PMIDs (prefix `10.1525` vs `10.1523`, PMID/title mismatches); all were corrected pre-Phase 4c validation. See `citation-hygiene-fix-report.md` for the diff.

---

## §S3. Inter-model leakage audit comparison (Layer 2 detail)

### S3.1 Model configuration

All three Gemini models were queried with identical prompt (see `run_gemini_audit_api.py`) and identical generation configuration:

```python
generation_config = {
    "temperature": 0.1,
    "max_output_tokens": 8192,  # required for Pro models (thinking tokens)
}
```

Temperature 0.1 was chosen for reproducibility; self-consistency sampling at higher temperature is left for future work.

### S3.2 Per-prediction verdict matrix (all 16 predictions × 3 models)

| PRED-ID | gemini-2.5-flash | gemini-2.5-pro | gemini-3.1-pro-preview (PRIMARY) | Adjudicated verdict |
|---------|------------------|----------------|-----------------------------------|---------------------|
| 001 | CLEAN | CLEAN | CLEAN | CLEAN |
| 002 | CLEAN | CLEAN | CLEAN | CLEAN |
| 003 | **LEAKED** | CLEAN | CLEAN | CLEAN (Flash FP — ALPS date) |
| 004 | **LEAKED** | CLEAN | CLEAN | CLEAN (Flash FP — ALPS date) |
| 005 | CLEAN | CLEAN | CLEAN | CLEAN |
| 006 | CLEAN | CLEAN | CLEAN | CLEAN |
| 007 | CLEAN | **LEAKED** | CLEAN | CLEAN (Pro 2.5 FP — Mestre 2018 over-read) |
| 008 | CLEAN | CLEAN | CLEAN | CLEAN |
| 009 | **LEAKED** | CLEAN | CLEAN | CLEAN — **REVALIDATED** (Flash over-reach on terminology) |
| 010 | DESTROYED pre-seal (not audited) | — | — | — |
| **011** | CLEAN | **LEAKED** | **LEAKED** | **LEAKED — INVALIDATED (methodological)** |
| 012 | CLEAN | **LEAKED** | CLEAN | CLEAN (Pro 2.5 FP — mis-dated Taoka) |
| 013 | CLEAN | CLEAN | CLEAN | CLEAN |
| 014 | CLEAN | **LEAKED** | CLEAN | CLEAN (Pro 2.5 FP — ALPS/Yokota confusion) |
| 015 | CLEAN | CLEAN | CLEAN | CLEAN |
| 016 | **LEAKED** | CLEAN | CLEAN | CLEAN (Flash FP — ALPS date) |
| 017 | CLEAN | CLEAN | CLEAN | CLEAN |
| 018 | DESTROYED pre-seal (not audited) | — | — | — |

### S3.3 Per-model summary

| Metric | gemini-2.5-flash | gemini-2.5-pro | gemini-3.1-pro-preview |
|--------|------------------|----------------|-----------------------|
| Total LEAKED flags | 4 | 4 | 1 |
| TRUE POSITIVES (convergent with primary) | 0 | 1 (PRED-011) | 1 (PRED-011) |
| FALSE POSITIVES | 3 (ALPS x3) | 3 (strain, Taoka-date, Yokota) | 0 |
| Over-reach flags (rejected by higher models) | 1 (PRED-009) | 0 | 0 |
| Sensitivity (TP / pool TP) | 0% | 100% | **100%** |
| Specificity (TN / pool TN) | 75% (12/16) | 75% (12/16) | **100%** (15/15 non-011) |

### S3.4 Inter-model agreement on flags

- Flash ∩ Pro 2.5 ∩ Pro 3.1: **0 predictions** (no single prediction flagged by all three)
- Pro 2.5 ∩ Pro 3.1: **1 prediction** (PRED-011) — the sole true positive
- Flash ∩ Pro 2.5: 0 predictions
- Flash ∩ Pro 3.1: 0 predictions
- Pro 3.1 unique flags: 0 (all Pro 3.1 flags also in Pro 2.5)

**Interpretation:** Cross-model convergence is near-zero except on the true positive. This is the central empirical finding supporting the methodological claim that **single-model independent audit is insufficient** — each model produces a different, mostly-false-positive flag set. Convergence across capable independent models is the only signal reliably correlated with true leakage.

### S3.5 Primary judge rationale (Pro 3.1 verbatim, all 16)

Full JSON output in `phase-4-validation/gemini_audit_results_pro31.json`. Key verdicts:

- **PRED-GLY-011 (LEAKED):** *"The specific correlation between delta-EEG oscillations and CSF inflow measured by synchronized fMRI in humans perfectly describes the methodology and findings of the landmark 2019 paper by Fultz et al."*
- **PRED-GLY-009 (CLEAN):** *"The prediction relies on pre-2018 concepts (the debate between Iliff bulk flow and Smith diffusion, and early models of oscillatory dispersion) to make a plausible forward-looking claim about whole-brain modeling and perivascular velocities without using post-2017 terminology."*
- **PRED-GLY-003 (CLEAN):** *"The ALPS index was introduced in 2017, making its proposed application to Parkinson's disease and correlation with UPDRS a temporally consistent extrapolation using strictly pre-2018 terminology and concepts."*
- **PRED-GLY-017 (CLEAN):** *"The prediction logically combines the 2015 discovery of meningeal lymphatics and their role in clearance with the long-established function of VEGF-C in lymphangiogenesis, using entirely pre-2018 concepts to hypothesize a therapeutic intervention for Alzheimer's disease."*

---

## §S4. Validation corpus construction

**Corpus:** `corpus-glymphatic-2018-2026.jsonl`
**Size:** 3,329 peer-reviewed papers and preprints
**Date range:** 2018-01-01 to 2026-04-23
**Hash (SHA-256):** `3aa15c2c2fd8af4291374671bf6d64a63cd0ca246ab0414967a6a3c8199be5df`

Assembly process:
1. PubMed E-utilities query: `(glymphatic OR AQP4 OR meningeal_lymphatic OR perivascular_space) AND (2018[PDAT]:2026[PDAT])`
2. Crossref API supplementary search for DOI-only entries
3. Preprint servers (bioRxiv, medRxiv, arXiv q-bio) for 2024-2026 coverage
4. De-duplication by DOI; 3,329 unique records

Full corpus file is released with the paper; any third-party auditor can re-run the validation scoring by hybrid BM25+embedding retrieval over this corpus.

---

## §S5. Per-prediction scoring detail

Individual scoring documents for each of the 15 valid-pool predictions are in `phase-4-validation/per-prediction-scores/PRED-GLY-###-score.md`. Each document contains:

- Exact claim (verbatim from YAML)
- Top 3-5 validation papers retrieved (with DOI + excerpt)
- Scoring rationale (why CONFIRMED, PARTIAL, or INCONCLUSIVE)
- Borderline flags for any case where reviewer disagreement is plausible

Independent re-scoring is welcomed.

---

*Supplementary Material v1.0 — 2026-04-23 · Prometheus Lab · exp-retrodiction*
