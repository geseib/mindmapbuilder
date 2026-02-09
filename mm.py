import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


# ── Color themes ──────────────────────────────────────────────────────

THEMES = {
  "classic": {
    "background":    "#FFFFFF",
    "center_bg":     "#E0E0E0",
    "center_border": "#AAAAAA",
    "center_text":   "#333333",
    "branches": ["#5B9BD5", "#70AD47", "#E07B7B", "#ED7D31"],
  },
  "midnight": {
    "background":    "#0E141C",
    "center_bg":     "#314B6E",
    "center_border": "#607EA2",
    "center_text":   "#BDB3A3",
    "branches": ["#607EA2", "#8197AC", "#BDB3A3", "#314B6E"],
  },
  "ember": {
    "background":    "#210100",
    "center_bg":     "#8C0902",
    "center_border": "#B14A36",
    "center_text":   "#FECE79",
    "branches": ["#E6A341", "#FECE79", "#B14A36", "#8C0902"],
  },
  "safari": {
    "background":    "#78614D",
    "center_bg":     "#ACCA92",
    "center_border": "#E0A752",
    "center_text":   "#78614D",
    "branches": ["#ACCA92", "#E0A752", "#D44720", "#C8B896"],
  },
}


# ── Configuration dictionary ──────────────────────────────────────────

MINDMAP = {
  "center": {
    "label": "Community",
    "url": "https://example.com/community",
  },
  "groups": [
    {
      "title": "Education",
      "url": "https://example.com/education",
      "position": (-0.90, 0.35),
      "side": "left",
      "half_width": 0.22,
      "items": [
        ("Workshops",  "https://example.com/workshops"),
        ("Webinars",   "https://example.com/webinars"),
        ("Tutorials",  "https://example.com/tutorials"),
        ("Tech Talks", "https://example.com/tech-talks"),
      ],
    },
    {
      "title": "Documentation",
      "url": "https://example.com/docs",
      "position": (0.95, 0.35),
      "side": "right",
      "half_width": 0.30,
      "items": [
        ("API Guides",      "https://example.com/api-guides"),
        ("Code Samples",    "https://example.com/code-samples"),
        ("Knowledge Base",  "https://example.com/knowledge-base"),
      ],
    },
    {
      "title": "Feedback",
      "url": "https://example.com/feedback",
      "position": (-0.90, -0.35),
      "side": "left",
      "half_width": 0.20,
      "items": [
        ("Surveys",          "https://example.com/surveys"),
        ("User Testing",     "https://example.com/user-testing"),
        ("Feature Requests", "https://example.com/feature-requests"),
      ],
    },
    {
      "title": "Marketing",
      "url": "https://example.com/marketing",
      "position": (0.95, -0.35),
      "side": "right",
      "half_width": 0.22,
      "items": [
        ("Content Creation",  "https://example.com/content-creation"),
        ("Social Media",      "https://example.com/social-media"),
        ("Events & Meetups",  "https://example.com/events"),
        ("Newsletters",       "https://example.com/newsletters"),
      ],
    },
  ],
}


# ── Branch drawing helpers ────────────────────────────────────────────

# -- Organic (swooping curves) -----------------------------------------

def smooth_branch(ax, start, end, color="#333", lw=2.5, alpha=1.0):
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


# -- Angular (90-degree right-angle lines) -----------------------------

def ortho_branch(ax, start, end, color="#333", lw=2.5, alpha=1.0):
  x0, y0 = start
  x1, y1 = end
  mx = (x0 + x1) / 2
  ax.plot(
    [x0, mx, mx, x1], [y0, y0, y1, y1],
    color=color, lw=lw, solid_capstyle="butt", alpha=alpha,
  )


