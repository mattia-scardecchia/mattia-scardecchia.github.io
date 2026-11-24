"""4:3 homepage thumbnail of the paper's method: panel 1 of fig_setting (autoencoder fine-tuning with
the temporal objective and the past-frame decoder), redrawn alone on a 4:3 canvas.

Reuses fig_setting/make.py's drawing code unchanged. The figure is drawn in the paper's inch
coordinates, then the page is shrunk by SCALE, so text and lines (sized in points) come out SCALE
times larger relative to the drawing; the layout constants below make room for that. The output is
an SVG, so it stays sharp at any display size.

Usage, from the paper's conda environment:
    python tools/make_preprint_thumb.py <wm-repr paper>/iclr/figures images/pub-predictable-latents.svg 1.4
"""
import sys
from pathlib import Path

figures, out, scale = Path(sys.argv[1]), sys.argv[2], float(sys.argv[3])
sys.path[:0] = [str(figures / "fig_setting"), str(figures / "scripts")]
import make as m  # noqa: E402

m.ps.setup_style()

# Symbols (math labels, E, D) get a further 10% over the other text.
import matplotlib as mpl  # noqa: E402
BASE = mpl.rcParams["font.size"]
mpl.rcParams["font.size"] = BASE * 1.1

# Rows from the bottom up, in drawing inches: past-frame wire, frame labels, frame tiles (larger than
# the paper's, to fill the lower half), encoder/decoder, latents, objective box. No panel title.
m.ROUTE_Y, m.TILE_Y, m.T = 0.10, 0.42, 0.40
m.ENC_Y, m.ENC_H = 0.98, 0.26
m.LAT_Y, m.L = 1.40, 0.22
m.BOX_Y, m.BOX_H = 1.78, 0.28
m.LAT_C, m.ENC_C = m.LAT_Y + m.L / 2, m.ENC_Y + m.ENC_H / 2
m.H = m.BOX_Y + m.BOX_H + 0.14
m.W = m.H * 4 / 3             # 4:3; this width leaves the decoder clear of the "past frame" label

fig, ax = m.d.canvas(m.W, m.H)
k = m.Canvas(ax)
m.d.box(ax, 0.02, 0.02, m.W - 0.04, m.H - 0.04, color=m.PANEL, edge="none", rounding=0.07, zorder=0)

fr = m.frames()
a = 0.45                      # x_t
b = a + 0.90                  # x_{t+1}; the gap fits "temporal objective" on one line
r = m.W - 0.42                # reconstruction
for cx, img, lab, dx, seed, zlab in ((a, fr[3], r"$x_t$", -0.08, 0, r"$z_t$"), (b, fr[4], r"$x_{t+1}$", 0, 1, "")):
    top = k.frames(cx, [img], lab, label_dx=dx)
    k.coder(cx, "E")
    k.encode_up(cx, top, k.latents(cx, seed, label=zlab))
m.d.box(ax, a - m.T / 2 - 0.03, m.BOX_Y, b - a + m.T + 0.06, m.BOX_H, "temporal objective", color=m.ACCENT_FILL,
        edge=m.ACCENT, text_color=m.ACCENT, lw=0.9, rounding=0.05, fontsize=BASE)
k.action((a + b) / 2, r"$a_t$")
k.coder(r, "D")
k.wire([(b + m.L / 2, m.LAT_C), (r, m.LAT_C), (r, m.ENC_Y + m.ENC_H)])
pad = m.LABEL_GAP * 72 / mpl.rcParams["font.size"] / scale
ax.text(b + m.L / 2 + m.LABEL_GAP, m.LAT_C, r"$z_{t+1}$", ha="left", va="center", zorder=5,
        bbox=dict(boxstyle=f"square,pad={pad:.3f}", facecolor=m.PANEL, edgecolor="none"))
k.arrow((r, m.ENC_Y), (r, m.TILE_Y + m.T))
k.frames(r, [fr[4]], r"$\hat{x}_{t+1}$")
k.past_frame(a + 0.08, r - 0.36, r)

fig.set_size_inches(m.W / scale, m.H / scale)
fig.savefig(out, facecolor="white", bbox_inches=None, pad_inches=0)
print(f"drawing {m.W:.3f} x {m.H:.3f} in, page {m.W / scale:.3f} x {m.H / scale:.3f} in, ratio {m.W / m.H:.4f}")
