#!/usr/bin/env python3
"""Build the multi-page PH Small-Boat Platform site from the Claude Design handoff.

Ports the single-page redesign (PH_Boat_Platform_Project_Pack.dc.html) onto the
existing multi-page structure: one page per section, shared stylesheet, cross-page
nav, prev/next, and a redesigned landing page. Section body markup is kept verbatim
from the design (inline styles) for pixel fidelity; only the page chrome is class-based.
Em-dashes are stripped everywhere (standing user preference).
"""
import re, os, html, sys

sys.path.insert(0, os.path.expanduser("~/ph-boat-platform"))
import refs  # shared reference list (labels + URLs)

SRC = os.path.expanduser("~/ph-boat-platform/design-source.dc.html")
OUT = os.path.expanduser("~/ph-boat-platform")
os.makedirs(OUT, exist_ok=True)

raw = open(SRC, encoding="utf-8").read()

# Never emit em-dashes: replace each (with surrounding spaces/tabs, not newlines) with " - ".
def desh(s):
    return re.sub(r"[ \t]*—[ \t]*", " - ", s)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">')

# --- pull the <main> inner content and split its top-level section/figure blocks ---
main_inner = re.search(r"<main\b[^>]*>(.*)</main>", raw, re.S).group(1)
main_inner = re.sub(r'\s*style-hover="[^"]*"', "", main_inner)  # design-tool attr -> real CSS hover
blocks = [m.group(0) for m in re.finditer(
    r"<section\b[^>]*>.*?</section>|<figure\b[^>]*>.*?</figure>", main_inner, re.S)]

def sec_id(block):
    m = re.match(r'<section\b[^>]*\bid="(s\d)"', block)
    return m.group(1) if m else None

# Group blocks: each id-section starts a page; unlabeled sections/figures attach to it.
page_blocks, current = {}, None
for b in blocks:
    i = sec_id(b)
    if i:
        current, page_blocks[i] = i, [b]
    else:
        page_blocks[current].append(b)

# (id, filename, nav label, card number, blurb)
PAGES = [
    ("s1", "problem.html",         "01 · Problem",         "01", "The market failure we picked and the alternatives we rejected."),
    ("s2", "research.html",        "02 · Research & Data", "02", "Every figure tagged sourced or estimated: market, supply, prices, competition, regulation, pain."),
    ("s3", "personas.html",        "03 · Personas",        "03", "Five actors - demand, supply, channel, gatekeeper - each mapped to an interview track."),
    ("s4", "interview-guide.html", "04 · Interview Guide", "04", "Four 20-minute tracks with objectives, questions, kill answers, and discriminators."),
    ("s5", "econ-concepts.html",   "05 · Econ Concepts",   "05", "Eight load-bearing course concepts, from lemons markets to repeated-game disintermediation."),
    ("s6", "business-model.html",  "06 · Business Model",  "06", "The hybrid model, revenue architecture, unit-economics sensitivity, and kill tests."),
    ("s7", "slides.html",          "07 · Slides",          "07", "Ten presentation slides, one claim each, with Q&A traps pre-answered."),
]

def h2_of(block):
    m = re.search(r"<h2\b[^>]*>(.*?)</h2>", block, re.S)
    return html.unescape(re.sub(r"<.*?>", "", m.group(1)).strip()) if m else ""

def nav(active):
    items = ['<a href="index.html"%s>Home</a>' % (' class="active"' if active == "index.html" else "")]
    for sid, fn, label, num, blurb in PAGES:
        cls = ' class="active"' if fn == active else ""
        items.append(f'<a href="{fn}"{cls}>{label}</a>')
    return '<nav class="toc">' + "".join(items) + "</nav>"

MASTHEAD = ('<header class="masthead"><div class="inner">'
            '<div class="kicker"><span class="rule"></span>'
            '<span>15.024 Applied Economics for Managers · Team Project Pack · July 2026</span></div>'
            '<h1><a href="index.html">Verified Small-Boat Transfers in the Philippines</a></h1>'
            '</div></header>')

def pagenav(idx):
    if idx > 0:
        p = PAGES[idx - 1]
        prev = f'<a class="pn prev" href="{p[1]}"><span>← Previous</span><b>{p[2]}</b></a>'
    else:
        prev = '<a class="pn prev" href="index.html"><span>← Back</span><b>Home</b></a>'
    if idx < len(PAGES) - 1:
        n = PAGES[idx + 1]
        nxt = f'<a class="pn next" href="{n[1]}"><span>Next →</span><b>{n[2]}</b></a>'
    else:
        nxt = '<a class="pn next" href="index.html"><span>Done →</span><b>Back to Home</b></a>'
    return f'<div class="pagenav">{prev}{nxt}</div>'

PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · PH Small-Boat Platform</title>
{fonts}
<link rel="stylesheet" href="style.css">
</head>
<body>
{masthead}
{nav}
<main>
{content}
{pagenav}
</main>
</body>
</html>
'''

def cite_markers(sid, content):
    """Insert superscript footnote markers after each configured anchor (first match)."""
    keys = refs.PAGE_REFS.get(sid) or []
    num = {k: i + 1 for i, k in enumerate(keys)}
    for csid, anchor, key in refs.CITES:
        if csid != sid or key not in num:
            continue
        pos = content.find(anchor)
        if pos == -1:
            continue
        end = pos + len(anchor)
        n = num[key]
        sup = (f'<sup style="font-size:.68em; line-height:0; font-weight:600;">'
               f'<a href="#{sid}-ref-{n}" style="text-decoration:none;">{n}</a></sup>')
        content = content[:end] + sup + content[end:]
    return content

def refs_block(sid):
    keys = refs.PAGE_REFS.get(sid)
    if not keys:
        return ""
    items = "".join(
        f'<li id="{sid}-ref-{i}" style="margin-bottom:6px; scroll-margin-top:72px;">'
        f'<a href="{refs.LUT[k][1]}" target="_blank" rel="noopener" '
        f'style="text-decoration:underline;">{html.escape(refs.LUT[k][0])}</a></li>'
        for i, k in enumerate(keys, 1))
    return (
        '<section style="margin-top:56px;">'
        '<h3 style="font-family:\'IBM Plex Mono\',monospace; font-size:12px; letter-spacing:.14em; '
        'text-transform:uppercase; color:#162A34; margin:0 0 14px; display:flex; align-items:center; gap:11px;">'
        '<span style="width:22px; height:2px; background:#C24A28;"></span>References &amp; sources</h3>'
        f'<ol style="margin:0; padding-left:22px; font-size:13.5px; line-height:1.5; color:#3A4A52;">{items}</ol>'
        '<p style="font-size:12px; color:#6D7A80; margin:10px 0 0; max-width:80ch;">Figures and charts on this '
        'page trace to these primary or reputable secondary sources. Items tagged ESTIMATED are derived and not '
        'directly citable.</p></section>')

for idx, (sid, fn, label, num, blurb) in enumerate(PAGES):
    content = cite_markers(sid, "\n".join(page_blocks[sid])) + "\n" + refs_block(sid)
    title = h2_of(page_blocks[sid][0]) or label
    page = PAGE.format(title=html.escape(title), fonts=FONTS, masthead=MASTHEAD,
                       nav=nav(fn), content=content, pagenav=pagenav(idx))
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(desh(page))
    print("wrote", fn)

# --- landing page: full design masthead + section cards ---
cards = []
for sid, fn, label, num, blurb in PAGES:
    h2 = h2_of(page_blocks[sid][0])
    cards.append(
        f'<a class="home-card" href="{fn}">'
        f'<div class="num">{num}</div>'
        f'<div class="lbl">Section {num}</div>'
        f'<div class="ttl">{html.escape(h2)}</div>'
        f'<p class="blurb">{html.escape(blurb)}</p>'
        f'<div class="go">Open section →</div></a>')

HOME_MASTHEAD = ('<header class="masthead home"><div class="inner">'
                 '<div class="kicker"><span class="rule"></span>'
                 '<span>15.024 Applied Economics for Managers · Team Project Pack · July 2026</span></div>'
                 '<h1>Verified Small-Boat Transfers in the Philippines:<br>'
                 '<em>a marketplace for the fleet the state cannot see</em></h1>'
                 '<div class="sub">Working hypothesis: a hybrid B2C marketplace for private bangka charters and '
                 'premium transfers in Northern Palawan, with hotels as affiliate distribution - built on the segment '
                 "MARINA's 2026 e-ticketing mandate explicitly exempts. Status: hypothesis to be tested in this week's "
                 'interviews, not a settled conclusion.</div>'
                 '</div></header>')

home = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Philippine Small-Boat Platform - 15.024 Project Pack</title>
{FONTS}
<link rel="stylesheet" href="style.css">
</head>
<body>
{HOME_MASTHEAD}
{nav("index.html")}
<div class="home-wrap">
  <div class="home-lead"><span class="rule"></span>Seven sections · each on its own page</div>
  <div class="home-grid">
    {"".join(cards)}
  </div>
  <div class="home-foot">A 15.024 Applied Economics for Managers team project pack. Navigate with the bar above or the cards. Status: working hypothesis to be tested in this week's interviews, not a settled conclusion.</div>
</div>
</body>
</html>
'''
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(desh(home))
print("wrote index.html")