def ortho_tapered_branch(ax, start, end, color, lw_start=8, lw_end=3):
  x0, y0 = start
  x1, y1 = end
  mx = (x0 + x1) / 2
  n = 40
  total_len = abs(mx - x0) + abs(y1 - y0) + abs(x1 - mx)
  if total_len == 0:
    return
  pts = []
  for i in range(n + 1):
    d = (i / n) * total_len
    seg1 = abs(mx - x0)
    seg2 = abs(y1 - y0)
    if d <= seg1:
      frac = d / seg1 if seg1 else 0
      pts.append((x0 + (mx - x0) * frac, y0))
    elif d <= seg1 + seg2:
      frac = (d - seg1) / seg2 if seg2 else 0
      pts.append((mx, y0 + (y1 - y0) * frac))
    else:
      frac = (d - seg1 - seg2) / abs(x1 - mx) if abs(x1 - mx) else 0
      pts.append((mx + (x1 - mx) * frac, y1))
  for i in range(len(pts) - 1):
    frac = i / (len(pts) - 1)
    lw = lw_start + (lw_end - lw_start) * frac
    ax.plot(
      [pts[i][0], pts[i + 1][0]],
      [pts[i][1], pts[i + 1][1]],
      color=color, lw=lw, solid_capstyle="butt",
    )


# ── Style presets ─────────────────────────────────────────────────────

STYLES = {
  "organic": {
    "main_branch": tapered_branch,
    "sub_branch": smooth_branch,
  },
  "angular": {
    "main_branch": ortho_tapered_branch,
    "sub_branch": ortho_branch,
  },
}


# ── Horizontal layout (current) ──────────────────────────────────────

def _draw_horizontal(config, outfile, style, t):
  draw_main = STYLES[style]["main_branch"]
  draw_sub = STYLES[style]["sub_branch"]
  bg = t["background"]
  branch_colors = t["branches"]

  fig, ax = plt.subplots(figsize=(22, 12))
  ax.set_xlim(-2.2, 2.2)
  ax.set_ylim(-1.1, 1.1)
  ax.axis("off")
  fig.patch.set_facecolor(bg)

  GAP = 0.05
  ITEM_OFFSET = 0.48
  ITEM_SPACING = 0.13

  center = config["center"]
  bbox = dict(boxstyle="round,pad=0.35", fc=t["center_bg"],
              ec=t["center_border"], lw=2)
  ax.text(0, 0, center["label"], ha="center", va="center",
          fontsize=26, fontweight="bold", color=t["center_text"],
          bbox=bbox, zorder=5, url=center.get("url", ""))

  CENTER_X_L = -0.45
  CENTER_X_R =  0.45
  CONN_GAP   =  0.03

  for idx, group in enumerate(config["groups"]):
    title = group["title"]
    color = branch_colors[idx % len(branch_colors)]
    tx, ty = group["position"]
    hw = group["half_width"]
    items = group["items"]
    is_left = group["side"] == "left"
    n = len(items)

    v_offset = CONN_GAP if ty > 0 else -CONN_GAP
    right_edge = tx + hw
    left_edge = tx - hw

    if is_left:
      branch_arrival = (right_edge + GAP, ty)
      sub_departure = (left_edge - GAP, ty)
      conn = (CENTER_X_L, v_offset)
    else:
      branch_arrival = (left_edge - GAP, ty)
      sub_departure = (right_edge + GAP, ty)
      conn = (CENTER_X_R, v_offset)

    draw_main(ax, conn, branch_arrival, color=color, lw_start=10, lw_end=5)

    ax.text(tx, ty, title, ha="center", va="center",
            fontsize=18, fontweight="bold", color=color, zorder=5,
            url=group.get("url", ""))

    y_start = ty + (n - 1) * ITEM_SPACING / 2
    for i, (label, url) in enumerate(items):
      iy = y_start - i * ITEM_SPACING
      if is_left:
        item_x = left_edge - ITEM_OFFSET
        item_end = (item_x + GAP, iy)
        item_ha = "right"
      else:
        item_x = right_edge + ITEM_OFFSET
        item_end = (item_x - GAP, iy)
        item_ha = "left"
      draw_sub(ax, sub_departure, item_end, color=color, lw=2, alpha=0.7)
      ax.text(item_x, iy, label, ha=item_ha, va="center",
              fontsize=13, fontweight="bold", color=color, url=url)

  plt.savefig(outfile, bbox_inches="tight", dpi=300, facecolor=bg)
  plt.close(fig)


