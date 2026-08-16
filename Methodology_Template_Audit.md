# Methodology Template Audit

This addresses the second half of FILE 3's Item 3: stating how `methodology_rewrite_prompt_template.md` was used — the module mapping table, what changed in the Methodology, which equations were preserved, how new component names were propagated, and the ACTION REQUIRED list.
s
## A. Structural Compliance (Part A/C of the template)

The template asks for: an opening paragraph naming the top-level components, a "Pipeline Overview" subsection with a compact forward-pass equation, one subsection per named module (each with a figure reference and numbered equations), and a "Mathematical Formulation" subsection. Checked against Section III:

| Template requirement | Present in this paper? | Where |
|---|---|---|
| Opening paragraph naming top-level components | Yes | Section III opening ("The pipeline comprises seven stages...") |
| Pipeline Overview subsection + compact forward-pass equation | Yes | Section III-A, Eq. 1 |
| One subsection per named module, each with figure + equations | Yes | III-B (label derivation, Fig. 2), III-E.1 (Tissue Proportion Encoder), III-E.2 (Cross-Modal Gate), III-E.3 (Prediction heads) |
| Separate Mathematical Formulation subsection | Yes | Section III-F, Eq. 4-9 |
| Reimplementable depth | Yes | Hyperparameters (Table II), parameter counts, and equations together are sufficient to reimplement |

The current Methodology already follows the template's skeleton correctly. This is worth stating in the paper's own submission notes, since it answers the checklist item without needing further rewriting.

## B. Module Mapping Table (Part B of the template)

Hi-TGNet's named modules mapped against this paper's actual architecture. Unlike a typical run of this template — where every sample module gets re-themed into an equivalent — several rows below have **no equivalent**, and that's reported honestly rather than forced.

| Hi-TGNet module | Function in Hi-TGNet | This paper's equivalent | Status |
|---|---|---|---|
| Stagewise Context Encoder *E*(·) | 4-stage custom feature extractor, growing channel width | Frozen EfficientNet-B0 backbone φ_B0 | Present, but off-the-shelf and frozen rather than a custom stagewise design — a deliberate choice (Section III-E: "keeps training feasible without sustained accelerator access") |
| Adaptive Spiral Block | Multi-scale receptive field via parallel dilated depthwise branches | Tissue Proportion Encoder ψ(p) | Positional equivalent only — both are this paper's "first custom module," but functionally different: a 3→32→64 MLP lifting tissue proportions, not a spatial convolutional block |
| Hierarchical Tumor Guidance (feature reweighting + spatial guidance map) | Pathology-aware spatial attention | Cross-Modal Gate (γ, tanh(W_g·e + b_g)) | Positional equivalent — both gate the backbone features — but TGO-Net's gate is a single global scalar γ, not a spatial map. This is intentional: the paper's point is a *readable diagnostic number*, not a performance-oriented attention mechanism |
| Cross-Scale Attention fusion (combines 4 stages) | Multi-resolution feature consolidation | **None** | Missing. TGO-Net has no multi-stage features to fuse, since it uses a single frozen backbone output rather than a custom stagewise encoder. This follows necessarily from the design choice above, not an oversight — but see Action 1 below |
| Dual-head predictor (class logits + per-class uncertainty) | Classification + uncertainty estimate | CORAL head / binary head | Partial — produces class logits (ordinal or binary) but no separate uncertainty branch |

Three of five Hi-TGNet modules have a genuine, if simplified, equivalent (encoder, first custom module, gating module). Two do not (multi-scale fusion, uncertainty head) — both because TGO-Net is deliberately a lighter, diagnostic instrument rather than a performance architecture, which is consistent with how the paper frames it in Section VI ("we therefore present TGO-Net as an instrument rather than a performance contribution").

## C. Equations Preserved / Written

No prior version of this Methodology exists in the project to preserve equations *from* — Eq. 1 (forward pass) and Eq. 4-9 (tissue encoder, gate, CORAL loss, BCE loss, SMOTE interpolation) were written directly for this paper, not carried over from an earlier draft. They satisfy the template's requirement in form (compact forward pass + per-module numbered equations + dedicated formulation subsection) even though the process wasn't literally "rewrite and preserve."

## D. Propagation Check (Part E.2 of the template)

Whether the component names (TGO-Net, Tissue Proportion Encoder, Cross-Modal Gate, CORAL head) are used consistently everywhere the architecture is discussed:

| Location | Uses correct component names? |
|---|---|
| Abstract | Yes — "TGO-Net", "gate initialized at zero" |
| Contributions bullets | Yes — bullet 5 names all three sub-components explicitly |
| Critical Gaps mapping (Section II-E) | Yes — Gap 3 → Contribution 5, Gap 4 → Contribution 6, stated explicitly |
| Methodology | Yes — consistent throughout III-A, III-E, III-F |
| Results / Ablation (Table V) | Yes — "TGO-Net", "gated", "concat" variants named consistently |
| Discussion | Yes — "the TGO-Net results deserve care..." |
| Conclusion | Yes — "TGO-Net, a tissue-guided architecture with a zero-initialized gate..." |

This is fully consistent — no stale or mismatched terminology found anywhere in the manuscript.

## E. ACTION REQUIRED FROM ME

Items the template would flag that can't be resolved by rewriting text — they need either a decision or new work:

1. **No external validation of the same task on a second dataset.** The template (and Hi-TGNet) requires in-domain testing *and* external validation on a second dataset for the *same* prediction task. This paper's "control task" (DFUC 2024 infection) is a different task used for a different purpose — it isolates label provenance, not generalization. That's a legitimate substitution given the paper's negative-result framing (there's no valid severity classifier to externally validate), but it's worth stating explicitly as a deliberate deviation somewhere in Limitations, so it doesn't read as a missed requirement to anyone checking against the Hi-TGNet template.
2. **No uncertainty-estimation head.** Hi-TGNet's dual-head design outputs both a prediction and a per-class uncertainty. TGO-Net doesn't have an equivalent. This could be added (e.g., a Softplus branch alongside the existing head) if you want closer structural parity with the template — but it's optional, not required by the paper's own argument, and I'm not going to invent a result for it.
3. **Figure production tool.** The template specifies architecture figures should be built in PowerPoint/draw.io/Figma/Illustrator/Visio/Lucidchart, not screenshots. I can't verify what Fig. 1 and Fig. 2 were built with from here — worth confirming yourself since the instructions call this out explicitly as a hard requirement.
4. **Reference count (40-60, mostly 2023-2026).** Carried over from the AI Review Report — still 36 references, still the one open item shared across every checklist in this project.

Nothing else on the template's checklist is missing or fabricatable-but-absent — the rest is either genuinely present or a documented, deliberate design choice rather than a gap.
