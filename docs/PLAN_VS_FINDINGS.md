# From Proposal to Findings: What Changed and Why

This document explains the project in plain terms. It covers what was
originally planned, what testing found, and what had to change as a
result. The title and topic did not change. The conclusion did.

---

## 1. The original plan

The proposal, as written in the earlier report, was this:

Grade diabetic foot ulcer severity (mild, moderate, severe) from a colour
photograph of the wound, with no clinical data attached. No public dataset
has severity labels, so the plan was to create them: cluster the wound
image by colour into three tissue types, measure how much of the wound
each type covers, and turn those measurements into a severity label using
threshold rules based on the Wagner grading scale.

Once labels existed, the plan was to train and compare three CNN
architectures (ResNet50, EfficientNet-B0, MobileNetV2) on those labels, and
use Grad-CAM to show that each model's attention lined up with the tissue
type expected for its predicted grade. This would give a full working
pipeline: image in, severity grade out, with a visual explanation attached.

At the time the report was written, this pipeline was built but not yet
tested. The paper said "results pending" in three separate places.

## 2. What testing found

Four checks were run against the derived labels, each designed to catch a
different way the labelling could be wrong.

**Check 1: Do the labels agree with what a clinician would say?**
Two independent reviewers graded a sample of the same images. Agreement
between the derived label and each reviewer was close to zero
(kappa −0.025 and +0.036). For comparison, the two reviewers agreed with
each other at kappa 0.254, which is itself only moderate. The derived
labels did not come close to that.

**Check 2: Does the method behave correctly on an image with no wound at
all?**
The same labelling process was run on photographs of healthy, undamaged
skin. If the method worked, every one of these should be labelled mild,
since there is no wound. Instead, 60% were labelled severe.

**Check 3: Does the same photograph get the same label twice?**
Many images in the dataset are the same photograph, saved multiple times
with small variations (rotated, flipped, slightly recoloured). These
variations do not change the wound. If the labelling method were reading
the wound correctly, all copies of one photograph should get the same
label. Instead, 62% of photographs with more than one copy got
inconsistent labels across their own copies.

**Check 4: Does the resulting mix of labels look like a real patient
population?**
Two out of every three images ended up labelled severe. No real clinical
population looks like that.

All four checks failed. Together they point to the same root cause: the
clustering step cannot tell the difference between "necrotic tissue" and
"anything dark in the photo," including shadows, wound depth, and
darker skin tone. It does not measure tissue type. It measures darkness.

## 3. Why this forced a change in scope

The original plan assumed the derived labels were a usable stand-in for
real clinical grades. That assumption turned out to be false, and the four
checks show it directly rather than by inference.

This creates a problem for the second half of the original plan. Training
three CNN backbones to predict these labels, and showing Grad-CAM lines up
with the expected tissue zone for each grade, only means something if the
grade itself means something. If the grade is close to random noise
relative to true severity, a model that predicts it well has learned to
predict the noise, not the wound. Reporting that as a working severity
classifier would overstate what was actually built.

So the plan had to adapt. Two changes followed directly from the four
failed checks:

**Change 1: the project stopped trying to fix the label derivation.**
Two rounds of threshold recalibration were tried before this validation
work (the original report mentions kappa improving from 0.08 to 0.15
through one such recalibration). The four checks explain why further
recalibration would not help. The problem is not the threshold values. It
is that colour alone does not contain the information severity grading
needs, chiefly wound depth, which no photograph captures. No threshold
adjustment fixes a variable that is not being measured.

**Change 2: a control experiment was added to answer the obvious
follow-up question.**
If the severity classifier does not work, the natural doubt is whether the
problem is the labels or the modelling pipeline itself, the CNN, the
training setup, the code. To answer this without ambiguity, the exact same
pipeline (same architecture, same preprocessing, same evaluation method)
was pointed at a different task: predicting infection status on wound
photographs that do carry real expert labels from clinicians. On that task,
the same pipeline reached a reasonable working accuracy (AUROC 0.81). This
shows the pipeline itself works. It fails specifically when asked to
predict a target derived from colour alone, because that target does not
correspond to anything real.

## 4. What stayed the same

- The title and the topic: severity grading of diabetic foot ulcers from
  colour images.
- The dataset sources.
- The tissue-based colour derivation method itself, tested exactly as
  designed.
- The intent to explain model behaviour visually (Grad-CAM), though its
  role changed (see below).

## 5. What changed

| Planned | What happened instead |
|---|---|
| Report a working 3-class severity classifier | Report that the derived labels do not measure severity, and show why |
| Compare 3 CNN backbones on severity accuracy | Report the severity ablation honestly, including the one result that looks good but is circular (explained below) |
| Grad-CAM shows the model attends to the correct tissue for its predicted grade | Grad-CAM is reported as showing where the model looks, not as proof it looks at the right tissue, because the tissue reference itself is not validated |
| Conclusion: a reproducible severity tool | Conclusion: severity cannot be recovered from colour alone; the missing piece is real clinical labels, not a better model |

One additional finding came out of testing that was not part of the
original plan at all. A custom module (TGO-Net) was built to feed the
tissue measurements into the model directly. On the derived labels, this
module appears to work extremely well. But this is misleading: the tissue
measurements are the same numbers used to create the label in the first
place, so feeding them back into the model is close to giving it the
answer. On the infection task, where labels come from real clinicians and
this shortcut does not exist, the same module makes results worse, not
better. This is reported directly rather than left out, because it is
further evidence for the same conclusion: colour-derived measurements do
not carry real severity information.

## 6. The one-sentence version

The project set out to build a severity classifier from colour photographs.
Testing showed the labels needed to train that classifier cannot be
trusted, and showed exactly why. The scope shifted from "here is a working
classifier" to "here is proof this specific approach cannot work, and here
is the evidence that the failure is the labels and not the model."
