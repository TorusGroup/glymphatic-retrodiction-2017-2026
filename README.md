# Glymphatic Retrodiction 2017-2026

**Hash-sealed AI retrodiction of glymphatic neuroscience, from 2017-12-31 cutoff through 2026-04-23 validation.**

This repository is the reproducibility companion to the paper:

> *Retrodiction as validation: A hash-sealed AI forecasting protocol tested on glymphatic neuroscience 2017-2026*

Submitted concurrently to **Royal Society Interface** (journal) and **arXiv** (preprint).

---

## The protocol in one sentence

An AI pipeline (Claude Opus 4.7, retrieval-only over literature ≤ 2017-12-31) generated 18 candidate predictions about glymphatic biology; an adversarial pre-audit (Anomalist Pass) killed 2 and reformulated 10; the resulting 16 predictions were hash-sealed (SHA-256, git-committed) before any post-2017 literature was consulted; a multi-model independent-judge leakage audit invalidated 1; the remaining 15 were scored against a 3,329-paper validation corpus published 2018-2026.

**Key result:** 8 CONFIRMED + 5 PARTIAL + 0 CONTRADICTED + 2 INCONCLUSIVE (N=15).
- Strict precision: **53.33%** (above 40% pre-registered threshold)
- Liberal precision: **86.67%** (STRONG band)
- Novelty: 53.33% · Insight value: 6.67% (1 prediction, Da Mesquita 2018 *Nature*, +1 year)
- Factual DOI leakage: **0.00%** · Convergent leakage: 6.25% (1/16, methodological leakage in PRED-GLY-011 = Fultz 2019 *Science* setup match)

---

## Seal chain (cryptographic integrity)

| Version | Event | SHA-256 |
|---------|-------|---------|
| v1 | Original hash-sealing after Anomalist Pass | `1765b221d1cc12d7c010cb4fe1f18bc987e6aa910d20e47ce609d92fd7afb586` |
| v2 | Citation hygiene fix (5 typo DOIs corrected) | `b9add8ef681fa02ecce726ba0d1b371013acf060130821377346d9de1ae9cc73` |
| v3 | Provisional Flash-flag invalidation of PRED-GLY-009 (*later reversed*) | `2db0fab5108af2727faa6a39b8da37ba2272664b00a618c2742942191d44928f` |
| **v4** | **Multi-model re-audit: PRED-GLY-011 invalidated, PRED-GLY-009 revalidated** (current canonical) | **`a144c1801ef24f4c8b73418a0836b61f9e25411e74329fa492915e5189e54460`** |

Verify: `sha256sum predictions/predictions-final.yaml` should output `a144c180…9e54460`.

---

## Repository layout

```
glymphatic-retrodiction-2017-2026/
├── paper/
│   ├── paper.html                        # Bilingual EN+PT single-file HTML
│   ├── manuscript.md                     # Journal version (Royal Society Interface)
│   ├── manuscript-arxiv-preprint.md      # arXiv preprint version + metadata
│   ├── supplementary-material.md         # §S1 seal chain · §S2 DOI audit · §S3 inter-model matrix
│   └── references.bib                    # Cite-keys for all anchors + validation papers
│
├── protocol/                             # Public specification of the methodology
│   ├── retrodiction-protocol-spec.md     # Public sanitized spec (internal details proprietary)
│   ├── predictions-schema.yaml           # YAML schema for sealed predictions
│   ├── leakage-measurement-plan.md       # Public leakage taxonomy + multi-layer strategy
│   └── literature-base-spec.md           # Corpus construction spec
│
├── predictions/                          # Hash-sealed predictions
│   ├── predictions-final.yaml            # v4 seal — CURRENT CANONICAL
│   └── anomalist-summary.md              # Public summary of adversarial pre-audit outcomes
│
├── corpus/
│   ├── baseline-2017/                    # Literature ≤ 2017-12-31 (N=563)
│   │   ├── corpus.jsonl                  # Primary dataset
│   │   ├── corpus.bib                    # BibTeX export
│   │   ├── manifest.yaml                 # Build metadata + SHA-256
│   │   └── exclusion-log.md              # Filtering decisions
│   │
│   └── validation-2018-2026/             # Literature 2018-01-01 → 2026-04-23 (N=3,329)
│       ├── corpus.jsonl
│       ├── corpus.bib
│       ├── manifest.yaml
│       └── exclusion-log.md
│
├── audit/
│   ├── layer1-doi/                       # Factual DOI-date verification
│   │   ├── audit_dois.py                 # Script (Crossref + PubMed)
│   │   ├── doi_audit_results.json        # 48/48 anchors ≤ 2017
│   │   ├── doi_audit_annotations.md      # Typo corrections (Phase 3.5)
│   │   └── citation-hygiene-fix-report.md
│   │
│   ├── layer2-multimodel/                # Multi-model LLM audit (Phase 3.8)
│   │   ├── run_gemini_audit_api.py                      # Parametric audit script
│   │   ├── results-gemini-3.1-pro-preview.json          # PRIMARY JUDGE — definitive
│   │   ├── results-gemini-2.5-pro.json                  # Cross-validator
│   │   └── results-gemini-2.5-flash.json                # Legacy baseline
│   │
│   ├── leakage-audit-report.md           # v3 audit report (Pro 3.1 primary)
│   └── validation-scoreboard.md          # v3 scoreboard (N=15, post-swap)
│
└── per-prediction-scores/                # Individual scoring rationale per prediction
    ├── PRED-GLY-001-score.md
    ├── PRED-GLY-002-score.md
    └── ...
```

---

## How to reproduce

### Seal verification (30 seconds)