# ── Vertical / hybrid layout ─────────────────────────────────────────
#
#                         Documentation   (branch from center)
#                         |
#                         |- API Guides   (items nest under group)
#   center --- branch --- |- Code Samples
#                         |
#                         Marketing
#                         |
#                         |- Content Creation

def _draw_vertical(config, outfile, style, t):
  draw_main = STYLES[style]["main_branch"]
  bg = t["background"]
  branch_colors = t["branches"]

  ITEM_SPACING = 0.18    # vertical distance between rows
  BLOCK_GAP = 0.30       # extra gap between group blocks
  ITEM_TICK = 0.12       # horizontal tick for item L-shape
  TEXT_GAP = 0.04
  SPINE_DROP = 0.06      # sub-spine starts this far below group title
  MIN_CENTER_GAP = 0.35  # min distance from center to any group title
  CONN_GAP = 0.03        # vertical offset so branches don't overlap at center

  X_GROUP_R = 0.65       # x anchor for right-side groups
  X_GROUP_L = -0.65      # x anchor for left-side groups

  groups = config["groups"]
  left_groups = [(i, g) for i, g in enumerate(groups) if g["side"] == "left"]
  right_groups = [(i, g) for i, g in enumerate(groups) if g["side"] == "right"]

  # Layout upper groups (above center): title high, items descend toward center.
  # Lowest item y will be exactly MIN_CENTER_GAP above center (y=0).
  def layout_upper(side_groups):
    total_h = 0.0
    for gi, (idx, group) in enumerate(side_groups):
      total_h += len(group["items"]) * ITEM_SPACING
      if gi > 0:
        total_h += BLOCK_GAP
    blocks = []
    y = MIN_CENTER_GAP + total_h
    for gi, (idx, group) in enumerate(side_groups):
      color = branch_colors[idx % len(branch_colors)]
      if gi > 0:
        y -= BLOCK_GAP
      group_y = y
      items = []
      for label, url in group["items"]:
        y -= ITEM_SPACING
        items.append((y, label, url))
      blocks.append((group_y, group["title"], group.get("url", ""), color, items))
    return blocks

  # Layout lower groups (below center): title starts at -MIN_CENTER_GAP, items descend.
  def layout_lower(side_groups):
    blocks = []
    y = -MIN_CENTER_GAP
    for gi, (idx, group) in enumerate(side_groups):
      color = branch_colors[idx % len(branch_colors)]
      if gi > 0:
        y -= BLOCK_GAP
      group_y = y
      items = []
      for label, url in group["items"]:
        y -= ITEM_SPACING
        items.append((y, label, url))
      blocks.append((group_y, group["title"], group.get("url", ""), color, items))
    return blocks

  def split_and_layout(side_groups):
    n = len(side_groups)
    mid = (n + 1) // 2   # first half above center, rest below
    upper = layout_upper(side_groups[:mid])
    lower = layout_lower(side_groups[mid:])
    return upper + lower

  left_blocks = split_and_layout(left_groups)
  right_blocks = split_and_layout(right_groups)

  center_y = 0.0  # fixed — groups are laid out symmetrically around it

  all_ys = []
  for block in left_blocks + right_blocks:
    all_ys.append(block[0])
    for iy, _, _ in block[4]:
      all_ys.append(iy)
  if not all_ys:
    return

  # Figure — portrait orientation
  margin_top, margin_bot = 0.6, 0.5
  y_hi = max(all_ys) + margin_top
  y_lo = min(all_ys) - margin_bot
  fig_h = max(10, (y_hi - y_lo) * 3.5)
  fig, ax = plt.subplots(figsize=(12, fig_h))
  ax.set_xlim(-1.5, 1.5)
  ax.set_ylim(y_lo, y_hi)
  ax.axis("off")
  fig.patch.set_facecolor(bg)

  # Center node
  center = config["center"]
  bbox_props = dict(boxstyle="round,pad=0.35", fc=t["center_bg"],
                    ec=t["center_border"], lw=2)
  ax.text(0, center_y, center["label"], ha="center", va="center",
          fontsize=24, fontweight="bold", color=t["center_text"],
          bbox=bbox_props, zorder=5, url=center.get("url", ""))

  CENTER_HALF_W = 0.38

  def draw_side(blocks, x_group, is_left):
    for group_y, title, url, color, items in blocks:
      # Vertical offset so upper/lower branches don't overlap at center
      v_offset = CONN_GAP if group_y > 0 else -CONN_GAP
      # Tapered branch from center to group title
      if is_left:
        conn_start = (-CENTER_HALF_W, v_offset)
        conn_end = (x_group + TEXT_GAP, group_y)
      else:
        conn_start = (CENTER_HALF_W, v_offset)
        conn_end = (x_group - TEXT_GAP, group_y)
      draw_main(ax, conn_start, conn_end, color=color, lw_start=8, lw_end=4)

      # Group title
      title_ha = "right" if is_left else "left"
      ax.text(x_group, group_y, title, ha=title_ha, va="center",
              fontsize=16, fontweight="bold", color=color, zorder=5, url=url)

      if not items:
        continue

      # Sub-spine: vertical line from just below group title to last item
      last_item_y = items[-1][0]
      ax.plot([x_group, x_group], [group_y - SPINE_DROP, last_item_y],
              color=color, lw=2, alpha=0.5)

      # Items with L-shape ticks
      for item_y, label, item_url in items:
        if is_left:
          ax.plot([x_group - ITEM_TICK, x_group], [item_y, item_y],
                  color=color, lw=2, alpha=0.7)
          ax.text(x_group - ITEM_TICK - TEXT_GAP, item_y, label,
                  ha="right", va="center",
                  fontsize=13, fontweight="bold", color=color, url=item_url)
        else:
          ax.plot([x_group, x_group + ITEM_TICK], [item_y, item_y],
                  color=color, lw=2, alpha=0.7)
          ax.text(x_group + ITEM_TICK + TEXT_GAP, item_y, label,
                  ha="left", va="center",
                  fontsize=13, fontweight="bold", color=color, url=item_url)

  draw_side(left_blocks, X_GROUP_L, is_left=True)
  draw_side(right_blocks, X_GROUP_R, is_left=False)

  plt.savefig(outfile, bbox_inches="tight", dpi=300, facecolor=bg)
  plt.close(fig)


