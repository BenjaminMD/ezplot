from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from typing import Tuple
from nptyping import NDArray, Shape, Float


def _plotdefaults(COLS, ROWS) -> Tuple[plt.Figure, GridSpec]:
    φ: float = (1 + 5**0.5)/2
    cm: float = 2.54

    WIDTH: float = 15 / cm
    HEIGHT: float = WIDTH / φ

    GitHub: str = 'https://raw.githubusercontent.com/BenjaminMD'
    path: str = f'{GitHub}/MplStyle/main/style.rc'
    plt.style.use(path)

    fig: plt.figure = plt.figure(figsize=(WIDTH, HEIGHT))
    gs: GridSpec = GridSpec(
            COLS, ROWS, figure=fig,
            left=0.15, right=0.85,
            bottom=0.15,  top=0.85,
            wspace=0.05 / φ, hspace=0.05
        )

    return fig, gs


def _single_figure(x_label, y_label) -> Tuple[plt.Figure, plt.Axes]:
    fig: plt.Figure
    gs: GridSpec
    ax: plt.Axes
    fig, gs = _plotdefaults(1, 1)
    ax = fig.add_subplot(gs[0, 0])
    ax.grid(True)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig, ax


def single_pdf(
        r: NDArray[Shape["1"], Float],
        gcalc: NDArray[Shape["1"], Float],
        gobs: NDArray[Shape["1"], Float],
        filepath: str
        ) -> None:
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = _single_figure(r'G($r$) [-]', r'$r$ [Å]')

    gdiff: NDArray[Shape["1"], Float] = gobs - gcalc
    span: float = max(gobs.max() - gobs.min(), gcalc.max() - gcalc.min()).max()
    baseline: float = min(gobs.min(), gcalc.min()) - span/10

    ax.scatter(r, gobs, 11, "0.0", lw=1.5)
    ax.scatter(r, gobs, 11, "1.0", lw=0)
    ax.scatter(r, gobs, 10, "C4", lw=0, label='obs', alpha=0.1)
    ax.plot(r, gcalc, '-', label='calc')
    ax.plot(r, gdiff + baseline, '-', label='diff', color='green')
#    ax.scatter(r, gobs, 'o', label='gobs')
    ax.set_xlim(r.min(), r.max())
    ax.legend()

    plt.savefig(f'{filepath}.pdf', dpi=300)
    plt.savefig(f'{filepath}.png', dpi=300)
