# Literature Base Specification

> **Expedição:** exp-retrodiction
> **Fase:** Phase 1 — Protocol Design (especifica), Phase 2 — Glymphatic Cartography (constrói)
> **Ciclo global:** 10 (spec), 11-12 (construção)
> **Autor:** Prometheus Lab
> **Data:** 2026-04-22

---

## 0. Propósito

Este documento especifica a estrutura, fontes, filtros, e critérios de inclusão/exclusão da **base de literatura congelada em 2017-12-31** que será o único corpus autorizado para as Fases R-1 a R-6 da expedição.

**Princípio central:** se uma predição não pode ser derivada deste corpus, ela não é permitida no protocolo.

---

## 1. Estrutura de Diretórios

```
exp-retrodiction/
├── phase-2-literature-base/
│   └── literature-base-2017/
│       ├── MANIFEST.yaml                  # índice principal + hash
│       ├── bibliography.bib               # BibTeX de todas entradas
│       ├── papers.jsonl                   # metadados estruturados (1 linha por paper)
│       ├── abstracts.jsonl                # abstracts extraídos
│       ├── pdfs/                          # PDFs originais (quando disponíveis)
│       │   ├── iliff-2012-scitranslmed.pdf
│       │   ├── xie-2013-science.pdf
│       │   └── ...
│       ├── extracted-text/                # OCR + parse text completo dos PDFs
│       │   ├── iliff-2012-scitranslmed.txt
│       │   └── ...
│       ├── embeddings/
│       │   ├── chroma-collection/         # ChromaDB vector store
│       │   └── metadata.yaml              # modelo de embeddings usado
│       ├── reviews/                       # reviews tratados separadamente
│       │   ├── nedergaard-2013-science.pdf
│       │   └── ...
│       ├── source-logs/
│       │   ├── pubmed-query.log           # queries executadas + counts
│       │   ├── arxiv-query.log
│       │   ├── biorxiv-query.log
│       │   └── manual-inclusions.log
│       └── excluded/                      # papers excluídos + razão
│           └── exclusion-log.yaml
```

---

## 2. Fontes (Sources)

### 2.1 Fontes primárias

| Fonte | URL | Query principal | Estimativa |
|-------|-----|------------------|------------|
| **PubMed** | https://pubmed.ncbi.nlm.nih.gov | MeSH terms + keywords | 400-600 papers |
| **arXiv** | https://arxiv.org | q-bio.NC, q-bio.TO, eess.IV | 20-60 papers |
| **bioRxiv** | https://www.biorxiv.org | neuroscience, AND glymphatic | 30-80 preprints |
| **Google Scholar** | https://scholar.google.com | validation cross-check | reference |

### 2.2 Fontes secundárias (validação)

- **Semantic Scholar API** — para enriquecer metadata (citações, author IDs)
- **OpenAlex** — open alternative para CrossRef, cobertura maior em 2017
- **CrossRef** — resolver DOIs, validar metadados

### 2.3 Fontes de reviews canônicas ≤2017

Reviews críticos (tratamento especial — Layer 1 primário):
- Nedergaard M. "Garbage Truck of the Brain" — Science 2013 (10.1126/science.1240514)
- Tarasoff-Conway JM et al. — Nature Reviews Neurology 2015 (10.1038/nrneurol.2015.119)
- Iliff JJ, Nedergaard M — Science 2013 review
- Jessen NA et al. — Neurochemical Research 2015 (10.1007/s11064-015-1581-6)
- Plog BA, Nedergaard M — Annual Review of Pathology 2018 (PUBLISHED Jan 2018 — CUTOFF RULE: check submission/acceptance date; if ≤2017-12-31, incluir com flag; senão excluir)

---

## 3. Queries Canônicas

### 3.1 PubMed Query Principal

```
(
  "glymphatic"[MeSH Terms] OR
  "glymphatic"[tiab] OR
  "glymphatic system"[tiab] OR
  "glymphatic pathway"[tiab] OR
  "paravascular clearance"[tiab] OR
  "paravascular pathway"[tiab] OR
  "perivascular space"[tiab] AND "brain"[tiab] OR
  "CSF-ISF exchange"[tiab] OR
  "brain waste clearance"[tiab] AND "astrocyte"[tiab]
)
AND (
  "2012/01/01"[Date - Publication] : "2017/12/31"[Date - Publication]
)
```

**Por que começar em 2012:** Iliff et al. 2012 é considerado o paper fundador do conceito "glymphatic system". Papers anteriores falam de "perivascular drainage" sem o framework unificado.

**Fallback include:** artigos-chave pré-2012 que são citados como fundadores (Rennels 1985, Cserr 1984):

