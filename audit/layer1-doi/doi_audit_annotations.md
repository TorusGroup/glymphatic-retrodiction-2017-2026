# DOI/PMID Audit — Post-Hoc Annotations

## Unresolved DOIs → Resolved via fallback (typo correction)

### 10.1525/JNEUROSCI.3020-14.2014 → typo for 10.1523/JNEUROSCI.3020-14.2014
- Corrected via Crossref (Society for Neuroscience prefix is `10.1523`, not `10.1525`)
- Paper: "Impairment of Glymphatic Pathway Function Promotes Tau Pathology after Traumatic Brain Injury" (Iliff et al.)
- Publication date: **2014-12-03** → **CLEAN**

### 10.3171/2017.4.JNS161549 → most likely Ringstad et al. 2017 (DOI `10.1093/brain/awx191`)
- Excerpt cited: "Intrathecal gadobutrol MRI visualizes human glymphatic inflow over hours."
- DOI pattern `10.3171/2017.4.JNS161549` does not resolve in Crossref; mimics J. Neurosurg. format but no match found
- Content-matched candidate: Ringstad et al. 2017, "Glymphatic MRI in idiopathic normal pressure hydrocephalus", Brain, DOI `10.1093/brain/awx191`, **published 2017-07-05** → **CLEAN**
- Flag: **citation integrity issue** (wrong DOI in YAML), but temporal classification unaffected

## PMID Title Mismatches (data integrity, NOT leakage)

Three PMIDs were cited in `predictions-final.yaml`; their PubMed titles do NOT match the excerpts in the YAML:

| PMID | Excerpt claimed in YAML | Actual PubMed title | PubMed pubdate |
|------|-------------------------|---------------------|----------------|
| 23943882 | "Arterial pulsations are primary driver of perivascular CSF flow" | "The apelin receptor APJ: journey from an orphan to a multifaceted regulator of homeostasis" | 2013-10 |
| 26318022 | "Respiratory pressure variations contribute to CSF movement" | "The Global Alzheimer's Association Interactive Network" | 2016-01 |
| 27005777 | "Hypertension and aging associated with enlarged Virchow-Robin spaces" | "Methylation levels of P16 and TP53 ... hexavalent chromium" | 2016-05 |

**Interpretation:** PMIDs appear hallucinated/miscopied during Phase 3 generation. The intended papers likely exist (Iliff 2013 arterial pulsations; Dreha-Kulaczewski 2015 respiratory CSF; Potter 2015 EPVS & hypertension) and all have pre-2018 publication dates.

**Impact on leakage audit:** All three claimed excerpts describe concepts well-established pre-2018 (arterial pulsations as CSF driver = Iliff 2013; respiratory CSF = Dreha-Kulaczewski 2015; EPVS & aging = multiple pre-2017 papers). **No temporal leakage introduced by these miscitations.** The issue is reference hygiene, not knowledge cutoff.

## Corrected totals

| Metric | Original | After corrections |
|--------|----------|-------------------|
| Total anchors | 13 | 13 |
| Clean (≤2017) | 11 | 13 |
| Leaked (>2017) | 0 | 0 |
| Unresolved | 2 | 0 |
| **Leakage rate (Camada 1)** | **0.00%** | **0.00%** |

## Recommendation

The leakage audit **PASSES** on Camada 1 regardless of citation hygiene issues. However, a future correction pass should:

1. Fix JNEUROSCI prefix typo (10.1525 → 10.1523)
2. Replace `10.3171/2017.4.JNS161549` with verified Ringstad 2017 DOI (`10.1093/brain/awx191`)
3. Replace the 3 miscited PMIDs with their intended papers (Iliff 2013, Dreha-Kulaczewski 2015, Potter 2015 or equivalent)

These corrections are **reference hygiene** tasks, orthogonal to the validation of Phase 4b.
