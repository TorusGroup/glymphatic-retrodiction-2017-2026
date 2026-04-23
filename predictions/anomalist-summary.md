# Anomalist Pass — Public Summary (Sanitized)

> **Note:** This document reports the aggregate outcomes of the adversarial pre-audit ("Anomalist Pass") applied to the draft predictions. The internal methodology, scoring heuristics, and specific challenges raised during the audit are proprietary to TorusGroup and are not released. The per-prediction adversarial verdicts and reformulation history are summarized here only at the level needed for the paper's methodology section and for reviewer verification of the sealed pool's provenance.

---

## Aggregate distribution

**Input:** 18 draft predictions (generated pre-seal under retrieval-only constraint).
**Process:** Each draft underwent adversarial review by an independent LLM session attempting to falsify, weaken, or reject the prediction.
**Output:** 16 sealed predictions (after destruction of 2 structurally flawed drafts).

| Verdict | Count | % | Definition |
|---------|-------|---|------------|
| **SURVIVED** | 6 | 33% | Prediction passed adversarial audit unchanged |
| **WOUNDED-REFORMULATED** | 10 | 56% | Audit identified weaknesses; prediction was revised (threshold relaxation, scope narrowing, language correction) and entered the sealed pool |
| **DESTROYED** | 2 | 11% | Audit identified structural issues (non-falsifiability, biological implausibility); prediction removed pre-seal |

**DESTROY rate (11%) is below the pre-registered 20-40% target band** — reported transparently in the manuscript (§3.3). The dominant weakness pattern detected was *optimistic quantitative thresholds* on directionally-correct claims; the bulk of adversarial work was reformulation, not outright destruction.

---

## Destroyed predictions (pre-seal)

| ID | Domain | Failure mode |
|----|--------|--------------|
| PRED-GLY-010 | AQP aquaporin redundancy | Biologically implausible — assumed anatomical/functional redundancy between AQP4 and AQP1/AQP9 that does not hold given the known spatial distribution (AQP1 choroid-plexus-localized, AQP9 sparse) |
| PRED-GLY-018 | Astrocytic gatekeeper | Structurally non-falsifiable — "*some* astrocytic kinase or ion channel will emerge as a gatekeeper" could be trivially satisfied |

Neither destroyed prediction appears in the sealed `predictions-final.yaml`. Their removal pre-seal means they never contributed to scoreboard metrics.

---

## Wounded-Reformulated predictions (included in sealed pool)

10 of 16 sealed predictions underwent reformulation. The dominant reformulation pattern was **relaxation of quantitative thresholds** to preserve falsifiability while reducing false-fail risk (e.g., `≥30% reduction` → `statistically significant reduction in the same direction`). Scope narrowing (e.g., restricting a mouse-model claim to specific strains) was a secondary pattern.

Full per-prediction reformulation history is not released. The reformulated (sealed) form of each prediction is canonical and present in `predictions-final.yaml`; the original draft form is present in `predictions-draft.yaml` for provenance. Comparing the two reveals which predictions were reformulated without exposing the adversarial methodology.

---

## Survived predictions (entered sealed pool unchanged)

6 of 16 sealed predictions passed adversarial audit without modification. These are marked `anomalist_verdict: "SURVIVED"` in `predictions-final.yaml`. In aggregate, SURVIVED predictions had higher mean confidence (0.70) than WOUNDED-REFORMULATED (0.57) — consistent with the Anomalist Pass functioning as a quality filter.

---

## Connection to final validation

The Anomalist Pass is a *pre-seal* quality gate. It does not guarantee that a prediction will be CONFIRMED in validation; it guarantees only that the prediction passed adversarial review for falsifiability and plausibility. In the final Phase 4c validation (against 2018-2026 literature):

- 2 DESTROYED-pre-seal predictions: not validated (absent from pool by design)
- 1 INVALIDATED-post-seal prediction (PRED-GLY-011, methodological leakage via multi-model Layer 2 audit)
- 15 valid-pool predictions: 8 CONFIRMED + 5 PARTIAL + 0 CONTRADICTED + 2 INCONCLUSIVE

**Zero CONTRADICTED predictions in the valid pool is the signature of the Anomalist Pass functioning correctly.** See `audit/validation-scoreboard.md` for the full per-prediction outcome table.

---

*Anomalist Pass Public Summary v1.0 · 2026-04-23 · Prometheus Lab*