```
(
  "perivascular drainage"[tiab] OR
  "paravascular drainage"[tiab] OR
  "brain interstitial fluid"[tiab] AND "bulk flow"[tiab]
)
AND "1980/01/01"[Date - Publication] : "2011/12/31"[Date - Publication]
```

Target: ~30-50 papers históricos para contexto.

### 3.2 Queries Auxiliares (Cross-Domain)

**Sleep research:**
```
("sleep"[tiab] AND "brain clearance"[tiab])
AND "2012/01/01":"2017/12/31"[Date - Publication]
```

**Alzheimer's / Amyloid clearance:**
```
("amyloid clearance"[tiab] OR "Aβ clearance"[tiab])
AND ("glymphatic"[tiab] OR "perivascular"[tiab])
AND "2012/01/01":"2017/12/31"[Date - Publication]
```

**AQP4 biology:**
```
("aquaporin-4"[MeSH] OR "AQP4"[tiab])
AND ("astrocyte"[tiab] OR "endfoot"[tiab] OR "endfeet"[tiab])
AND "2010/01/01":"2017/12/31"[Date - Publication]
```

**Meningeal lymphatic (cautious — bordeline período):**
```
("meningeal lymphatic"[tiab] OR "dural lymphatic"[tiab])
AND "2015/01/01":"2017/12/31"[Date - Publication]
```

Louveau et al. 2015 é publicado em julho/2015 (Nature). Incluir.

**Imaging methods ≤2017:**
```
("MRI"[tiab] OR "diffusion tensor"[tiab] OR "phase contrast"[tiab])
AND ("glymphatic"[tiab] OR "perivascular"[tiab] OR "CSF flow"[tiab])
AND "2012/01/01":"2017/12/31"[Date - Publication]
```

Taoka et al. 2017 (ALPS index) aparece aqui. Incluir.

### 3.3 arXiv Queries

```
# Category: q-bio.NC + eess.IV
title OR abstract:
  "glymphatic" OR "paravascular" OR "brain clearance" OR "CSF-ISF"
submitted: 2012-01-01 TO 2017-12-31
```

arXiv coverage de neurociência é baixa até 2017 — expect ~20 preprints.

### 3.4 bioRxiv Queries

```
keywords: glymphatic, perivascular, paravascular, CSF clearance
date range: 2013-11-01 (bioRxiv launch) TO 2017-12-31
```

Expect ~30-80 preprints. Muitos viram publicação peer-reviewed no período — deduplicar por DOI.

---

## 4. Filtros de Inclusão

### 4.1 Filtros obrigatórios (hard)

Um paper só entra no corpus se atende TODOS:

1. **Publication date ≤ 2017-12-31** (usar `published_online` ou `published_print`, o que vier primeiro)
2. **Tem DOI resolvível** via CrossRef (ou PMID se DOI não existe, raro)
3. **Está em inglês** (restrição prática — tradução excede budget)
4. **Não é retratado** (check PubMed retraction list + Retraction Watch)
5. **É peer-reviewed OU é preprint com relevância clara** (preprints indexados separadamente)
6. **Tem abstract em inglês** (mesmo que full-text seja paywall)

### 4.2 Filtros de relevância (scored)

Score de relevância (0-10) baseado em:
- Keyword density em title + abstract: 0-3 pts
- Cita ≥1 dos 5 papers fundadores: 0-2 pts
- Autor/lab reconhecido no campo: 0-2 pts
- Journal/venue peer-reviewed: 0-2 pts
- Citação count em 2017 (via Semantic Scholar): 0-1 pt

Threshold: score ≥ 5 para inclusão automática. Score 3-4 = revisão manual.

### 4.3 Balanço de coverage

Evitar over-indexing em um subtema. Garantir representação de:

| Subtema | Min papers | Max papers |
|---------|-----------|-----------|
| Mecanismos básicos (AQP4, perivascular flow) | 40 | 100 |
| Envelhecimento / idade | 20 | 50 |
| Alzheimer's / amyloid | 30 | 70 |
| Sleep | 20 | 50 |
| Imaging methods | 20 | 50 |
| Meningeal lymphatic | 10 | 30 |
| Stroke / TBI | 15 | 40 |
| Other (neurodegen, MS, glioma) | 15 | 40 |

Total estimado: **300-600 papers** (bate com estimativa do design brief).

---

## 5. Filtros de Exclusão

### 5.1 Exclusão automática

