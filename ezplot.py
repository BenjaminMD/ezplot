from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt


def PlotDefaults(COLS, ROWS):
    φ = (1 + 5**0.5)/2
    cm = 2.54

    WIDTH = 15 / cm
    HEIGHT = WIDTH / φ

    GitHub = 'https://raw.githubusercontent.com/BenjaminMD'
    path = f'{GitHub}/MplStyle/main/style.rc'
    plt.style.use(path)

    fig = plt.figure(figsize=(WIDTH, HEIGHT))
    gs = GridSpec(
            COLS, ROWS, figure=fig,
            left=0.15, right=0.85,
            bottom=0.15,  top=0.85,
            wspace=0.05 / φ, hspace=0.05
        )

    return fig, gs


def SingleFigure(x_label, y_label):
    fig, gs = PlotDefaults(1, 1)
    ax = fig.add_subplot(gs[0, 0])
    ax.grid(True)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig, ax


def SinglePDF(r, gcalc, gobs, filepath):
    fig, ax = SingleFigure(r'G($r$) [-]', r'$r$ [Å]')

    gdiff = gobs - gcalc
    span = max(gobs.max() - gobs.min(), gcalc.max() - gcalc.min()).max()
    baseline = min(gobs.min(), gcalc.min()) - span/10

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
