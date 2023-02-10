from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Union, List
from nptyping import NDArray, Shape, Float, String


def _plotdefaults(COLS, ROWS, size=15) -> Tuple[plt.Figure, GridSpec]:
    φ: float = (1 + 5**0.5)/2
    cm: float = 2.54

    WIDTH: float = size / cm
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


def _single_figure(xlabel, ylabel) -> Tuple[plt.Figure, plt.Axes]:
    fig: plt.Figure
    gs: GridSpec
    ax: plt.Axes
    fig, gs = _plotdefaults(1, 1)
    ax = fig.add_subplot(gs[0, 0])
    ax.grid(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig, ax


def _dual_figure() -> Tuple[plt.Figure, plt.Axes]:
    fig, gs = _plotdefaults(2, 1)
    ax_left = fig.add_subplot(gs[0, 0])
    ax_right = fig.add_subplot(gs[1, 0])
    ax_left.grid(True, zorder=-10.0)
    axs = (ax_left, ax_right)
    return fig, axs


def _single_dual_axis_figure() -> Tuple[plt.Figure, plt.Axes]:
    fig, gs = _plotdefaults(1, 1)
    ax_left = fig.add_subplot(gs[0, 0])
    ax_left.grid(True, zorder=-10.0)
    ax_right = ax_left.twinx()
    axs = (ax_left, ax_right)
    return fig, axs


def single_plot(
        xs: NDArray[Shape["1, Dim"], Float],
        ys: NDArray[Shape["1, Dim"], Float],
        labels: NDArray[Shape["Dim"], String],
        x_label: str,
        y_label: str,
) -> Tuple[plt.Figure, plt.Axes]:
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = _single_figure(x_label, y_label)
    for x, y, label in zip(xs, ys, labels):
        ax.plot(x, y, label=label)
    return fig, ax


def single_plot_dual_axis():
    fig, ax = _single_figure(r'$r$ [Å]', r'G($r$) [-]')


def single_pdf(
        r: NDArray[Shape["1"], Float],
        gcalc: NDArray[Shape["1"], Float],
        gobs: NDArray[Shape["1"], Float],
        filepath: str
) -> Tuple[plt.Figure, plt.Axes]:
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = _single_figure(r'$r$ [Å]', r'G($r$) [-]')

    gdiff: NDArray[Shape["1"], Float] = gobs - gcalc
    span: float = max(gobs.max() - gobs.min(), gcalc.max() - gcalc.min()).max()
    baseline: float = min(gobs.min(), gcalc.min()) - span/10

    ax.scatter(r, gobs, 11, "0.0", lw=1.5)
    ax.scatter(r, gobs, 11, "1.0", lw=0)
    ax.scatter(r, gobs, 10, "C4", lw=0, label='obs', alpha=0.1)
    ax.plot(r, gcalc, '-', label='calc')
    ax.plot(r, gdiff + baseline, '-', label='diff', color='green')
    ax.set_xlim(r.min(), r.max())
    ax.legend()

    return fig, ax


def stacked_single_pdf(
        rs: List[List[Float]],
        gcalcs: List[List[Float]],
        gobss: List[List[Float]],
        names: List[str],
        filepath: str
) -> Tuple[plt.Figure, plt.Axes]:
    labels = {'calc': names, 'obs': 'obs', 'diff': 'diff'}

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = _single_figure(r'$r$ [Å]', r'G($r$) [-]')
    global_max = np.max([np.max(gobss), np.max(gcalcs)])
    global_min = np.min([np.min(gobss), np.min(gcalcs)])
    for i, (r, gcalc, gobs) in enumerate(zip(rs, gcalcs, gobss)):
        gdiff: NDArray[Shape["1"], Float] = gobs - gcalc
        span: float = max(gobs.max() - gobs.min(),
                          gcalc.max() - gcalc.min()).max()
        baseline: float = min(gobs.min(), gcalc.min()) - span/10
        shift = (global_max - global_min - baseline) * i
        ax.scatter(r, gobs + shift, 11, "0.0", lw=1.5)
        ax.scatter(r, gobs + shift, 11, "1.0", lw=0)
        ax.scatter(r, gobs + shift, 10, "C4", lw=0,
                   label=labels['obs'], alpha=0.1)
        ax.plot(r, gdiff + baseline + shift, '-',
                label=labels['diff'], color='green')
        ax.plot(r, gcalc + shift, '-', label=labels['calc'][i])
        labels = {k: None if type(v) != list else v for k, v in labels.items()}
    ax.set_xlim(r.min(), r.max())

    handles, labels = plt.gca().get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper right')

    return fig, ax
