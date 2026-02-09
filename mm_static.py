import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def smooth_branch(ax, start, end, color="#333", lw=2.5, alpha=1.0):
  """Draw a smooth S-curve branch (horizontal-first bezier)."""
  x0, y0 = start
  x1, y1 = end
  mx = (x0 + x1) / 2
  verts = [(x0, y0), (mx, y0), (mx, y1), (x1, y1)]
  codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
  patch = patches.PathPatch(
    Path(verts, codes), fill=False, lw=lw,
    color=color, capstyle="round", alpha=alpha,
  )
  ax.add_patch(patch)


def tapered_branch(ax, start, end, color, lw_start=8, lw_end=3):
  """Draw a tapered S-curve branch using many line segments."""
  x0, y0 = start
  x1, y1 = end
  mx = (x0 + x1) / 2

  n = 40
  pts = []
  for i in range(n + 1):
    t = i / n
    u = 1 - t
    x = u**3 * x0 + 3 * u**2 * t * mx + 3 * u * t**2 * mx + t**3 * x1
    y = u**3 * y0 + 3 * u**2 * t * y0 + 3 * u * t**2 * y1 + t**3 * y1
    pts.append((x, y))

  for i in range(len(pts) - 1):
    frac = i / (len(pts) - 1)
    lw = lw_start + (lw_end - lw_start) * frac
    ax.plot(
      [pts[i][0], pts[i + 1][0]],
      [pts[i][1], pts[i + 1][1]],
      color=color, lw=lw, solid_capstyle="round",
    )


def draw_mindmap(outfile="mindmap.svg"):
  fig, ax = plt.subplots(figsize=(22, 12))
  ax.set_xlim(-2.2, 2.2)
  ax.set_ylim(-1.1, 1.1)
  ax.axis("off")
  fig.patch.set_facecolor("white")

  # Soft colors inspired by Coggle style
  C = {
    "Education":     "#5B9BD5",
    "Documentation": "#70AD47",
    "Feedback":      "#E07B7B",
    "Marketing":     "#ED7D31",
  }

  # Estimated title HALF-widths in data coords (generous to avoid overlap)
  HALF_W = {
    "Education":     0.22,
    "Documentation": 0.30,
    "Feedback":      0.20,
    "Marketing":     0.22,
  }

  # Center node
  bbox = dict(boxstyle="round,pad=0.35", fc="#E0E0E0", ec="#AAAAAA", lw=2)
  ax.text(
    0, 0, "Community", ha="center", va="center",
    fontsize=26, fontweight="bold", color="#333333",
    bbox=bbox, zorder=5,
  )

  # Approximate left/right edges of the center box
  CL = (-0.45, 0.0)
  CR = (0.45, 0.0)

  GAP = 0.05           # space between line end and text edge
  ITEM_OFFSET = 0.48   # items sit this far past the group-title outer edge
  ITEM_SPACING = 0.13  # vertical spacing between sibling items

  groups = [
    ("Education",     (-0.90,  0.35), ["Workshops", "Webinars", "Tutorials", "Tech Talks"],                      "left"),
    ("Documentation", ( 0.95,  0.35), ["API Guides", "Code Samples", "Knowledge Base"],                          "right"),
    ("Feedback",      (-0.90, -0.35), ["Surveys", "User Testing", "Feature Requests"],                           "left"),
    ("Marketing",     ( 0.95, -0.35), ["Content Creation", "Social Media", "Events & Meetups", "Newsletters"],   "right"),
  ]

  for title, (tx, ty), items, side in groups:
    color = C[title]
    hw = HALF_W[title]
    is_left = side == "left"
    n = len(items)

    # Text edges
    right_edge = tx + hw
    left_edge  = tx - hw

    if is_left:
      branch_arrival = (right_edge + GAP, ty)
      sub_departure  = (left_edge - GAP, ty)
      conn = CL
    else:
      branch_arrival = (left_edge - GAP, ty)
      sub_departure  = (right_edge + GAP, ty)
      conn = CR

    # Main branch (thick, tapered)
    tapered_branch(ax, conn, branch_arrival, color=color, lw_start=10, lw_end=5)

    # Group title
    ax.text(
      tx, ty, title, ha="center", va="center",
      fontsize=18, fontweight="bold", color=color, zorder=5,
    )

    # Sub-branches & leaf items
    y_start = ty + (n - 1) * ITEM_SPACING / 2

    for i, item in enumerate(items):
      iy = y_start - i * ITEM_SPACING

      if is_left:
        item_x = left_edge - ITEM_OFFSET
        item_end = (item_x + GAP, iy)
        item_ha = "right"
      else:
        item_x = right_edge + ITEM_OFFSET
        item_end = (item_x - GAP, iy)
        item_ha = "left"

      smooth_branch(ax, sub_departure, item_end, color=color, lw=2, alpha=0.7)

      ax.text(
        item_x, iy, item, ha=item_ha, va="center",
        fontsize=13, fontweight="bold", color=color,
      )

  plt.savefig(outfile, bbox_inches="tight", dpi=300, facecolor="white")
  plt.close(fig)


if __name__ == "__main__":
  draw_mindmap("community_mindmap.svg")
  draw_mindmap("community_mindmap.png")
