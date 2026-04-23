# Retrodiction Protocol — Public Specification (Sanitized)

> **Note:** This is a high-level specification describing the retrodiction protocol at the level required for a reviewer or third-party auditor to understand the experimental design and verify the reported results. The internal implementation details of the Torus OS / Prometheus Lab cognitive pipeline — including prompt engineering strategies, agent architectures, and scoring heuristics — are proprietary technology of TorusGroup and are not released.
>
> For methodological discussion see the companion manuscript (`paper/manuscript.md`) §2. For reproducibility verification, the released artifacts (sealed predictions, corpora, audit scripts, scoring rationale) are sufficient; replicating the generation step requires either (a) re-implementing the protocol described below with a comparable LLM pipeline, or (b) contacting TorusGroup for a licensed engagement.

---

## 1. Overview

The retrodiction protocol is a cryptographically-blinded AI hypothesis-generation and validation procedure. Given a scientific domain with a well-defined "cutoff date" and a corpus of post-cutoff literature, it produces a set of sealed predictions about the domain's future, then scores those predictions against the actual post-cutoff literature.

The protocol has eight phases:

| Phase | Name | Output |
|-------|------|--------|
| R-0 | Domain selection | Chosen field + cutoff date |
| R-1 | Literature base (baseline corpus ≤ cutoff) | Hash-sealed JSONL + BibTeX |
| R-2 | Knowledge map | Structured representation of baseline state (internal artifact) |
| R-3 | Hypothesis generation (retrieval-only) | Draft predictions YAML |
| R-4 | Adversarial pre-audit (Anomalist Pass) | Survived / wounded / destroyed verdicts |
| R-5 | Hash-sealing | SHA-256 seal, git commit, seal chain |
| R-6 | Validation corpus (post-cutoff literature) | Hash-sealed JSONL |
| R-7 | Scoring + leakage audit | CONFIRMED / PARTIAL / CONTRADICTED / INCONCLUSIVE + multi-layer leakage audit |

---

## 2. Inputs and outputs (contract)

**Inputs:**
- Domain name (e.g., "glymphatic system")
- Cutoff date (ISO-8601)
- Prediction count target (e.g., 16 ± 2)
- Confidence interval for predictions (typical 0.40–0.80)

**Outputs:**
- `predictions-final.yaml` — sealed, hashed, committed
- `corpus/baseline/corpus.jsonl` — hashed, released
- `corpus/validation/corpus.jsonl` — hashed, released
- `audit/leakage-audit-report.md` — multi-layer audit
- `audit/validation-scoreboard.md` — per-prediction adjudication
- Per-prediction scoring rationale

---

## 3. Phase specifications (high-level)

### R-1. Literature base

Automated construction of a baseline corpus ≤ cutoff date from PubMed, Crossref, arXiv, bioRxiv, and Europe PMC. Aggressive filters remove out-of-scope work. Output is a JSONL where each line is a normalized paper record (DOI, title, abstract, authors, year, venue). The corpus is SHA-256 hashed before any downstream use.

### R-2. Knowledge map

An internal structured representation of the baseline state, organized along a "known knowns / known unknowns / unknown unknowns" taxonomy. The structure of this representation and the prompts used to derive it are proprietary to TorusGroup. The outputs of this phase are intermediate artifacts — not released in the public repository.

### R-3. Hypothesis generation

A retrieval-only language model pipeline (based on Claude Opus 4.7) generates candidate predictions constrained to the baseline corpus. The system prompt enforces three properties: (a) no post-cutoff references, (b) each prediction anchored to DOIs in the baseline corpus, (c) each prediction accompanied by a confidence score and a falsifiability criterion. The exact system prompt and generation strategy are proprietary.

Output format is specified in `predictions-schema.yaml`.

### R-4. Adversarial pre-audit (Anomalist Pass)

A second LLM session, given the draft predictions, attempts to falsify or weaken each one. Outcomes are:
- **SURVIVED** — prediction passed adversarial audit unchanged
- **WOUNDED-REFORMULATED** — audit identified weaknesses that were addressed by reformulation (threshold relaxation, scope narrowing, language correction); the reformulated prediction entered the sealed pool
- **DESTROYED** — audit identified structural issues that rendered the prediction non-falsifiable or biologically implausible; prediction removed pre-seal

The adversarial audit methodology, scoring heuristics, and agent architecture are proprietary. Only the outcome distribution is released.

### R-5. Hash-sealing

The surviving predictions are serialized (YAML with `sort_keys=True`, LF line endings, UTF-8, trailing newline) and SHA-256 hashed. The file and hash are committed to a public git repository before any post-cutoff literature is consulted. Planned trust anchors: git commit, arXiv preprint, OpenTimestamps Bitcoin anchoring.

### R-6. Validation corpus

Post-cutoff literature is harvested via the same aggregation strategy as R-1. The validation corpus is independently hashed and is used only after R-5 completes.

### R-7. Scoring + leakage audit

**Scoring:** for each sealed prediction, a hybrid BM25 + semantic embedding retrieval returns candidate validation papers; these are adjudicated into CONFIRMED / PARTIALLY CONFIRMED / CONTRADICTED / INCONCLUSIVE.

**Leakage audit (three layers):**
- Layer 1: DOI date verification (factual, objective)
- Layer 2: multi-model independent-judge audit across capability tiers (primary: `gemini-3.1-pro-preview`; cross-validator: `gemini-2.5-pro`; legacy baseline: `gemini-2.5-flash`)
- Layer 3: same-model self-consistency pass

See `audit/leakage-audit-report.md` for full detail.

---

## 4. Pre-registered success thresholds

| Metric | Minimum PASS | STRONG |
|--------|-------------|--------|
| Precision (strict, CONFIRMED only) | 0.40 | 0.60 |
| Precision (liberal, CONFIRMED ∪ PARTIAL) | 0.40 | 0.60 |
| Novelty | 0.30 | 0.50 |
| Insight value (≥1 year anticipation) | 0.10 | 0.25 |
| Leakage (factual DOI) | ≤ 0.05 | — |

A result below Minimum PASS is to be published as a methodology failure rather than concealed.

---

## 5. Dependencies

- Python 3.10+
- `google-generativeai`, `requests`, `python-dotenv`
- Crossref API, PubMed E-utilities (no authentication required for moderate usage)
- Gemini API key (for Layer 2 audit reproduction)
- Git (for hash-sealing and commit history)

---

## 6. Licensing

The public artifacts in this repository (sealed predictions, corpora, audit results, scoring rationale) are released under CC-BY 4.0 (data) + MIT (code). The underlying Torus OS cognitive pipeline — including agent architectures, prompts, scoring heuristics, and knowledge-mapping formats — is proprietary technology of TorusGroup and is not included in this release.

Commercial licensing of the full Torus OS pipeline for scientific retrodiction or applied pre-mortem forecasting: contact `acc.torusgroup@gmail.com` with subject line `retrodiction licensing`.

---

*Retrodiction Protocol Public Specification v1.0 · 2026-04-23 · Prometheus Lab · TorusGroup*
