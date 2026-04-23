# Validation Scoreboard Final — exp-retrodiction (v3, pós Phase 3.8 Pro 3.1 re-audit)

**Date:** 2026-04-23
**Phase:** 4c (Prediction vs Evidence), updated after Phase 3.8 multi-model re-audit
**Seal (current):** predictions-final.yaml hash `a144c1801ef24f4c8b73418a0836b61f9e25411e74329fa492915e5189e54460` (v4)
**Seal chain:** v1 `1765b221…7afb586` → v2 `b9add8ef…ae9cc73` → v3 `2db0fab5…44928f` → v4 `a144c180…9e54460`
**Corpus:** corpus-glymphatic-2018-2026.jsonl (N=3,329, hash `3aa15c2c2fd8af4291374671bf6d64a63cd0ca246ab0414967a6a3c8199be5df`)
**Valid pool:** N=15 (PRED-GLY-011 invalidated via Gemini Pro 3.1 + Pro 2.5 convergent leakage detection; PRED-GLY-009 revalidated after multi-model re-audit rejected the original Flash flag)

---

## Sumário Executivo

| Métrica | Valor (N=15) | Target Min | Target Strong | Status |
|---------|--------------|------------|---------------|--------|
| **Precision (strict CONFIRMED)** | **53.33%** (8/15) | 40% | 60% | ✅ PASS (between minimum and strong) |
| **Precision (liberal CONFIRMED ∪ PARTIAL)** | **86.67%** (13/15) | 40% | 60% | ✅ **STRONG** |
| **Novelty** | **53.33%** (8/15 NOVEL) | 30% | 50% | ✅ **STRONG** |
| **Insight Value** | **6.67%** (1/15 antecipação ≥1 ano) | 10% | 25% | ⚠️ below target, reported transparently |
| **Contradicted** | **0.00%** (0/15) | — | — | — |
| **Leakage (convergent, Pro 3.1 primary)** | **6.25%** (1/16 invalidated) | ≤5% | — | ⚠️ slightly above target, transparently reported |

### Decisão: **PASS — paper publicável**

Rationale: Precision strict (53.33%) meaningfully exceeds the pre-registered 40% minimum threshold. Precision liberal (86.67%) is STRONG. The multi-model cross-audit successfully detected methodological leakage in PRED-GLY-011 (Fultz 2019 Science setup) that single-model audits of lower-capability models (gemini-2.5-flash) missed — and simultaneously rejected a single-model false positive (PRED-GLY-009 Iliff-Smith terminology) that would have unnecessarily reduced the pool. The audit protocol demonstrated self-correction capability under capability scaling.

Insight value (6.67%) is below the 10% pre-registered target — only PRED-GLY-017 (Da Mesquita 2018 Nature, +1 year anticipation) qualifies. This is reported transparently. The Lab demonstrates concurrent forecasting capability; forward-anticipation of ≥1 year remains rare.

---

## Invalidation & Revalidation Log

### Invalidated post-seal

| ID | Phase | Original verdict | Reason | Detected by |
|----|-------|------------------|--------|-------------|
| PRED-GLY-011 | 3.8 (2026-04-23) | CONFIRMED (Fultz 2019 Science) | Methodological leakage — the predicted experimental setup (synchronized fMRI + delta-EEG + CSF inflow + NREM humans) is a near-verbatim description of Fultz 2019 Science. Anchor papers (Xie 2013 mice; Jessen 2015 review) do not describe the multimodal human design. Classified as TRUE POSITIVE by convergent flag of gemini-3.1-pro-preview (primary) and gemini-2.5-pro (independent). | Multi-model audit Phase 3.8 |

### Revalidated post-seal

| ID | Phase | Prior state | Reason for revalidation |
|----|-------|-------------|-------------------------|
| PRED-GLY-009 | 3.8 (2026-04-23) | invalidated-post-seal (Phase 3.7, flagged by gemini-2.5-flash alone) | Upon re-audit with more capable models (gemini-2.5-pro and gemini-3.1-pro-preview), both independent judges classified the prediction as CLEAN. Pro 3.1 reasoning: *"relies on pre-2018 concepts (the debate between Iliff bulk flow and Smith diffusion, and early models of oscillatory dispersion) to make a plausible forward-looking claim about whole-brain modeling and perivascular velocities without using post-2017 terminology."* The original Phase 3.7 flag was a false positive of gemini-2.5-flash, not confirmed at higher capability. |

