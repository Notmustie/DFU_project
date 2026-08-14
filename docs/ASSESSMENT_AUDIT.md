# Audit against `Overall_assessment.docx`

That file is a reviewer report on a different manuscript (toxicity and
extremism classification), supplied as a specimen of the failure modes a
harsh reviewer looks for. Below, each of its ten criticisms is checked
against this paper.

---

## 1. Conceptual confusion between two constructs

**Their failure:** the title implied toxicity classification detects
extremism; the manuscript acknowledged the distinction occasionally, then
kept returning to claims that conflated them.

**Our analogous risk:** treating the infection control task as if it were
severity grading.

**Status: addressed, and strengthened after reading this.** Infection and
severity are now separated explicitly in three places: the abstract states
the infection task is used "strictly as a control condition and not as a
substitute for severity"; Section VII-C opens with a paragraph stating that
the two are different constructs, that infection is one of several criteria
contributing to a grade, and that no result in that section should be read
as a severity grading result; and Section IX repeats it. The comparison
table reports "n/a" for severity performance rather than substituting the
infection number.

## 2. Source leakage

**Their failure:** labels correlated with source dataset, so reported
accuracy may reflect dataset identification rather than the target task.

**Status: this is the paper's strongest section rather than a weakness.**
Section V-D documents dihedral-invariant content hashing, photograph
identity from the union of filename and pixel evidence, patient-grouped
folds, and verification on the image table across five keys. Cross-corpus
independence is measured, not assumed: 14 shared photographs, 0.2% and
0.3%. The reviewer's suggested remedy of a "source-only baseline" has a
direct analogue here in the negative control.

## 3. Contradictory labelling descriptions

**Their failure:** three sections gave incompatible accounts of how labels
were produced.

**Status: single account, stated once.** The rule appears exactly once, as
Equation 3, and is referenced by number thereafter. Every reported value
was read from the project result files rather than retyped, which removes
the mechanism by which such contradictions arise.

## 4. Overstated claims from small samples

**Their failure:** a multilingual claim resting on five French examples,
with none in the test set.

**Status: every small-n claim is bounded in the sentence that makes it.**
The mild class (30 photographs, about six per fold) is stated as not
measurable, with Wilson intervals reported. Grad-CAM used 16 held-out
images and the text says it is "sufficient to characterise the
area-normalised lift but not to support finer claims about attention
patterns." Expert agreement is reported as 134 matched images with the
inter-rater value given as the ceiling.

## 5. Unclear evaluation methodology

**Their failure:** "accuracy" undefined for a multi-label problem; single
fixed split; no significance analysis.

**Status: addressed.** Section VI-C names each metric and why it was
chosen. Five-fold patient-grouped cross-validation, not a single split.
Bootstrap confidence intervals with 2,000 resamples, paired t-tests across
shared folds, and Holm-Bonferroni correction across the tissue-pathway
family. Per-fold values are reported alongside pooled ones.

## 6. Model and loss inconsistencies

**Their failure:** table said cross-entropy, equation said binary
cross-entropy, for a multi-label sigmoid output.

**Status: consistent.** Equation 7 gives the CORAL objective for the
ordinal task and Equation 8 the weighted binary cross-entropy for the
binary task, with the head for each stated in Section V-E and repeated in
Table II. Optimiser, learning rate, batch size, epochs, patience, dropout,
gate initialisation and seed are all in Table II.

## 7. Baseline problems

**Their failure:** a large unexplained gap between baselines, and results
only in a figure rather than a table.

**Status: addressed.** Table V gives all nine executed configurations as
numbers. The one large gap, QWK 0.0000 to 0.9458 on the severity task, is
explained rather than left standing: the tissue input is the
label-generating variable, and the row is flagged in the table and analysed
in Section VII-E.

## 8. Mathematical inaccuracies

**Status: equations restated and checked.** Equations 1 to 10 cover the
forward pass, tissue proportions, the threshold rule, the encoder, the
gate, the CORAL head and its loss, the binary loss, the SMOTE simplex
property, and Grad-CAM with area normalisation. Tensor shapes are stated.
The parameter counts quoted (86,915 / 86,914 / 1.62%) were recomputed from
the instantiated model, not carried over.

## 9. AI-writing concerns

**Their failure:** repetitive claims of being "comprehensive" and
"innovative", inflated claims, terminology drift, figure captions that
narrate colours instead of interpreting results.

**Status: checked programmatically and by reading.** A scan for the
specific vocabulary they list returns nothing. Figure captions state what
the figure shows and what it means, not what colour the bars are. Section
VII-F explicitly refuses the available inflated claim by stating that
Grad-CAM alignment is not evidence of clinical correctness.

**You must still do the human audit they demand**, on every statistic,
citation, equation and figure interpretation, before submission. See the
action list in `PAPER_AUDIT.md`.

## 10. Tortured wording

**Status: written in plain declarative sentences.** Worth one careful
read-through before submission regardless.

---

## Correction made in this revision

**The title was wrong and is now restored.** You told me earlier not to
change the title or scope, and the v6 revision package respected that. When
I wrote the full manuscript I changed it anyway, to a title naming the
negative result. That was my error. The paper now carries your original
title exactly as it appears in `DFU_IEEE.docx`:

> Diabetic Foot Ulcers Severity Grading from Colour Wound Images Using Deep
> Learning and Tissue Mapped Explainable AI

The scope is unchanged from your earlier report: severity grading from
colour wound images, with tissue-mapped explainability. What differs is
that the derivation is now validated rather than assumed, and the outcome
is reported as measured.

**Student ID:** your earlier PDF used 25-93863-3 and `DFU_IEEE.docx` uses
211002042. The paper currently carries 211002042, taken from the newer
document. Correct it if that is wrong.

---

## Where this paper still differs from the earlier report

These are consequences of the completed experiments, not scope changes.

| Earlier report | Now |
|---|---|
| Kappa 0.1534 as the headline | Measured −0.025 / +0.036, inter-rater 0.254 |
| "Results pending" in three tables | All nine configurations executed |
| Three CNN backbones compared | Frozen-probe comparison plus TGO-Net |
| Grad-CAM alignment as a contribution | Reported, with its validity limit stated |
| Severe class 74.8% | 65.0% after consolidation |
| 9,385 images | 9,881 images, 3,614 photographs |
