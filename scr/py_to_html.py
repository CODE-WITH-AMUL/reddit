
import datetime

# ─────────────────────────────────────────────
# HTML  (fully self-contained with inline CSS)
# ─────────────────────────────────────────────
def _save_html(posts, folder, today_date):
    now_str = datetime.datetime.now().strftime("%B %d, %Y at %H:%M")
    total_upvotes = sum(u for _, _, u in posts if isinstance(u, int))
    max_upvotes   = max((u for _, _, u in posts if isinstance(u, int)), default=1)

    def upvote_color(u):
        if not isinstance(u, int): return "#888"
        if u >= 500: return "#16a34a"
        if u >= 100: return "#d97706"
        return "#64748b"

    def badge_bg(u):
        if not isinstance(u, int): return "#f1f5f9"
        if u >= 500: return "#dcfce7"
        if u >= 100: return "#fef9c3"
        return "#f1f5f9"

    rows_html = ""
    for i, (title, description, upvotes) in enumerate(posts, start=1):
        bar_pct = int((upvotes / max_upvotes) * 100) if isinstance(upvotes, int) and max_upvotes else 0
        color   = upvote_color(upvotes)
        bg      = badge_bg(upvotes)
        rows_html += f"""
        <tr class="{'row-even' if i % 2 == 0 else 'row-odd'}">
          <td style="text-align:center;color:#94a3b8;font-size:0.8rem;font-weight:600;">{i}</td>
          <td>
            <span style="font-weight:700;color:#0f172a;font-size:0.95rem;">{title}</span>
          </td>
          <td style="color:#475569;font-size:0.875rem;line-height:1.55;">{description}</td>
          <td style="text-align:center;">
            <span style="display:inline-block;padding:4px 12px;border-radius:999px;font-weight:700;
                         font-size:0.85rem;color:{color};background:{bg};letter-spacing:0.02em;">
              ▲ {upvotes:,}
            </span>
            <div style="margin-top:5px;height:4px;background:#e2e8f0;border-radius:2px;overflow:hidden;">
              <div style="width:{bar_pct}%;height:100%;background:{color};border-radius:2px;
                           transition:width 0.6s ease;"></div>
            </div>
          </td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Startup Ideas — {today_date}</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'DM Sans', sans-serif;
    background: #f8fafc;
    background-image:
      radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,102,241,0.12) 0%, transparent 70%);
    min-height: 100vh;
    padding: 48px 24px;
    color: #0f172a;
  }}

  .container {{
    max-width: 1060px;
    margin: 0 auto;
  }}

  /* ── Header ── */
  .header {{
    margin-bottom: 36px;
  }}
  .header-eyebrow {{
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 8px;
  }}
  .header h1 {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 5vw, 3rem);
    color: #0f172a;
    line-height: 1.1;
    margin-bottom: 10px;
  }}
  .header h1 span {{ color: #6366f1; }}
  .header-meta {{
    font-size: 0.875rem;
    color: #64748b;
  }}

  /* ── Stats strip ── */
  .stats {{
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
    flex-wrap: wrap;
  }}
  .stat-card {{
    flex: 1;
    min-width: 140px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }}
  .stat-label {{
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 6px;
  }}
  .stat-value {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #0f172a;
  }}
  .stat-value.accent {{ color: #6366f1; }}

  /* ── Table wrapper ── */
  .table-wrapper {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
  }}

  thead tr {{
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  }}
  thead th {{
    padding: 16px 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #c7d2fe;
    text-align: left;
  }}
  thead th:first-child {{ text-align: center; width: 48px; }}
  thead th:last-child  {{ width: 140px; text-align: center; }}

  tbody tr {{
    border-bottom: 1px solid #f1f5f9;
    transition: background 0.15s ease;
  }}
  tbody tr:last-child {{ border-bottom: none; }}
  tr.row-odd  {{ background: #ffffff; }}
  tr.row-even {{ background: #fafbff; }}
  tbody tr:hover {{ background: #eef2ff !important; }}

  tbody td {{
    padding: 16px 20px;
    vertical-align: top;
  }}
  tbody td:first-child {{ vertical-align: middle; }}

  /* ── Footer ── */
  .footer {{
    margin-top: 24px;
    text-align: center;
    font-size: 0.78rem;
    color: #94a3b8;
    letter-spacing: 0.03em;
  }}

  @media (max-width: 640px) {{
    thead th:nth-child(3), tbody td:nth-child(3) {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="header-eyebrow">Product Hunt Tracker</div>
    <h1> Startup <span>Ideas</span></h1>
    <p class="header-meta">Generated on {now_str} &nbsp;·&nbsp; {today_date}</p>
  </div>

  <div class="stats">
    <div class="stat-card">
      <div class="stat-label">Total Ideas</div>
      <div class="stat-value accent">{len(posts)}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Total Upvotes</div>
      <div class="stat-value">{total_upvotes:,}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Avg Upvotes</div>
      <div class="stat-value">{int(total_upvotes / len(posts)) if posts else 0:,}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Top Score</div>
      <div class="stat-value accent">{max_upvotes:,}</div>
    </div>
  </div>

  <div class="table-wrapper">
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Startup Name</th>
          <th>Description</th>
          <th style="text-align:center;">Upvotes</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>

  <div class="footer">
    {len(posts)} startups &nbsp;·&nbsp; {total_upvotes:,} total upvotes &nbsp;·&nbsp; auto-generated report
  </div>

</div>
</body>
</html>"""

    with open(f"{folder}/startup_ideas.html", "w", encoding="utf-8") as f:
        f.write(html)