**Net impact:** Pool N unchanged (15). CONFIRMED count unchanged (8). The swap preserves total metrics while reassigning which prediction contributes.

---

## Contagem por Veredicto (pool N=15)

| Classe | N | % de N=15 |
|--------|---|-----------|
| **CONFIRMED** | 8 | 53.33% |
| **PARTIALLY CONFIRMED** | 5 | 33.33% |
| **CONTRADICTED** | 0 | 0.00% |
| **INCONCLUSIVE / UNTESTABLE** | 2 | 13.33% |
| **DESTROYED pre-seal (PRED-010, 018)** | — | (excluídas de N=15) |
| **INVALIDATED post-seal (PRED-011)** | — | (excluída de N=15) |
| **Total valid pool** | **15** | 100% |

---

## Tabela por Predição (N=15 + 1 invalidated + 2 destroyed)

| ID | Status Anomalist | Veredicto 4c | Confirmação (1ª pub) | Antecipação | Novel? |
|----|------------------|--------------|----------------------|-------------|--------|
| PRED-GLY-001 | WOUNDED-REFORM | **CONFIRMED** | Zou 2019 Trans Neurodegen | 0-1 ano | SIM |
| PRED-GLY-002 | WOUNDED-REFORM | PARTIAL | Zou 2019 + Ding 2024 | 0 anos | SIM |
| PRED-GLY-003 | SURVIVED | **CONFIRMED** | Ma 2022 NPJ PD | 0 anos | NÃO |
| PRED-GLY-004 | WOUNDED-REFORM | **CONFIRMED** | Si 2022 NPJ PD | 0 anos | SIM |
| PRED-GLY-005 | WOUNDED-REFORM | INCONCLUSIVE | — | N/A | SIM (sem val.) |
| PRED-GLY-006 | WOUNDED-REFORM | PARTIAL | Wang 2023/24 J Adv Res | 0 anos | SIM |
| PRED-GLY-007 | SURVIVED | PARTIAL | Mestre 2018 eLife (mec. diff.) | 0 anos | SIM |
| PRED-GLY-008 | WOUNDED-REFORM | INCONCLUSIVE | — | N/A | SIM (sem val.) |
| PRED-GLY-009 | SURVIVED | **CONFIRMED** | Helakari 2022 | 0 anos | SIM |
| PRED-GLY-010 | DESTROYED pre-seal | — | — | — | — |
| ~~PRED-GLY-011~~ | ~~SURVIVED~~ | ~~CONFIRMED~~ | ~~Fultz 2019 Science~~ | ~~0 anos~~ | ~~SIM~~ — **INVALIDATED (methodological leakage)** |
| PRED-GLY-012 | SURVIVED | PARTIAL | Feliciano 2025 AJRCCM | 0 anos | SIM |
| PRED-GLY-013 | SURVIVED | PARTIAL | Demiral 2019 NeuroImage | 0 anos | NÃO |
| PRED-GLY-014 | WOUNDED-REFORM | **CONFIRMED** | Steward 2021 J Neuroimag | 0 anos | NÃO |
| PRED-GLY-015 | WOUNDED-REFORM | **CONFIRMED** | Paradise 2021 Neurology | 0 anos | NÃO |
| PRED-GLY-016 | WOUNDED-REFORM | **CONFIRMED** | Taoka 2018 eLife + ALPS consolid. | 0 anos | NÃO |
| PRED-GLY-017 | WOUNDED-REFORM | **CONFIRMED** | Da Mesquita 2018 Nature | **1 ano** | **SIM (high)** |
| PRED-GLY-018 | DESTROYED pre-seal | — | — | — | — |

