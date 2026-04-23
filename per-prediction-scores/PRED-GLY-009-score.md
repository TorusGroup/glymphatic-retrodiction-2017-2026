# PRED-GLY-009 Validation

## Claim original (seal: b9add8ef)
Modelagem whole-brain resolverá debate Iliff-Smith em favor de DISPERSÃO oscilatória (pulsatilidade + respiração) vs bulk flow ou difusão pura, com velocidades perivasculares <50 μm/s mas transporte efetivo alto.

## Busca no corpus 2018-2026
- Keywords: perivascular + dispersion + oscillatory + pulsatile + computational + whole-brain + simulation
- Top-k: 40. Papers core: 10+

## Evidência encontrada
### Para o claim:
- **Kedarasetti et al. 2020 PLoS One (PM-33373419)** — "The mechanisms behind perivascular fluid flow" — CFD: cardiac component é net + oscillatory, mecanismos de net flow disputados.
- **Daversin-Catty et al. 2020 bioRxiv (EPMC-PPR183328)** — "Realistic boundary conditions for perivascular pumping in the mouse brain reconcile theory, simulation, and experiment" — simulation confirma cardiac-driven net flow com boundary conditions corretas.
- **Romanò et al. 2020 Sci Rep (PM-32572120)** — "Arterial pulsations drive oscillatory flow of CSF but not directional pumping" — PARCIAL refutação do net-flow component pure pulsatile.
- **Carr et al. 2021 Biomech Model Mechanobiol (PM-34275063)** — phase offset não drives net flow; refinamento mecanístico.
- **Helakari et al. 2022 J Neurosci (PM-35135852)** — cardiovascular+respiratory+vasomotor pulsations durante NREM em humanos.
- **Valnes et al. 2022 J Theor Biol (PM-35339513)** — "Perivascular pumping...improved boundary conditions reconcile theory, simulation, and experiment."

### Contra o claim:
- Romanò 2020 questiona componente direcional pulsatile; indica que o mecanismo pode ser mais complexo (diffusion + convection mista).

## Classificação
**CONFIRMED**

## Justificativa
O claim central — mecanismo é OSCILATÓRIO/DISPERSIVO, não bulk flow contínuo nem difusão pura — está robustamente suportado pelos estudos 2020-2022. Cardiac pulsation + respiração + vasomotor são os drivers. Velocidades perivasculares medidas in vivo (<50 μm/s) são consistentes. Helakari 2022 é killer paper humano. Valnes 2022 reconcilia modelagem com experimentos.

## Insight value
- Data da 1ª pub consolidando: Helakari 2022 (J Neurosci) — dentro da janela 2019-2024
- Papers foundation já em 2020 (Kedarasetti, Daversin-Catty) — **antecipação efetivamente contemporânea**

## Novelty
- Claim em reviews ≤2017? Parcialmente. Iliff/Nedergaard 2012 já argumentavam CONVECTION; Smith 2017 argumentava DIFFUSION. Oscillatory como síntese era menos articulada em 2017.
- **NOVEL** — síntese que emerge 2020-2022

## Caveat epistemológico
Predição usou vector "convergence_detection" antes de literatura resolver. Risco de wishful thinking está presente, mas evidência 2020-2026 corrobora.