```bash
sha256sum predictions/predictions-final.yaml
# Expected: a144c1801ef24f4c8b73418a0836b61f9e25411e74329fa492915e5189e54460

sha256sum corpus/baseline-2017/corpus.jsonl
# Expected: d4f52383c20a98bab610d40716c0e5767c60c34153c2e6e6c642c48b64e4849b

sha256sum corpus/validation-2018-2026/corpus.jsonl
# Expected: 3aa15c2c2fd8af4291374671bf6d64a63cd0ca246ab0414967a6a3c8199be5df
```

### Re-run Layer 1 audit (DOI date verification)

```bash
cd audit/layer1-doi/
pip install requests
python audit_dois.py
# Output: doi_audit_results.json (48/48 anchors ≤ 2017)
```

### Re-run Layer 2 audit (multi-model Gemini)

Requires a Google AI Studio API key with Gemini access.

```bash
cd audit/layer2-multimodel/
pip install google-generativeai python-dotenv
echo "GEMINI_API_KEY=your_key_here" > .env

# Primary judge (current canonical)
python run_gemini_audit_api.py  # MODEL_NAME="gemini-3.1-pro-preview" by default

# Compare capability tiers (edit MODEL_NAME in the script)
# gemini-2.5-pro → cross-validator
# gemini-2.5-flash → legacy baseline
```

### Re-score predictions against validation corpus

Individual per-prediction scoring rationale is in `per-prediction-scores/`. Each file cites the 3-5 validation papers retrieved from the corpus and explains the verdict (CONFIRMED / PARTIAL / INCONCLUSIVE).

Full corpus is in `corpus/validation-2018-2026/corpus.jsonl` (one JSON record per paper: title, abstract, authors, DOI, year, venue).

---

## Key findings

### 3 biggest hits

1. **PRED-GLY-017** — Meningeal lymphatic / VEGF-C / Aβ clearance. Moonshot (confidence 0.45). Confirmed by **Da Mesquita 2018 Nature**, +1 year anticipation. The only prediction meeting the insight-value criterion.
2. **PRED-GLY-001** — α-synuclein glymphatic clearance via AQP4. Confirmed by Zou 2019 → Ding 2024 → Scarpelli 2025 serial convergence.
3. **PRED-GLY-009** — Whole-brain modeling resolves Iliff-Smith via oscillatory dispersion. Confirmed by Helakari 2022. *(Note: this prediction was provisionally invalidated in Phase 3.7 based on a single-model Flash flag; the flag was reversed in Phase 3.8 when higher-capability models both classified the prediction as CLEAN.)*

### 3 biggest errors

1. **PRED-GLY-011** (invalidated) — Methodological leakage. The predicted setup (synchronized fMRI + delta-EEG + CSF inflow in NREM humans) too precisely matched the Fultz 2019 *Science* experimental design. Detected by Pro 3.1 + Pro 2.5 convergent flag.
2. **PRED-GLY-007** — Right question, wrong mechanism. Predicted mouse strain explains Iliff-Smith discrepancy; Mestre 2018 showed anesthesia/age/tracer were the actual confounders.
3. **PRED-GLY-005, -008** — INCONCLUSIVE. Required tools not developed in the validation window.

### Methodological finding

A single-model independent-model audit at **any** capability tier is insufficient. Capability-scaling the independent judge (from `gemini-2.5-flash` to `gemini-3.1-pro-preview`) simultaneously rejected false positives and detected a true positive the lower-capability model had missed. See `audit/leakage-audit-report.md` §Camada 2 and `paper/supplementary-material.md` §S3 for the full inter-model comparison matrix.

---

## Citation

If you build on this protocol, please cite the paper (DOI forthcoming from Royal Society Interface) and this repository:

```bibtex
@article{glymphatic_retrodiction_2026,
  title = {Retrodiction as validation: A hash-sealed AI forecasting protocol tested on glymphatic neuroscience 2017-2026},
  author = {Fink, Matheus and {Prometheus Lab}},
  year = {2026},
  journal = {Royal Society Interface (under review)},
  note = {Repository: https://github.com/TorusGroup/glymphatic-retrodiction-2017-2026},
  urldate = {2026-04-23}
}
```

---

## Scope of release — what is and isn't public

This repository releases the **reproducibility artifacts** required to verify the paper's results: the sealed predictions (with cryptographic integrity), the baseline and validation corpora, the audit scripts and raw outputs, and the scoring rationale per prediction.

The underlying **Torus OS cognitive pipeline** — including the hypothesis-generation system prompts, the Anomalist Pass adversarial-audit methodology, the Knowledge Map framework (Known Knowns / Known Unknowns structure), and the detection-vector heuristic classes — is **proprietary technology of TorusGroup** and is not included in this release. The `vectors` field in `predictions/predictions-final.yaml` references internal heuristic classes by name; the names are preserved in the seal (and cannot be modified without invalidating the SHA-256 chain) but their implementation is not disclosed.

The documents in `protocol/` are **sanitized public specifications** that describe the methodology at the level required for a reviewer or third-party auditor to understand the experimental design and verify the reported results. They do not expose the internal implementation.

Commercial licensing of the full Torus OS pipeline for scientific retrodiction or applied pre-mortem forecasting in other domains: contact `acc.torusgroup@gmail.com` with subject `retrodiction licensing`.

## License

- **Text, data, and analysis:** CC-BY 4.0
- **Code (Python scripts):** MIT

See `LICENSE` for full terms.

---

## Contact and issues

- Bug reports or reproducibility issues: [GitHub Issues](https://github.com/TorusGroup/glymphatic-retrodiction-2017-2026/issues)
- Methodological questions or collaboration proposals: contact the Prometheus Lab via the TorusGroup organization

---

*Prometheus Lab · exp-retrodiction · 2026-04-23*
*Seal chain v1 → v2 → v3 → v4 (`a144c180…9e54460`)*