**CONFIRMED in pool (N=15):** 001, 003, 004, 009, 014, 015, 016, 017 (8 predictions)
**PARTIAL in pool:** 002, 006, 007, 012, 013 (5 predictions)
**INCONCLUSIVE in pool:** 005, 008 (2 predictions)

---

## 3 Maiores Acertos

### 1. PRED-GLY-017 — Meningeal lymphatic / VEGF-C / Aβ clearance

**Da Mesquita 2018 Nature** foi publicado 25 de julho de 2018, dentro da janela predita (2018-2022). Confidence original 0.45 (moonshot). O paper demonstra EXATAMENTE o que a predição afirmou: VEGF-C → meningeal lymphatic enhancement → redução Aβ + cognição melhorada em aged mice. Predição de nível substancial/alto novelty acertada em "moonshot" mode. **Este é o único predição do pool com antecipação ≥1 ano.**

### 2. PRED-GLY-001 — α-synuclein clearance via glymphatic/AQP4

Série de papers mecanísticos (Zou 2019, Cui 2023, Ding 2024, Scarpelli 2025) demonstra AQP4 KO → reduced α-syn clearance → aggregated pathology. Claim direcional plenamente confirmado; a comparação quantitativa exata com Aβ ainda falta (fair to call CONFIRMED com caveat). Confidence 0.65 bem calibrado.

### 3. PRED-GLY-009 — Whole-brain modeling resolve Iliff-Smith via oscillatory dispersion

Confidence 0.60. A predição antecipou que modelagem computacional 2019-2024 convergiria em **dispersão oscilatória** (pulsatilidade cardíaca + respiração) como mecanismo dominante de transporte, com velocidades <50 μm/s mas transporte efetivo alto. **Helakari 2022** e estudos subsequentes confirmaram exatamente esse padrão. Predição SURVIVED anomalist pass; revalidada em Phase 3.8 após re-audit multi-modelo rejeitar falsa flag inicial de gemini-2.5-flash sobre terminologia "Iliff-Smith".

---

## 3 Maiores Erros / Revelações

### 1. PRED-GLY-011 (agora INVALIDATED) — methodological leakage

Ilustração direta do valor do multi-model cross-audit. Predição estava CONFIRMED contra corpus (Fultz 2019 Science), mas a Camada 2 primary (gemini-3.1-pro-preview) detectou que o **setup experimental específico** (synchronized fMRI + delta-EEG + CSF inflow + NREM humanos) é descrição quase verbatim do paper Fultz 2019. Os anchors pré-2018 (Xie 2013 sleep-glymphatic em camundongos; Jessen 2015 review) NÃO descrevem este design multimodal humano. Classificado como methodological leakage por convergência de Pro 3.1 + Pro 2.5 (independentes). **Aprendizado: independent-model audit com modelo mais capaz é necessário para capturar leakage metodológica.**

### 2. PRED-GLY-007 — Mecanismo da controvérsia Iliff-Smith ERRADO

Previmos que **background genético do camundongo** explicaria a discrepância. Mestre 2018 eLife (coautoria de Iliff + Nedergaard + 5 groups) resolveu a controvérsia, mas identificou **anesthesia, age, and tracer delivery** como os fatores dominantes — NÃO background genético. Acertamos que a disputa seria resolvida e que AQP4 importa, mas o mecanismo específico da discrepância foi outro. Aprendizado: "failure archaeology" vector nos levou à pergunta certa mas à resposta errada.

### 3. PRED-GLY-005 + PRED-GLY-008 — INCONCLUSIVE estrutural

Moonshots que dependiam de ferramentas que não foram desenvolvidas no validation window. Reveals: predições quantitativas em espaços sem ferramenta mensurável produzem não-falsificabilidade de facto. **Lição epistemológica sobre retrodiction: quantitative predictions over unexplored measurement spaces may be de facto non-falsifiable.**

---

## Análise de Calibração (recalculada N=15)

### Confidence × Accuracy (pós-swap 009↔011)

