# Phase 3.5 — Citation Hygiene Fix Report

**Expedition:** exp-retrodiction
**Phase:** 3.5 — Citation Hygiene Fix (post-seal correction)
**Date:** 2026-04-23
**Operator:** Dara (data-engineer)
**Scope:** Reference hygiene only — zero leakage impact
**File corrected:** `phase-3-hypothesis-generation/predictions-final.yaml`

---

## Executive Summary

The DOI Audit performed during Phase 4a (see `doi_audit_annotations.md`) detected **5 citation errors** in `predictions-final.yaml`:

- 2 DOI typos/mismatches (did not resolve in Crossref or resolved to unrelated papers)
- 3 PMID miscitations (PubMed titles did not match the YAML excerpts)

All 5 errors were **reference hygiene issues**, not temporal leakage — all intended source papers were confirmed as pre-2018 (consistent with the Phase 3 temporal cutoff of 2017-12-31).

This report documents the corrections, verifies each new reference via Crossref API, and records the new SHA-256 seal.

---

## Corrections Applied

### Correction 1 — JNEUROSCI prefix typo

| Field | Before | After |
|---|---|---|
| DOI | `10.1525/JNEUROSCI.3020-14.2014` | `10.1523/JNEUROSCI.3020-14.2014` |
| Year | 2014 | 2014 (unchanged) |
| Used in | PRED-GLY-001 | PRED-GLY-001 |

**Reason:** Society for Neuroscience (JNEUROSCI) uses DOI prefix `10.1523`, not `10.1525`. Typo error.

**Crossref verification:**
- Title: *Impairment of Glymphatic Pathway Function Promotes Tau Pathology after Traumatic Brain Injury*
- First author: Iliff
- Year: 2014

---

### Correction 2 — Ringstad 2017 (unresolvable DOI)

| Field | Before | After |
|---|---|---|
| DOI | `10.3171/2017.4.JNS161549` | `10.1093/brain/awx191` |
| Year | 2017 | 2017 (unchanged) |
| Used in | PRED-GLY-003, PRED-GLY-004, PRED-GLY-013, PRED-GLY-016 (4 occurrences) | same |

**Reason:** Original DOI did not resolve in Crossref. The excerpt ("Intrathecal gadobutrol MRI visualizes human glymphatic inflow over hours") content-matches Ringstad et al. 2017 in Brain.

**Crossref verification:**
- Title: *Glymphatic MRI in idiopathic normal pressure hydrocephalus*
- First author: Ringstad
- Year: 2017

---

### Correction 3 — Iliff 2013 arterial pulsations (PMID miscopied)

| Field | Before | After |
|---|---|---|
| Reference | `pmid: "23943882"` | `doi: "10.1523/JNEUROSCI.1592-13.2013"` |
| Year | 2013 | 2013 (unchanged) |
| Used in | PRED-GLY-009 | PRED-GLY-009 |

**Reason:** PMID 23943882 actually refers to an apelin receptor paper, unrelated to the cited excerpt "Arterial pulsations are primary driver of perivascular CSF flow". The intended paper is Iliff et al. 2013, J. Neurosci. Replaced PMID with verified DOI.

**Crossref verification:**
- Title: *Cerebral Arterial Pulsation Drives Paravascular CSF–Interstitial Fluid Exchange in the Murine Brain*
- First author: Iliff
- Year: 2013

---

### Correction 4 — Dreha-Kulaczewski 2015 respiratory CSF (PMID miscopied, year correction)

| Field | Before | After |
|---|---|---|
| Reference | `pmid: "26318022"` | `doi: "10.1523/JNEUROSCI.3246-14.2015"` |
| Year | 2016 | **2015** (corrected) |
| Used in | PRED-GLY-009, PRED-GLY-012, PRED-GLY-016 (3 occurrences) | same |

**Reason:** PMID 26318022 actually refers to an Alzheimer network paper (GAAIN), unrelated to the cited excerpt about respiratory CSF flow. The intended paper is Dreha-Kulaczewski et al. 2015 ("Inspiration is the major regulator of human CSF flow"), J. Neurosci. Replaced PMID with verified DOI; year corrected 2016 → 2015.

**PubMed verification (ESearch/ESummary):**
- PMID: 25673843
- Title: *Inspiration is the major regulator of human CSF flow*
- First author: Dreha-Kulaczewski
- Pubdate: 2015-02-11
- DOI: `10.1523/JNEUROSCI.3246-14.2015`

