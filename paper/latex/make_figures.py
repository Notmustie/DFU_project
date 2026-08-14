"""
Vector figures for the paper: pipeline overview and TGO-Net architecture.
Rendered with matplotlib to PDF (vector) and PNG (preview).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from pathlib import Path

OUT = Path('figures'); OUT.mkdir(exist_ok=True)

INK   = '#14313D'
MUTE  = '#5B7683'
TEAL  = '#2E7D8F'
AMBER = '#D97706'
CRIM  = '#BE123C'
GREEN = '#15803D'
LILAC = '#6D5BA6'
BG1   = '#E8F1F4'
BG2   = '#FDF0E3'
BG3   = '#FBE9ED'
BG4   = '#ECEAF6'

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8})


def box(ax, x, y, w, h, label, sub=None, fc='#FFFFFF', ec=INK, fs=8.2,
        lw=1.0, tc=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle='round,pad=0.004,rounding_size=0.012',
                                facecolor=fc, edgecolor=ec, linewidth=lw))
    tc = tc or INK
    if sub:
        ax.text(x + w/2, y + h*0.62, label, ha='center', va='center',
                fontsize=fs, fontweight='bold', color=tc)
        ax.text(x + w/2, y + h*0.26, sub, ha='center', va='center',
                fontsize=fs - 1.5, color=MUTE)
    else:
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=fs, fontweight='bold', color=tc)


def group(ax, x, y, w, h, title, color):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=color,
                           linewidth=1.1, linestyle=(0, (5, 3))))
    ax.text(x + 0.008, y + h - 0.014, title, fontsize=7.6,
            color=color, fontweight='bold', va='top')


def arrow(ax, x1, y1, x2, y2, label=None, color='#8FA9B4', style='-|>',
          rad=0.0, fs=6.8):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=11, color=color, lw=1.15,
                                 connectionstyle=f'arc3,rad={rad}'))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.014, label, ha='center',
                fontsize=fs, color=MUTE)


# =====================================================================
# FIGURE 1 — pipeline overview
# =====================================================================
def fig_pipeline():
    fig, ax = plt.subplots(figsize=(14.0, 8.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    # ---- stage A: identity resolution
    group(ax, 0.015, 0.70, 0.30, 0.27, 'A  Identity resolution', TEAL)
    box(ax, 0.03, 0.885, 0.125, 0.055, 'Roboflow DFU', '9,881 files', BG1)
    box(ax, 0.175, 0.885, 0.125, 0.055, 'DFUC 2024', '5,372 files', BG1)
    box(ax, 0.03, 0.805, 0.27, 0.055, 'dihedral-invariant 256-bit hash',
        '16x16 square grid, Hamming clustering', '#FFFFFF')
    box(ax, 0.03, 0.725, 0.27, 0.055, 'photograph unit',
        'union of filename id and content cluster', BG1)

    # ---- stage B: label derivation
    group(ax, 0.36, 0.70, 0.29, 0.27, 'B  Label derivation', AMBER)
    box(ax, 0.375, 0.885, 0.26, 0.055, 'CIE LAB k-means, k = 3',
        'clusters ordered by luminance', BG2)
    box(ax, 0.375, 0.805, 0.26, 0.055, 'tissue proportions',
        r'$\rho_{nec}, \rho_{sl}, \rho_{gran}$', BG2)
    box(ax, 0.375, 0.725, 0.26, 0.055, 'threshold rule',
        r'severe := $\rho_{nec} \geq 0.20$', BG2)

    # ---- stage C: validation
    group(ax, 0.665, 0.70, 0.32, 0.27, 'C  Label validation', CRIM)
    for i, (t, s) in enumerate([('expert agreement', r'$\kappa$'),
                                ('negative control', 'lesion-free skin'),
                                ('stability', 'across augmented copies')]):
        box(ax, 0.68, 0.885 - i*0.08, 0.29, 0.055, t, s, BG3)

    arrow(ax, 0.305, 0.835, 0.372, 0.835)
    arrow(ax, 0.645, 0.835, 0.677, 0.835)

    # ---- stage D: split
    box(ax, 0.20, 0.575, 0.60, 0.062, 'D  Patient-grouped 5-fold split',
        'verified on the image table across five keys; zero leakage',
        '#FFFFFF', TEAL, 8.6)
    arrow(ax, 0.50, 0.695, 0.50, 0.642)

    # ---- stage E: two tasks
    group(ax, 0.015, 0.20, 0.47, 0.33, 'E  Severity task (derived labels)', AMBER)
    box(ax, 0.03, 0.435, 0.44, 0.055, 'frozen EfficientNet-B0',
        '1,280-d features, 3,614 photographs', BG2)
    box(ax, 0.03, 0.355, 0.205, 0.055, 'CNN-only', 'softmax / CORAL', '#FFFFFF')
    box(ax, 0.265, 0.355, 0.205, 0.055, 'TGO-Net', 'tissue + gate', BG2)
    box(ax, 0.03, 0.275, 0.44, 0.055, 'six-configuration ablation',
        'with and without tissue, gate, SMOTE', '#FFFFFF')
    box(ax, 0.03, 0.215, 0.44, 0.045, 'QWK, macro F1, severe-vs-rest F1',
        None, BG2, INK, 7.6)

    group(ax, 0.515, 0.20, 0.47, 0.33, 'F  Control task (expert labels)', TEAL)
    box(ax, 0.53, 0.435, 0.44, 0.055, 'identical pipeline, identical folds',
        '4,542 photographs, 1,417 patients', BG1)
    box(ax, 0.53, 0.355, 0.205, 0.055, 'frozen probe', 'linear head', '#FFFFFF')
    box(ax, 0.765, 0.355, 0.205, 0.055, 'fine-tuned', 'backbone unfrozen', BG1)
    box(ax, 0.53, 0.275, 0.44, 0.055, 'per-photograph aggregation',
        'scores averaged before any metric', '#FFFFFF')
    box(ax, 0.53, 0.215, 0.44, 0.045, 'AUROC, AUPRC, MCC, sensitivity, specificity',
        None, BG1, INK, 7.6)

    arrow(ax, 0.35, 0.570, 0.25, 0.535)
    arrow(ax, 0.65, 0.570, 0.75, 0.535)

    # ---- stage G: comparison
    box(ax, 0.13, 0.075, 0.74, 0.075,
        'G  Control comparison: same architecture, same folds, same code',
        'the only variable is label provenance', BG4, LILAC, 9.0)
    arrow(ax, 0.25, 0.195, 0.35, 0.155)
    arrow(ax, 0.75, 0.195, 0.65, 0.155)

    # explainability side note
    box(ax, 0.015, 0.075, 0.10, 0.075, 'Grad-CAM', 'attention', '#F3F6F7',
        MUTE, 7.6)
    arrow(ax, 0.115, 0.112, 0.128, 0.112)

    fig.savefig(OUT / 'fig_pipeline.pdf', bbox_inches='tight', facecolor='white')
    fig.savefig(OUT / 'fig_pipeline.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('wrote fig_pipeline.pdf / .png')


# =====================================================================
# FIGURE 2 — TGO-Net architecture
# =====================================================================
def fig_architecture():
    fig, ax = plt.subplots(figsize=(14.0, 6.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    # ---- inputs
    box(ax, 0.015, 0.72, 0.155, 0.10, 'wound image', r'$3 \times 224 \times 224$',
        BG1, INK, 8.2)
    box(ax, 0.015, 0.30, 0.155, 0.10, 'tissue vector',
        r'$p \in \Delta^2$,  3-d', BG2, INK, 8.2)

    # ---- frozen backbone
    box(ax, 0.215, 0.72, 0.185, 0.10, 'EfficientNet-B0', 'FROZEN  5.29 M',
        '#EDF2F4', MUTE, 8.2)
    ax.text(0.3075, 0.685, r'$z \in \mathbb{R}^{1280}$', ha='center',
            fontsize=7.6, color=MUTE)
    arrow(ax, 0.172, 0.77, 0.212, 0.77)

    # ---- tissue encoder
    group(ax, 0.205, 0.155, 0.205, 0.39, 'Tissue Proportion Encoder', AMBER)
    box(ax, 0.218, 0.44, 0.18, 0.052, 'Linear 3 -> 32', None, BG2, INK, 7.8)
    box(ax, 0.218, 0.375, 0.18, 0.052, 'LayerNorm + GELU', None, '#FFFFFF',
        INK, 7.8)
    box(ax, 0.218, 0.31, 0.18, 0.052, 'Linear 32 -> 64', None, BG2, INK, 7.8)
    box(ax, 0.218, 0.245, 0.18, 0.052, 'LayerNorm + GELU', None, '#FFFFFF',
        INK, 7.8)
    ax.text(0.3075, 0.192, r'$e \in \mathbb{R}^{64}$   2,432 params',
            ha='center', fontsize=7.4, color=MUTE)
    arrow(ax, 0.172, 0.35, 0.215, 0.40, rad=0.12)

    # ---- gate
    group(ax, 0.435, 0.155, 0.235, 0.39, 'Cross-Modal Gate', CRIM)
    box(ax, 0.448, 0.44, 0.21, 0.052, r'Linear 64 -> 1280', None, BG3, INK, 7.8)
    box(ax, 0.448, 0.375, 0.21, 0.052, r'$g = \tanh(W_g e + b_g)$', None,
        '#FFFFFF', INK, 7.8)
    box(ax, 0.448, 0.29, 0.21, 0.065, r'$\gamma$  scalar,  init $= 0$',
        'model starts as pure CNN', BG3, CRIM, 7.8)
    ax.text(0.5525, 0.245, r'83,201 params', ha='center', fontsize=7.4,
            color=MUTE)
    arrow(ax, 0.400, 0.35, 0.445, 0.35)

    # ---- modulation
    box(ax, 0.435, 0.72, 0.235, 0.10, r'$\tilde{z} = z \odot (1 + \gamma g)$',
        'per-channel multiplicative gating', '#FFFFFF', INK, 9.0)
    arrow(ax, 0.402, 0.77, 0.432, 0.77)
    arrow(ax, 0.5525, 0.548, 0.5525, 0.715, rad=0.0)

    # ---- heads
    group(ax, 0.705, 0.155, 0.28, 0.70, 'Prediction heads', TEAL)
    box(ax, 0.718, 0.735, 0.255, 0.058, 'Dropout p = 0.3', None, '#FFFFFF',
        INK, 7.8)
    arrow(ax, 0.672, 0.77, 0.715, 0.77)

    # CORAL head: title inside the box, equations printed BELOW it
    box(ax, 0.718, 0.585, 0.255, 0.052, 'CORAL head (severity)',
        None, BG1, INK, 8.2)
    ax.text(0.8455, 0.556, r'$\eta_k = w^{\top}\tilde{z} + b_k$,   $k = 1..K\!-\!1$',
            ha='center', fontsize=7.4, color=INK)
    ax.text(0.8455, 0.529, 'shared $w$, separate biases',
            ha='center', fontsize=6.9, color=MUTE)
    ax.text(0.8455, 0.506, 'rank-consistent by construction',
            ha='center', fontsize=6.9, color=MUTE)

    box(ax, 0.718, 0.425, 0.255, 0.052, 'Binary head (infection)',
        None, BG1, INK, 8.2)
    ax.text(0.8455, 0.396, r'$\eta = w^{\top}\tilde{z} + b$', ha='center',
            fontsize=7.4, color=INK)

    box(ax, 0.718, 0.268, 0.255, 0.052, 'trainable parameters',
        None, BG4, LILAC, 8.0)
    ax.text(0.8455, 0.240, '86,915 ordinal / 86,914 binary',
            ha='center', fontsize=7.2, color=INK)
    ax.text(0.8455, 0.216, '1.62% of the full model', ha='center',
            fontsize=7.2, color=MUTE)

    ax.text(0.8455, 0.186, r'$\gamma$ read after training as a',
            ha='center', fontsize=7.0, color=CRIM)
    ax.text(0.8455, 0.167, 'diagnostic of tissue reliance', ha='center',
            fontsize=7.0, color=CRIM)

    arrow(ax, 0.8455, 0.730, 0.8455, 0.642)

    fig.savefig(OUT / 'fig_architecture.pdf', bbox_inches='tight',
                facecolor='white')
    fig.savefig(OUT / 'fig_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('wrote fig_architecture.pdf / .png')


if __name__ == '__main__':
    fig_pipeline()
    fig_architecture()
