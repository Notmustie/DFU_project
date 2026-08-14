"""
Regenerate fig2_control and fig3_gate with the corrected statistics from
the live In[13] run. The old versions were rendered from a superseded
results_infection.json and disagree with the current text.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path('figures'); OUT.mkdir(exist_ok=True)
INK, MUTE, TEAL, CRIM, GREEN = '#14313D', '#5B7683', '#2E7D8F', '#BE123C', '#15803D'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'axes.spines.top': False, 'axes.spines.right': False})


# ---------------------------------------------------------------------
# FIG 2 — control comparison, with the corrected AUROC and its CI
# ---------------------------------------------------------------------
def fig_control():
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    names = ['derived colour labels\n(severity, QWK)',
             'expert clinician labels\n(infection, AUROC)']
    vals = [0.2492, 0.8101]
    err = [[0, 0.8101 - 0.7971], [0, 0.8288 - 0.8101]]   # asymmetric CI

    bars = ax.bar(names, vals, color=[CRIM, TEAL], width=0.5,
                  yerr=err, capsize=6, error_kw=dict(ecolor=INK, lw=1.2))
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.055, f'{v:.3f}',
                ha='center', fontsize=13, fontweight='bold', color=INK)
    ax.text(1.30, 0.8101, '95% CI', ha='left', va='center', fontsize=7.5,
            color=MUTE)

    ax.set_ylim(0, 1.0)
    ax.set_ylabel('score from pixels alone', fontsize=9, color=MUTE)
    ax.set_title('Identical pipeline. Only the label source differs.',
                 fontsize=12, fontweight='bold', color=INK, loc='left')
    ax.text(0, -0.24,
            'Same architectures, preprocessing, grouped folds and code.\n'
            'The gap isolates label provenance, not model capacity.',
            transform=ax.transAxes, fontsize=8.5, color=MUTE, va='top')
    fig.tight_layout()
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'fig2_control.{ext}', dpi=300,
                    bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('wrote fig2_control (AUROC 0.8101, CI 0.797-0.829)')


# ---------------------------------------------------------------------
# FIG 3 — the gate, shown as a distribution rather than per-fold bars
# ---------------------------------------------------------------------
# The per-fold gamma values from the current run were not available, only
# their mean (-0.060), standard deviation (0.928) and the test against
# zero (p = 0.90). Rather than plot five bars from stale numbers, the
# figure now shows what is actually established: an estimate whose
# confidence interval straddles zero by a wide margin.
def fig_gate():
    mean, sd, n, p = -0.060, 0.928, 5, 0.9033
    se = sd / np.sqrt(n)
    ci = 2.776 * se        # t(0.975, df=4)

    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.axvline(0, color=INK, lw=1.4, zorder=1)
    ax.axhspan(-0.35, 0.35, xmin=0, xmax=1, color='#F3F6F7', zorder=0)

    ax.errorbar([mean], [0], xerr=[[ci], [ci]], fmt='o', color=TEAL,
                markersize=11, capsize=8, lw=2, zorder=3)
    ax.text(mean, 0.16, f'mean {mean:+.3f}', ha='center', fontsize=10,
            fontweight='bold', color=INK)
    ax.text(mean, -0.22, f'95% CI  [{mean-ci:+.2f}, {mean+ci:+.2f}]',
            ha='center', fontsize=8.5, color=MUTE)

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-0.45, 0.45)
    ax.set_yticks([])
    ax.set_xlabel(r'learned gate scalar $\gamma$', fontsize=9.5, color=MUTE)
    ax.spines['left'].set_visible(False)
    ax.set_title('The gate did not converge on a use of tissue',
                 fontsize=12, fontweight='bold', color=INK, loc='left')
    ax.text(0, -0.30,
            r'$\gamma$ is initialised at 0 and free to grow. Across five folds it has'
            f'\nstandard deviation {sd:.2f} against a mean of {mean:+.2f}, '
            f'and is not\ndistinguishable from zero (p = {p:.2f}).',
            transform=ax.transAxes, fontsize=8.5, color=CRIM, va='top')
    fig.tight_layout()
    for ext in ('pdf', 'png'):
        fig.savefig(OUT / f'fig3_gate.{ext}', dpi=300,
                    bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'wrote fig3_gate (mean {mean:+.3f}, sd {sd}, p {p})')


if __name__ == '__main__':
    fig_control()
    fig_gate()