- Publication date > 2017-12-31 — CRITICAL (viola temporal cutoff)
- Retratado ou editorial notice de concerns → `excluded/retracted.yaml`
- Duplicata (mesmo DOI em múltiplas fontes) — deduplicar para preprint+published
- Comentários editoriais, cartas ao editor, errata (incluir como metadados mas não como source)
- Review de livro, protocolo de revisão, guidelines

### 5.2 Exclusão manual (caso-a-caso)

- Paper claims "glymphatic" mas contexto é não-relacionado (ex: "glymphatic" como termo ocasional em paper de diabetes)
- Paper é technical/methodological sem substance biológica
- Paper de teaching/education, não pesquisa primária

Todas exclusões manuais registradas em `excluded/exclusion-log.yaml` com rationale.

### 5.3 Casos borderline

| Caso | Decisão |
|------|---------|
| Paper submitted 2017, published online Jan 2018 | INCLUIR com flag; publication date do print decide |
| Preprint no bioRxiv 2017 + peer-reviewed 2018 | INCLUIR preprint version (se acessível); marcar |
| Paper em hebrew/chinese/japanese com abstract inglês | EXCLUIR (sem full text access) |
| Review 2017 que cita papers 2018 em pre-print forma | INCLUIR mas flag para L7 check |

---

## 6. Schema de Armazenamento

### 6.1 `MANIFEST.yaml` (index principal)

```yaml
manifest_version: "1.0"
corpus_name: "glymphatic-literature-2017"
temporal_cutoff: "2017-12-31"
build_date: "2026-05-02T12:00:00Z"  # Phase 2 target
total_papers: 487  # placeholder
total_reviews: 23
total_preprints: 41
sources_breakdown:
  pubmed: 412
  arxiv: 18
  biorxiv: 41
  manual_historical: 16
hash_corpus: "a3f5c9b2e1d7f8a4b6c2e9d4f1a7b3c8e6d2f9a1b4c7e3d8f2a6b9c1e4d7f3a8"
# hash é SHA-256 do tarball de papers.jsonl + abstracts.jsonl
query_log_hash: "b4d8a2c6e0f4a8b3c7d1e5f9a3b7c1d5e9f3a7b1c5d9e3f7a1b5c9d3e7f1a5b9"
status: "frozen"  # pode ser: draft, frozen, archived
```

### 6.2 `papers.jsonl` (one paper per line)

Cada linha é um JSON objeto:

```json
{
  "paper_id": "PAP-00001",
  "doi": "10.1126/scitranslmed.3003748",
  "pmid": "22896675",
  "arxiv_id": null,
  "biorxiv_id": null,
  "title": "A paravascular pathway facilitates CSF flow through the brain parenchyma and the clearance of interstitial solutes, including amyloid-β, from the mouse brain",
  "authors": [
    {"given": "Jeffrey J", "family": "Iliff", "orcid": "0000-0001-5810-6735"},
    {"given": "Minghuan", "family": "Wang"},
    "..."
  ],
  "journal": "Science Translational Medicine",
  "volume": "4",
  "issue": "147",
  "pages": "147ra111",
  "published_online": "2012-08-15",
  "published_print": "2012-08-15",
  "publication_year": 2012,
  "abstract": "Because the brain lacks a lymphatic system...",
  "mesh_terms": ["Animals", "Mice", "Aquaporin 4", "..."],
  "keywords": ["glymphatic", "paravascular", "CSF", "amyloid"],
  "citation_count_2017": 1247,
  "source": "pubmed",
  "include_verdict": true,
  "relevance_score": 9.8,
  "has_pdf": true,
  "pdf_path": "pdfs/iliff-2012-scitranslmed.pdf",
  "text_path": "extracted-text/iliff-2012-scitranslmed.txt",
  "embedding_id": "chroma-0001",
  "subtopic_tags": ["foundational", "paravascular", "CSF-ISF"],
  "retracted": false,
  "notes": "Foundational paper — introduces glymphatic system concept"
}
```

### 6.3 `bibliography.bib` (BibTeX)

Formato BibTeX padrão. Gerado automaticamente de `papers.jsonl` via script. Usado para citation em paper writing (Phase 5).

```bibtex
@article{iliff_2012_paravascular,
  author    = {Iliff, Jeffrey J. and Wang, Minghuan and Liao, Yonghong and ...},
  title     = {A paravascular pathway facilitates CSF flow through the brain parenchyma and the clearance of interstitial solutes, including amyloid-$\beta$, from the mouse brain},
  journal   = {Science Translational Medicine},
  volume    = {4},
  number    = {147},
  pages     = {147ra111},
  year      = {2012},
  doi       = {10.1126/scitranslmed.3003748},
  pmid      = {22896675}
}
```

### 6.4 Embeddings

