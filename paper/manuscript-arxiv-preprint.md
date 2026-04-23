# Retrodiction as validation: A hash-sealed AI forecasting protocol tested on glymphatic neuroscience 2017-2026

## arXiv submission metadata

- **Primary category:** `cs.AI` (Artificial Intelligence)
- **Secondary categories:**
  - `q-bio.OT` (Quantitative Biology — Other)
  - `cs.DL` (Digital Libraries) — for the cryptographic seal methodology
  - `stat.AP` (Applications) — for the validation statistics
- **MSC / ACM classification:** I.2.8 (Problem Solving, Control Methods, and Search); J.3 (Life and Medical Sciences)
- **License:** CC-BY 4.0
- **Submission type:** Preprint (concurrent with journal submission to Royal Society Interface)

---

## Comment field (arXiv "Comments" box)

> 24 pages, 3 tables, 5 figures. Supplementary materials (sealed predictions YAML, baseline and validation corpora JSONL, audit scripts, multi-model audit JSON outputs) available at https://github.com/TorusGroup/glymphatic-retrodiction-2017-2026 (public release). SHA-256 seal chain: v1 `1765b221…7afb586` (original seal, committed 2026-04-23 before any post-2017 literature consulted) → v2 `b9add8ef…ae9cc73` (citation hygiene) → v3 `2db0fab5…44928f` (provisional Flash-flag invalidation) → **v4 `a144c180…9e54460`** (current canonical, Phase 3.8 multi-model re-audit). Methodological paper; glymphatic neuroscience is the test domain, not the scientific claim. Presented also to the Royal Society Interface (simultaneous submission).

---

## arXiv abstract (reformatted from journal version — ≤1920 chars)

Large language models increasingly generate scientific hypotheses, but validity is confounded by training-data leakage: the model may "predict" what it has already memorized. Existing methodologies (benchmarks, human review, RLHF) cannot distinguish synthesis from paraphrase. We present a composite retrodiction protocol combining literature freezing with cryptographic seal, retrieval-only generation, adversarial pre-audit, multi-model independent-judge leakage audit across capability tiers, and independent validation corpus. We demonstrate it on the glymphatic system (neuroscience): a pipeline based on Claude Opus 4.7 generated 18 candidate predictions about glymphatic biology, constrained to literature ≤ 2017-12-31. An adversarial audit killed 2 and reformulated 10, yielding 16 predictions hash-sealed before any post-2017 literature was consulted. Against 3,329 peer-reviewed papers and preprints published 2018-01-01 through 2026-04-23, a Layer-2 multi-model audit (gemini-3.1-pro-preview primary, gemini-2.5-pro cross-validator, gemini-2.5-flash baseline) invalidated 1 prediction (PRED-GLY-011, methodological leakage detected via convergent flag of the two most capable models — the predicted experimental setup matched Fultz 2019 Science too precisely to be an a priori formulation). The final valid pool N=15 yields strict precision 53.33% (8 CONFIRMED), liberal precision 86.67% (adding 5 PARTIAL), 0% contradicted, novelty 53.33%, and forward insight value 6.67% (1 prediction, PRED-017 Da Mesquita 2018 Nature, +1 year anticipation). Temporal leakage measured at the DOI date level is 0.00% across 48 verified anchors; convergent leakage under the primary judge is 6.25%. The protocol itself is offered as a reproducible falsification test for AI-generated scientific hypotheses in any mature field with a tractable cutoff and accessible post-cutoff literature. We report honestly that single-model independent audit at any capability tier is insufficient: capability-scaling the independent judge both rejected false positives produced by the lowest-capability model (three ALPS-date errors and one over-reach on PRED-GLY-009 that was subsequently revalidated) and detected the genuine methodological leakage that the lowest-capability model had missed. The test was single-domain; anticipation beyond cutoff was small (6.67%) because the glymphatic field exploded in the 18 months immediately following our cutoff. The protocol does not prove AI can do science. It provides the first cryptographically-auditable tool by which such a claim can begin to be tested. All hashes, corpora, sealed predictions, and multi-model audit logs are publicly available.

---

## Note on manuscript equivalence

The arXiv preprint body is identical to the journal submission in `manuscript.md`. Differences:

1. **Format:** arXiv accepts Markdown / LaTeX; journal will require LaTeX + specific style. Conversion via pandoc is straightforward.
2. **Figures:** Journal version may require higher-resolution exports; arXiv accepts PDFs or inline images.
3. **References:** arXiv accepts natbib; journal may require specific style (Royal Society Interface = modified Vancouver). See `references.bib`.
4. **Supplementary materials:** arXiv allows a `supplementary.zip`. We will package:
   - `predictions-final.yaml` + seal manifest
   - `corpus-glymphatic-2017.jsonl.gz`
   - `corpus-glymphatic-2018-2026.jsonl.gz`
   - `leakage-audit-report.md`
   - `validation-scoreboard.md`
   - `audit_dois.py` (Layer 1 script)

---

## Cross-referencing strategy

Both versions will cite each other:
- Journal version cites "arXiv preprint, XXXX.XXXXX" (filled in after arXiv assigns ID)
- arXiv version cites "Manuscript submitted to Royal Society Interface, journal reference pending"

This cross-linkage is standard practice and preserves provenance for both scholarly indexing and open-science accessibility.

---

## Publication timing

1. **T+0 (target: 2026-04-25):** arXiv preprint submitted. Full DOI-stamped hash becomes publicly timestamped independent of git.
2. **T+1 week:** Royal Society Interface submission (after arXiv ID returned).
3. **T+2-4 weeks:** Royal Society Interface initial review. If desk-rejected, re-target PLOS ONE (methodology-friendly).
4. **T+8-16 weeks:** Peer review cycle.
5. **T+16-24 weeks:** Accepted publication (best case) or revision cycle.

The arXiv preprint serves three purposes:
- Establishes priority (important for methodology papers)
- Provides a third independent trust anchor (the predictions-file hash appears in a public, indexed preprint — an external auditor can cross-check)
- Gives the community immediate access while peer review proceeds

---

*This document is a metadata wrapper. See `manuscript.md` for the full paper text.*