---

### Correction 5 — Riba-Llena 2016 EPVS + hypertension (PMID miscopied)

| Field | Before | After |
|---|---|---|
| Reference | `pmid: "27005777"` | `doi: "10.1111/ene.12979"` |
| Year | 2016 | 2016 (unchanged) |
| Used in | PRED-GLY-015 | PRED-GLY-015 |

**Reason:** PMID 27005777 actually refers to a chromium methylation cancer paper, unrelated to the cited excerpt "Hypertension and aging associated with enlarged Virchow-Robin spaces". The intended paper, identified via PubMed search, is Riba-Llena et al. 2016 — a direct match on content (EPVS + target organ damage + MCI in hypertensive patients).

**Crossref verification:**
- Title: *Assessment of enlarged perivascular spaces and their relation to target organ damage and mild cognitive impairment in patients with hypertension*
- First author: Riba-Llena
- Year: 2016
- Journal: European Journal of Neurology

---

## Leakage Impact Analysis

**Temporal cutoff:** 2017-12-31

All 5 replacement references are pre-2018:

| # | Replacement | Year | Status |
|---|---|---|---|
| 1 | `10.1523/JNEUROSCI.3020-14.2014` | 2014 | CLEAN |
| 2 | `10.1093/brain/awx191` | 2017 | CLEAN |
| 3 | `10.1523/JNEUROSCI.1592-13.2013` | 2013 | CLEAN |
| 4 | `10.1523/JNEUROSCI.3246-14.2015` | 2015 | CLEAN |
| 5 | `10.1111/ene.12979` | 2016 | CLEAN |

**Leakage introduced:** 0 (zero). All papers existed and were known pre-cutoff.

---

## Substance Preservation

The following fields were **NOT touched** in any prediction:

- `claim` — all 16 claims verbatim
- `confidence` — all 16 confidence scores unchanged
- `predicted_window` — unchanged
- `falsification` — all falsification criteria unchanged
- `vectors` — cognitive vectors unchanged
- `category` — unchanged
- `novelty` — unchanged
- `anomalist_verdict` — unchanged
- `anomalist_score` — unchanged
- `reformulation_notes` — unchanged

Changes were **strictly limited to** the `anchors` list (DOI/PMID fields) and one year correction (2016→2015) tied to the Dreha-Kulaczewski paper.

**Prediction count:** 16 before, 16 after. No additions, no removals.

---

## Re-Sealing

### SHA-256 seals

| Version | Hash | Date |
|---|---|---|
| v1 (original) | `1765b221d1cc12d7c010cb4fe1f18bc987e6aa910d20e47ce609d92fd7afb586` | 2026-04-23T03:57:02Z |
| **v2 (post-fix)** | **`b9add8ef681fa02ecce726ba0d1b371013acf060130821377346d9de1ae9cc73`** | 2026-04-23T04:30:00Z |

### Verification command

```bash
node -e "const fs=require('fs'),crypto=require('crypto');console.log(crypto.createHash('sha256').update(fs.readFileSync('predictions-final.yaml')).digest('hex'))"
```

Expected output (v2): `b9add8ef681fa02ecce726ba0d1b371013acf060130821377346d9de1ae9cc73`

### Git commit

Commit hash: *[registered post-commit — see seal-manifest.yaml chain_of_custody]*

### YAML validity

Confirmed via `python -c "import yaml; yaml.safe_load(open('predictions-final.yaml'))"` — loads cleanly; 16 predictions parsed.

---

## Status

**PASS** — Reference hygiene restored. Zero leakage impact. All 16 predictions preserved verbatim (claims, confidence, falsification, vectors, verdicts). Ready for Phase 4 validation with clean citation trail.

---

## Artifacts

- `phase-3-hypothesis-generation/predictions-final.yaml` (v2, SHA-256 `b9add8ef...ae9cc73`)
- `phase-3-hypothesis-generation/seal-manifest.yaml` (updated with v1 + v2 hashes, corrections log, Phase 3.5 in chain_of_custody)
- `phase-4-validation/citation-hygiene-fix-report.md` (this document)
- `phase-4-validation/doi_audit_annotations.md` (original findings, unchanged)

---

*Phase 3.5 Citation Hygiene Fix — complete 2026-04-23 by Dara (data-engineer).*