**Modelo recomendado:** `voyage-3` (1024 dims, high performance, cost-effective) OU `text-embedding-3-large` da OpenAI (3072 dims).

**Fallback:** `text-embedding-3-small` (1536 dims) — mais barato.

**Texto embedado por paper:**
- Título + abstract concatenados (quando abstract existe)
- Se full-text disponível, também embedar chunks de 512 tokens com overlap 64

**Armazenamento:** ChromaDB local em `embeddings/chroma-collection/`.

**Usage pattern:** retrieval-augmented generation (RAG) durante Fases R-1 a R-5. Opus recebe top-K papers retrievados, não "lembra" o corpus.

---

## 7. Processo de Construção (Phase 2)

### 7.1 Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: Query Execution                                          │
│   - Executar queries PubMed, arXiv, bioRxiv                      │
│   - Log de counts per query                                      │
│   - Export metadata em JSON                                      │
│   Duration: ~2h (depends on API rate limits)                     │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: Deduplication & Merging                                  │
│   - Deduplicar por DOI                                           │
│   - Resolver preprint+published duplicates                       │
│   - Enriquecer metadata via Semantic Scholar                     │
│   Duration: ~1h                                                  │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: Filter Application                                       │
│   - Apply hard filters (temporal, DOI, language)                 │
│   - Apply relevance scoring                                      │
│   - Manual review of borderline cases                            │
│   Duration: ~4h (inclui manual review)                           │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: PDF Acquisition                                          │
│   - Download open-access PDFs                                    │
│   - Sci-Hub / institutional access para paywall (eticamente      │
│     relevantes — revisar com Magister)                           │
│   - Log missing PDFs para review manual                          │
│   Duration: ~6h                                                  │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 5: Text Extraction                                          │
│   - PDF → text via PyMuPDF ou similar                            │
│   - OCR para PDFs scaneados                                      │
│   - Clean-up (headers, footers, references)                      │
│   Duration: ~3h (automated)                                      │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 6: Embedding Generation                                     │
│   - Title+abstract → embedding                                   │
│   - Full-text chunking (512 tokens + 64 overlap)                 │
│   - Store in ChromaDB                                            │
│   Duration: ~2h + cost $50-100 in embedding API                  │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 7: Manifest Generation + Hash                               │
│   - Generate MANIFEST.yaml                                       │
│   - Compute SHA-256 of corpus tarball                            │
│   - Commit to git + tag                                          │
│   Duration: < 30min                                              │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 8: Validation & Audit                                       │
│   - Spot-check 20 random papers: metadata accuracy               │
│   - Verify no papers >2017 in corpus                             │
│   - Verify DOI resolution rate ≥98%                              │
│   - Magister signs off                                           │
│   Duration: ~3h                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Total Phase 2 duration estimate:** ~3 weeks (per original spec), ~22h of active work + async waits.

### 7.2 Owner matrix

| Step | Primary Owner | Support |
|------|---------------|---------|
| 1 (queries) | @analyst | @architect |
| 2 (dedup) | @data-engineer | @analyst |
| 3 (filter) | @analyst + Magister | — |
| 4 (PDF) | @analyst | Magister |
| 5 (text extract) | @data-engineer | — |
| 6 (embedding) | @data-engineer | @dev |
| 7 (manifest+hash) | @dev | @devops |
| 8 (validation) | Magister + @qa | consultor bioinformata (opcional) |

---

## 8. Validation Set (2017-2026) — Phase 4

A validação final (Phase 4, R-7) requer um **segundo corpus** com literatura 2017-2026 para checar predictions.

### 8.1 Estrutura paralela

```
literature-base-2017-2026/
├── MANIFEST.yaml
├── bibliography.bib
├── papers.jsonl
├── abstracts.jsonl
├── pdfs/
└── ...
```

Mesmo schema, mas com `temporal_range: "2018-01-01 to 2026-12-31"`.

### 8.2 Construção adiada

Este corpus NÃO é construído em Phase 2. É construído em Phase 4 (Validation) — propositalmente depois do hash-seal das predictions.

**Razão:** manter o Magister blind até o seal. Se o corpus 2017-2026 existir antes do seal, há risco de contaminação.

### 8.3 Construção by-prediction

Para cada predição hash-selada, buscar literatura 2017-2026 usando `expected_literature_signature` keywords:

```python
for prediction in sealed_predictions:
    search_query = " OR ".join(prediction.expected_literature_signature)
    results = pubmed_search(
        query=search_query,
        date_range=("2018-01-01", "2026-12-31")
    )
    store_in_validation_corpus(prediction.id, results)
```