# ── Main entry point ──────────────────────────────────────────────────

def draw_mindmap(config=None, outfile="mindmap.svg", style="organic",
                 theme="classic", layout="horizontal"):
  """
  Generate a mindmap from *config* dict.

  style:  "organic" | "angular"
  theme:  "classic" | "midnight" | custom dict
  layout: "horizontal" | "vertical"
  """
  if config is None:
    config = MINDMAP
  t = THEMES[theme] if isinstance(theme, str) else theme

  if layout == "vertical":
    _draw_vertical(config, outfile, style, t)
  else:
    _draw_horizontal(config, outfile, style, t)

  if outfile.endswith(".svg"):
    _inject_svg_link_styles(outfile)


def _inject_svg_link_styles(svg_path):
  style_block = (
    '<style type="text/css">\n'
    '  a { cursor: pointer; text-decoration: underline; }\n'
    '  a:hover g { opacity: 0.6; }\n'
    '</style>\n'
  )
  with open(svg_path, "r") as f:
    svg = f.read()
  svg = svg.replace("</metadata>", "</metadata>\n" + style_block, 1)
  svg = svg.replace('xlink:href="http', 'target="_blank" xlink:href="http')
  with open(svg_path, "w") as f:
    f.write(svg)


if __name__ == "__main__":
  for theme_name in THEMES:
    for style_name in STYLES:
      for layout_name in ("horizontal", "vertical"):
        base = f"community_mindmap_{theme_name}_{style_name}_{layout_name}"
        draw_mindmap(MINDMAP, f"{base}.svg", style=style_name,
                     theme=theme_name, layout=layout_name)
        draw_mindmap(MINDMAP, f"{base}.png", style=style_name,
                     theme=theme_name, layout=layout_name)