# --- shared stylesheet (page chrome only; section bodies carry their own inline styles) ---
CSS = '''*{box-sizing:border-box;}
html,body{overflow-x:hidden;}
body{margin:0; background:#F5EFE4; color:#162A34; font-family:'Newsreader',Georgia,serif; font-size:17.5px; line-height:1.62; -webkit-font-smoothing:antialiased;}
a{color:#C24A28; text-decoration:none;}
a:hover{color:#B8862F;}
::selection{background:#C24A28; color:#F5EFE4;}

/* masthead */
header.masthead{position:relative; background-color:#0A1A24; color:#EFE6D3; padding:34px 7vw 28px; border-bottom:5px solid #B8862F; background-image:repeating-linear-gradient(0deg, rgba(184,134,47,.06) 0 1px, transparent 1px 46px), repeating-linear-gradient(90deg, rgba(184,134,47,.05) 0 1px, transparent 1px 46px); overflow:hidden;}
header.masthead.home{padding:64px 7vw 52px;}
header.masthead .inner{max-width:1080px; margin:0 auto; position:relative;}
header.masthead .kicker{display:flex; align-items:center; gap:14px; font-family:'IBM Plex Mono',monospace; font-size:11.5px; letter-spacing:.28em; text-transform:uppercase; color:#C9A24B; margin-bottom:16px;}
header.masthead.home .kicker{margin-bottom:26px;}
header.masthead .kicker .rule{width:34px; height:2px; background:#C24A28; display:inline-block; flex:none;}
header.masthead h1{font-family:'Libre Caslon Display',Georgia,serif; font-weight:400; font-size:clamp(22px,3vw,32px); line-height:1.12; margin:0; letter-spacing:-.01em;}
header.masthead.home h1{font-size:clamp(34px,5.2vw,60px); line-height:1.08; max-width:20ch;}
header.masthead h1 a{color:inherit;}
header.masthead h1 a:hover{color:#E6BE73;}
header.masthead h1 em{font-style:italic; color:#E6BE73;}
header.masthead .sub{margin-top:26px; color:#B9C6CE; font-size:16.5px; line-height:1.6; max-width:74ch; border-left:2px solid #2C4653; padding-left:20px;}

/* sticky cross-page nav */
nav.toc{position:sticky; top:0; z-index:50; background:#07141B; border-bottom:1px solid #21323B; display:flex; flex-wrap:wrap; justify-content:center; padding:0 4vw;}
nav.toc a{font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:#9FB0B8; padding:14px 15px; border-bottom:3px solid transparent;}
nav.toc a:hover{color:#FFFFFF; border-bottom-color:#C24A28;}
nav.toc a.active{color:#FFFFFF; border-bottom-color:#C24A28;}

/* main column (matches design) */
main{max-width:1080px; margin:0 auto; padding:0 32px 110px;}

/* reference list: highlight the item a footnote marker jumps to */
li:target{background:#F6E4D9; box-shadow:0 0 0 4px #F6E4D9;}
sup a{color:#C24A28;}

/* prev / next */
.pagenav{display:flex; justify-content:space-between; gap:14px; margin-top:72px; border-top:1px solid #D9CFBD; padding-top:22px; flex-wrap:wrap;}
.pn{display:flex; flex-direction:column; text-decoration:none; padding:14px 20px; background:#FFFFFF; border:1px solid #E4DBC9; min-width:220px; flex:1; transition:border-color .12s ease, transform .12s ease;}
.pn:hover{border-color:#C24A28; transform:translateY(-2px);}
.pn.next{text-align:right; align-items:flex-end;}
.pn span{font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:#6D7A80;}
.pn b{font-family:'Libre Caslon Display',serif; font-weight:400; font-size:18px; color:#162A34; margin-top:3px;}
@media(max-width:600px){.pn{min-width:100%;}}

/* landing */
.home-wrap{max-width:1080px; margin:0 auto; padding:56px 32px 110px;}
.home-lead{font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:#162A34; margin:0 0 22px; display:flex; align-items:center; gap:11px;}
.home-lead .rule{width:22px; height:2px; background:#C24A28;}
.home-grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:18px;}
.home-card{display:flex; flex-direction:column; background:#FFFFFF; border:1px solid #E4DBC9; border-top:3px solid #C24A28; padding:22px 24px; text-decoration:none; color:#162A34; transition:transform .12s ease, box-shadow .12s ease;}
.home-card:hover{transform:translateY(-3px); box-shadow:0 10px 26px rgba(10,26,36,.13);}
.home-card:nth-child(3n+2){border-top-color:#B8862F;}
.home-card:nth-child(3n){border-top-color:#2F6C7B;}
.home-card .num{font-family:'Libre Caslon Display',serif; font-size:44px; line-height:.85; color:#C24A28;}
.home-card .lbl{font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.16em; text-transform:uppercase; color:#6D7A80; margin-top:12px;}
.home-card .ttl{font-family:'Libre Caslon Display',serif; font-size:21px; color:#162A34; margin:5px 0 9px; line-height:1.15;}
.home-card .blurb{font-size:15px; color:#3A4A52; margin:0 0 18px; flex:1; line-height:1.5;}
.home-card .go{font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:#C24A28;}
.home-foot{font-size:13px; color:#6D7A80; line-height:1.55; border-top:1px solid #D9CFBD; margin-top:44px; padding-top:16px;}
'''
open(os.path.join(OUT, "style.css"), "w", encoding="utf-8").write(desh(CSS))
print("wrote style.css")
print("DONE ->", OUT)
'''
'''