Se < 5 papers são encontrados para uma predição, marcar `INCONCLUSIVE`.

---

## 9. Volume Estimado

### 9.1 Volume por fonte

Estimativa baseada em búsqueda preliminar:

| Source | Queries | Expected papers | After dedup |
|--------|---------|----------------|-------------|
| PubMed principal | ~800 raw | ~500 relevant | 400-450 |
| PubMed auxiliares | ~600 raw | ~200 novel | 80-120 |
| arXiv | ~50 raw | ~25 relevant | 15-20 |
| bioRxiv | ~150 raw | ~80 relevant | 30-50 (pós-dedup com PubMed) |
| Historical (pre-2012) | ~100 raw | ~40 relevant | 20-30 |

**Total esperado:** **~550-700 papers**

Mais conservador que os 2000-3000 papers mencionados no design brief — porque aplicamos filtros de relevância. Papers tangenciais (glymphatic mencionado mas não central) são excluídos.

Para 5000 tokens/paper médio (abstract + metadata), corpus total ~3M tokens indexados.

### 9.2 Volume mínimo para viabilidade

**Hard gate:** se após todos os filtros o corpus tem < 200 papers, volume insuficiente. Opções:

1. Relaxar filtros de relevância (score ≥ 3 em vez de ≥ 5)
2. Expandir histórico (pré-2012 até pré-2000)
3. Incluir domínios secundários (CRISPR base editing, mRNA, etc.) para paralelizar

**Soft gate:** se < 400 papers, recomendar expansão para 2-3 domínios secundários para fortalecer estatística.

---

## 10. Custo Estimado

| Item | Custo |
|------|-------|
| PubMed access | $0 (free) |
| arXiv access | $0 (free) |
| bioRxiv access | $0 (free) |
| Semantic Scholar API | $0 (free tier adequate) |
| CrossRef API | $0 (free) |
| PDF paywall (institutional) | $0 (Magister tem access) |
| Embedding API (Voyage ou OpenAI) | ~$50-100 (one-time) |
| ChromaDB hosting | $0 (local) |
| Storage (500 PDFs @ 2MB avg) | ~1GB — $0 |
| **Total** | **~$50-100** |

Trivial no budget de $5500 da expedição.

---

## 11. Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Paywall impede acesso a full-text de papers críticos | Institutional access via Magister; Sci-Hub como fallback ético-ambíguo (Magister decide) |
| PDF de 1990s sem OCR legível | Aceitar abstract-only; flag em papers.jsonl |
| bioRxiv indexação inconsistente pré-2015 | Manual curation dos anos 2013-2014 |
| Query PubMed retorna results irrelevantes | Iteração de query; manual review dos top 50 para calibrar |
| Embedding model muda comportamento | Fix model version em MANIFEST.yaml; re-embed se trocar |
| Paper claimado 2017 mas published online Jan 2018 | Regra: publication_print ≤ 2017-12-31 OU published_online ≤ 2017-12-31, o que vier primeiro |
| Corpus está frozen mas alguém commita mudança | Git tag + hash de corpus; auditar antes de qualquer uso |

---

## 12. Hash-Sealing do Corpus

Análogo ao hash-sealing das predições, o corpus também deve ser selado:

```bash
# 1. Gerar tarball determinístico
tar --sort=name \
    --mtime='2017-12-31 23:59:59 UTC' \
    --owner=0 --group=0 --numeric-owner \
    -cf literature-base-2017.tar \
    literature-base-2017/

# 2. Compute hash
sha256sum literature-base-2017.tar > literature-base-2017.tar.sha256

# 3. Commit to git
git add literature-base-2017.tar.sha256 MANIFEST.yaml
git commit -m "SEAL: corpus literature-base-2017 — SHA256=$(cat literature-base-2017.tar.sha256)"
git tag seal/corpus-2017-v1
```

O hash do corpus é referenciado em `predictions-sealed.yaml` metadata (`corpus_hash` field). Liga predictions ao corpus que as gerou — prova de ancoragem.

---

## 13. Cross-References

- `retrodiction-protocol-spec.md` §1.1 — Fase R-1 critérios de corpus
- Corpus RAG usage is described at high level in `retrodiction-protocol-spec.md` §3.R-3
- `predictions-schema.yaml` metadata_schema — `corpus_hash` field
- `leakage-measurement-plan.md` §1.3 — excerpt verification requer corpus

---

## 14. Changelog

- v1.0 (2026-04-22) — Spec inicial por Prometheus Lab, ready para execução em Phase 2.

---

*Literature Base Specification v1.0*
*"O corpus é o chão. O que não está nele, não existe."*
*Prometheus Lab — 2026-04-22*
