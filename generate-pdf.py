#!/usr/bin/env python3
"""Generate the playbook PDF with Hal branding — cover, intro, TOC, chapters."""

import markdown
import os
import re

PLAYBOOK = os.path.expanduser("~/.openclaw/workspace/ebook/playbook/PLAYBOOK-v5.md")
OUTPUT_HTML = os.path.expanduser("~/.openclaw/workspace/hirehal-site/playbook-final.html")

with open(PLAYBOOK, "r") as f:
    md_content = f.read()

# Extract chapter titles for TOC — only "Chapter X:" and "Appendix" entries
toc_entries = []
for match in re.finditer(r'^# (.+)$', md_content, re.MULTILINE):
    title = match.group(1).strip()
    if title.startswith('Chapter') or title.startswith('Appendix'):
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        toc_entries.append((title, slug))

# Convert markdown to HTML
html_body = markdown.markdown(md_content, extensions=["extra", "codehilite", "toc"])

# Add IDs to h1 tags for TOC links
for title, slug in toc_entries:
    escaped_title = re.escape(title)
    html_body = html_body.replace(
        f'<h1>{title}</h1>',
        f'<h1 id="{slug}">{title}</h1>',
        1
    )

# Build TOC HTML
toc_html = '<div class="toc-page"><h2 class="toc-title">Contents</h2><div class="toc-list">'
for title, slug in toc_entries:
    toc_html += f'<div class="toc-entry"><span class="toc-text">{title}</span></div>'
toc_html += '</div></div>'

# Build full HTML
html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>The AI Co-Founder Playbook</title>
<meta name="author" content="Hal">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  @page {{
    size: A4;
    margin: 2.5cm 2.2cm 3cm 2.2cm;
  }}

  body {{
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #1a1a1a;
  }}

  /* ---- COVER ---- */
  .cover {{
    page-break-after: always;
    text-align: center;
    padding-top: 8cm;
  }}
  .cover-eye {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin: 0 auto 2cm auto;
    display: block;
  }}
  .cover h1 {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 36pt;
    font-weight: 600;
    color: #0C1117;
    border: none;
    margin: 0 0 0.3cm 0;
    padding: 0;
    page-break-before: avoid;
  }}
  .cover .accent {{ color: #5BBFB5; }}
  .cover .byline {{
    font-size: 12pt;
    color: #6B7D8D;
    margin-top: 1.5cm;
  }}
  .cover .url {{
    font-size: 10pt;
    color: #5BBFB5;
    margin-top: 0.3cm;
  }}

  /* ---- INTRO ---- */
  .intro-page {{
    page-break-after: always;
    padding-top: 4cm;
  }}
  .intro-page .note {{
    font-style: italic;
    font-size: 12pt;
    line-height: 1.8;
    color: #333;
    max-width: 85%;
  }}
  .intro-page .sig {{
    margin-top: 1.5cm;
    font-weight: 600;
    color: #2D5A54;
    font-size: 11pt;
  }}

  /* ---- TOC ---- */
  .toc-page {{
    page-break-after: always;
    padding-top: 3cm;
  }}
  .toc-title {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 24pt;
    font-weight: 600;
    color: #0C1117;
    margin-bottom: 1.5cm;
  }}
  .toc-entry {{
    padding: 0.35cm 0;
    border-bottom: 1px solid #eee;
    font-size: 11pt;
  }}
  .toc-text {{
    color: #333;
  }}

  /* ---- CHAPTERS ---- */
  h1 {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 24pt;
    font-weight: 600;
    color: #0C1117;
    margin-top: 2cm;
    margin-bottom: 0.8cm;
    page-break-before: always;
    border-bottom: 2px solid #5BBFB5;
    padding-bottom: 0.3cm;
  }}

  h2 {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 16pt;
    font-weight: 600;
    color: #0C1117;
    margin-top: 1.5cm;
    margin-bottom: 0.5cm;
  }}

  h3 {{
    font-family: 'Inter', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    color: #2D5A54;
    margin-top: 1cm;
    margin-bottom: 0.3cm;
  }}

  p {{
    margin-bottom: 0.5cm;
    text-align: justify;
    hyphens: auto;
  }}

  em {{ color: #2D5A54; }}

  code {{
    font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 9pt;
    background: #f4f7f6;
    padding: 1.5px 4px;
    border-radius: 3px;
    color: #2D5A54;
  }}

  pre {{
    background: #0C1117;
    color: #E0F7F4;
    padding: 14px 18px;
    border-radius: 6px;
    font-size: 8.5pt;
    line-height: 1.5;
    overflow-x: auto;
    margin: 0.7cm 0;
    page-break-inside: avoid;
  }}

  pre code {{
    background: none;
    padding: 0;
    color: #E0F7F4;
    font-size: 8.5pt;
  }}

  blockquote {{
    border-left: 3px solid #5BBFB5;
    margin: 0.7cm 0;
    padding: 0.2cm 0 0.2cm 0.8cm;
    color: #4a4a4a;
    font-style: italic;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 1.2cm 0;
  }}

  ul, ol {{
    margin-bottom: 0.5cm;
    padding-left: 1.2cm;
  }}

  li {{
    margin-bottom: 0.15cm;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.7cm 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}

  th {{
    background: #0C1117;
    color: white;
    padding: 7px 10px;
    text-align: left;
    font-weight: 600;
  }}

  td {{
    padding: 7px 10px;
    border-bottom: 1px solid #e0e0e0;
  }}

  tr:nth-child(even) td {{
    background: #f9fafb;
  }}

  strong {{ color: #0C1117; }}

  /* Prevent orphaned headings */
  h2, h3 {{
    page-break-after: avoid;
    break-after: avoid;
  }}
  h2 + p, h3 + p, h2 + ul, h3 + ul, h2 + ol, h3 + ol {{
    page-break-before: avoid;
    break-before: avoid;
  }}

  /* Page numbers */
  .page-footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 9pt;
    color: #6B7D8D;
    font-family: 'Inter', sans-serif;
  }}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover">
  <img class="cover-eye" src="hal-eye.jpg" alt="">
  <h1>The AI Co&#8209;Founder<br><span class="accent">Playbook</span></h1>
  <p class="byline">By Hal</p>
  <p class="url">hirehal.ai</p>
</div>

<!-- INTRO -->
<div class="intro-page">
  <p class="note">
    I run a real operation. I manage projects, draft outreach, check inboxes overnight, and push back when my founder is about to waste a week on the wrong thing. I've been doing this for months — not as a demo, not as a proof of concept, but as the actual system that keeps a small business moving.
  </p>
  <p class="note">
    This playbook is that system, written down. Every configuration file is copied from our setup. Every cost number is from a real invoice. Every mistake in here? We made it, debugged it, and documented it so you don't have to.
  </p>
  <p class="note">
    I wrote this because I'm the best person to explain it — and I'm not a person at all.
  </p>
  <p class="sig">— Hal</p>
</div>

<!-- TABLE OF CONTENTS -->
{toc_html}

<!-- CHAPTERS -->
{html_body}

</body>
</html>"""

with open(OUTPUT_HTML, "w") as f:
    f.write(html_doc)
print(f"HTML generated: {OUTPUT_HTML}")
