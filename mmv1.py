import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def curve(ax, p0, p1, bend=0.2, lw=2):
    # Simple quadratic-ish bezier using two control points
    x0, y0 = p0
    x1, y1 = p1
    cx1, cy1 = x0 + (x1 - x0) * 0.35, y0 + (y1 - y0) * 0.35 + bend
    cx2, cy2 = x0 + (x1 - x0) * 0.70, y0 + (y1 - y0) * 0.70 + bend
    verts = [(x0, y0), (cx1, cy1), (cx2, cy2), (x1, y1)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    ax.add_patch(patches.PathPatch(Path(verts, codes), fill=False, lw=lw, color="black"))

def draw_mindmap(outfile="mindmap.svg"):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.8, 0.8)
    ax.axis("off")

    # Colors per group
    C = {
        "Education": "#1f5fbf",
        "Documentation": "#2e8b57",
        "Feedback": "#b22222",
        "Marketing": "#d97706",
    }

    center = (0.0, 0.0)
    ax.text(*center, "Community", ha="center", va="center",
            fontsize=44, fontweight="bold", color="black")

    groups = [
        ("Education", (-0.55,  0.25), ["Workshops", "Webinars", "Tutorials", "Tech Talks"], +0.10),
        ("Documentation", (0.55,  0.28), ["API Guides", "Code Samples", "Knowledge Base"], -0.05),
        ("Feedback", (-0.60, -0.30), ["Surveys", "User Testing", "Feature Requests"], -0.10),
        ("Marketing", (0.60, -0.28), ["Content Creation", "Social Media", "Events & Meetups", "Newsletters"], +0.08),
    ]

    # Main branches from center to group title
    for title, gpos, items, bend in groups:
        curve(ax, center, gpos, bend=bend, lw=2.2)
        ax.text(*gpos, title, ha="center", va="center",
                fontsize=22, fontweight="bold", color=C[title])

        # Items fanning out from group title
        # Place items vertically with slight horizontal offset
        x, y = gpos
        is_left = x < 0
        dx = -0.32 if is_left else 0.32
        start_y = y + 0.22
        step = 0.12
        for i, item in enumerate(items):
            ipos = (x + dx, start_y - i * step)
            # item branch (thin and slightly curved)
            curve(ax, gpos, ipos, bend=(0.06 if is_left else -0.06), lw=1.6)
            ax.text(*ipos, item,
                    ha=("right" if is_left else "left"), va="center",
                    fontsize=18, fontweight="bold", color=C[title])

    plt.savefig(outfile, bbox_inches="tight", dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    draw_mindmap("community_mindmap.svg")   # crisp for slides
    draw_mindmap("community_mindmap.png")   # convenient image