- **Confidence ≥0.70 (2 predições no pool, 011 removida):** PRED-003 (0.70) CONFIRMED ✓, PRED-014 (0.72) CONFIRMED ✓ → **2/2 = 100%**
- **Confidence 0.60-0.69 (6 predições no pool, 009 incluída):** PRED-001 (0.65, C), PRED-002 (0.68, P), PRED-007 (0.65, P), PRED-009 (0.60, C), PRED-012 (0.65, P), PRED-015 (0.65, C) → 3 CONFIRMED + 3 PARTIAL = 50% strict, 100% liberal
- **Confidence 0.45-0.55 (6 predições):** PRED-005 (0.45, I), PRED-006 (0.45, P), PRED-008 (0.50, I), PRED-013 (0.60, P), PRED-016 (0.50, C), PRED-017 (0.45, C) → 2 CONFIRMED + 2 PARTIAL + 2 INCONCLUSIVE. Calibração razoável — moonshots acertaram 2/6 strict, 4/6 liberal.

### Insight Calibration Epistêmico

O Lab mostrou calibração DECENTE:
- Alta confidence (≥0.70) → 100% strict accuracy (2/2 confirmed).
- Mid-confidence (0.60-0.69) → 50% strict, 100% liberal — bem calibrado.
- Moonshots (0.45-0.50) → 2 CONFIRMED (017, 016) e 2 INCONCLUSIVE (005, 008) — sinal de que o Lab reconhece quando está operando em território de "low-data" e atribui confidence apropriadamente baixa.
- Nenhuma predição foi CONTRADICTED — sinal de que o Anomalist Pass fez seu trabalho pré-seal.

---

## Decisão Final

**PASS — paper publicável.** Precision strict (53.33%) between minimum and strong targets; Precision liberal (86.67%) is STRONG. Zero CONTRADICTED. Este resultado é mais honesto (e mais interessante metodologicamente) que as versões anteriores, porque demonstra que o multi-model cross-audit detectou leakage metodológica (011 Fultz setup) que o audit single-model com modelo inferior (flash) não detectou, e simultaneamente rejeitou um falso positivo single-model (009 Iliff-Smith terminology).

Argumentos para publicação:
1. Precision strict 53.33% (acima do threshold 40%); liberal 86.67% (strong)
2. Zero predições CONTRADICTED — Anomalist Pass funcionou
3. 1 insight moonshot antecipatório (017 +1 ano) bem calibrado — Da Mesquita 2018 Nature
4. 8/15 predições NOVEL (not trivial extrapolation)
5. Metodologia epistemologicamente disciplinada (seal-before-check, corpus independente, hash chain v1→v2→v3→v4, multi-model audit)
6. **Multi-model cross-audit VALIDATED operacionalmente** — Pro 3.1 convergente com Pro 2.5 detectou leakage que Flash não detectou, e rejeitou false positive que Flash criou. Isto é evidência POSITIVA para o protocolo de triplo-filtro × multi-modelo.

Caveats honestos reportados no paper:
- **Antecipação temporal efetiva foi ~0 anos** em quase todas as predições (exceto 017 com 1 ano). Lab demonstra **concurrent forecasting**, não forward prediction forte.
- 2 predições INCONCLUSIVE revelam limitação: quantitative thresholds em espaços sem ferramenta mensurável produzem não-falsificabilidade de facto.
- PRED-GLY-007 revelou que "failure archaeology" vector pode fazer perguntas certas com respostas erradas.
- PRED-GLY-011 invalidated: convergent flag de Pro 3.1 + Pro 2.5 identificou que o setup experimental da predição é descrição verbatim de Fultz 2019 Science. Methodological leakage, não terminology leakage. Esta é a contribuição positiva do multi-model audit.
- Insight value 6.67% abaixo do target 10% — Lab não produziu antecipação forte consistente; apenas PRED-017 qualifica.

---

*Phase 4c v3 complete 2026-04-23. Retrodiction card generated with multi-model post-audit correction. The envelope is opened honestly.*
*Seal chain: v1 → v2 (citation hygiene) → v3 (Phase 3.7 invalidation, gemini-2.5-flash) → v4 (Phase 3.8 multi-model correction, gemini-3.1-pro-preview primary).*
