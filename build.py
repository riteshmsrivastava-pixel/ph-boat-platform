#!/usr/bin/env python3
import re, os, html

SRC = os.path.expanduser("~/Downloads/PH_Boat_Platform_Project_Pack_1.html")
OUT = os.path.expanduser("~/ph-boat-platform")
os.makedirs(OUT, exist_ok=True)

src = open(SRC, encoding="utf-8").read()

# --- extract the main <style> block from <head> ---
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)

# --- extract masthead ---
masthead = re.search(r"<header class=\"masthead\">.*?</header>", src, re.S).group(0)

# --- extract each <section id="sN">...</section> ---
sections = re.findall(r"<section id=\"(s\d)\">(.*?)</section>", src, re.S)
sec_map = {sid: body for sid, body in sections}

# Page metadata: (source id, filename, short nav label, long home-card blurb)
PAGES = [
    ("s1", "problem.html",         "1 · Problem",           "The market failure we picked and the alternatives we rejected."),
    ("s2", "research.html",        "2 · Research & Data",   "Every figure tagged sourced or estimated: market, supply, prices, competition, regulation, pain."),
    ("s3", "personas.html",        "3 · Personas",          "Five actors — demand, supply, channel, gatekeeper — each mapped to an interview track."),
    ("s4", "interview-guide.html", "4 · Interview Guide",   "Four 20-minute tracks with objectives, questions, kill answers, and discriminators."),
    ("s5", "econ-concepts.html",   "5 · Econ Concepts",     "Eight load-bearing course concepts, from lemons markets to repeated-game disintermediation."),
    ("s6", "business-model.html",  "6 · Business Model",    "The hybrid model, revenue architecture, unit-economics sensitivity, and kill tests."),
    ("s7", "slides.html",          "7 · Slides",            "Ten presentation slides, one claim each, with Q&A traps pre-answered."),
]

def nav_html(active_file):
    links = ['<a href="index.html"%s>Home</a>' % (' class="active"' if active_file=="index.html" else "")]
    for sid, fn, label, _ in PAGES:
        cls = ' class="active"' if fn == active_file else ""
        links.append(f'<a href="{fn}"{cls}>{label}</a>')
    return '<nav class="toc">\n  ' + "\n  ".join(links) + "\n</nav>"

# smaller masthead for interior pages (keep full one only on home)
def compact_masthead(title_label):
    return f'''<header class="masthead compact">
  <div class="kicker">15.024 Applied Economics for Managers · Team Project Pack · July 2026</div>
  <h1><a href="index.html" class="home-link">Verified Small-Boat Transfers in the Philippines</a></h1>
</header>'''

PAGE_TMPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · PH Small-Boat Platform</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{masthead}
{nav}
<main>
<section id="{sid}">
{body}
</section>
{pagenav}
</main>
</body>
</html>
'''

def pagenav(idx):
    prev_link = ""
    next_link = ""
    if idx > 0:
        p = PAGES[idx-1]
        prev_link = f'<a class="pn prev" href="{p[1]}"><span>← Previous</span><b>{p[2]}</b></a>'
    else:
        prev_link = f'<a class="pn prev" href="index.html"><span>← Back</span><b>Home</b></a>'
    if idx < len(PAGES)-1:
        n = PAGES[idx+1]
        next_link = f'<a class="pn next" href="{n[1]}"><span>Next →</span><b>{n[2]}</b></a>'
    else:
        next_link = f'<a class="pn next" href="index.html"><span>Done →</span><b>Back to Home</b></a>'
    return f'<div class="pagenav">{prev_link}{next_link}</div>'

# --- write interior pages ---
for idx, (sid, fn, label, blurb) in enumerate(PAGES):
    body = sec_map[sid].strip()
    # h2 title from body
    m = re.search(r"<h2>(.*?)</h2>", body, re.S)
    title = html.unescape(re.sub(r"<.*?>", "", m.group(1)).strip()) if m else label
    page = PAGE_TMPL.format(
        title=html.escape(title),
        masthead=compact_masthead(label),
        nav=nav_html(fn),
        sid=sid,
        body=body,
        pagenav=pagenav(idx),
    )
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(page)
    print("wrote", fn)

# --- home page ---
cards = []
for sid, fn, label, blurb in PAGES:
    body = sec_map[sid]
    m = re.search(r"<h2>(.*?)</h2>", body, re.S)
    h2 = html.unescape(re.sub(r"<.*?>", "", m.group(1)).strip()) if m else label
    num = label.split(" · ")[0]
    name = label.split(" · ")[1]
    cards.append(f'''  <a class="home-card" href="{fn}">
    <div class="hc-num">Section {num}</div>
    <div class="hc-title">{html.escape(h2)}</div>
    <p class="hc-blurb">{html.escape(blurb)}</p>
    <div class="hc-go">Open section →</div>
  </a>''')

home = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Philippine Small-Boat Platform — 15.024 Project Pack</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{masthead}
{nav_html("index.html")}
<main>
  <div class="home-grid">
{chr(10).join(cards)}
  </div>
  <div class="footnote" style="margin-top:56px">
    A 15.024 Applied Economics for Managers team project pack. Each section is its own page — use the navigation bar or the cards above. Status: working hypothesis to be tested in this week's interviews, not a settled conclusion.
  </div>
</main>
</body>
</html>
'''
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(home)
print("wrote index.html")

# --- extra CSS appended to shared stylesheet ---
extra_css = '''

/* ---- multi-page additions ---- */
header.masthead.compact{padding:26px 6vw 22px;}
header.masthead.compact h1{font-size:clamp(20px,2.4vw,26px);}
.home-link,.home-link:visited{color:inherit;text-decoration:none;}
.home-link:hover{color:#E8C97F;}
nav.toc a.active{color:#fff;border-bottom-color:var(--rust);}

.home-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;margin-top:48px;}
.home-card{display:flex;flex-direction:column;background:var(--paper);border:1px solid var(--line);border-top:4px solid var(--navy);padding:20px 22px;text-decoration:none;color:var(--ink);transition:transform .12s ease,box-shadow .12s ease,border-color .12s ease;}
.home-card:hover{transform:translateY(-3px);box-shadow:0 8px 22px rgba(30,42,74,.14);border-top-color:var(--rust);}
.home-card:nth-child(3n+2){border-top-color:var(--rust);}
.home-card:nth-child(3n){border-top-color:var(--gold);}
.hc-num{font-family:'Helvetica Neue',Arial,sans-serif;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--rust);}
.hc-title{font-size:19px;color:var(--navy);margin:8px 0 8px;line-height:1.25;}
.hc-blurb{font-size:14px;color:var(--muted);margin:0 0 16px;flex:1;}
.hc-go{font-family:'Helvetica Neue',Arial,sans-serif;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--navy);font-weight:bold;}

.pagenav{display:flex;justify-content:space-between;gap:14px;margin-top:64px;border-top:1px solid var(--line);padding-top:20px;flex-wrap:wrap;}
.pn{display:flex;flex-direction:column;text-decoration:none;padding:12px 18px;background:var(--paper);border:1px solid var(--line);min-width:200px;flex:1;color:var(--ink);transition:border-color .12s ease,background .12s ease;}
.pn:hover{border-color:var(--rust);background:#FBF7EE;}
.pn.next{text-align:right;align-items:flex-end;}
.pn span{font-family:'Helvetica Neue',Arial,sans-serif;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}
.pn b{color:var(--navy);font-size:15px;margin-top:2px;}
@media(max-width:600px){.pn{min-width:100%;}}
'''
open(os.path.join(OUT, "style.css"), "w", encoding="utf-8").write(style + extra_css)
print("wrote style.css")
print("DONE ->", OUT)
'''
'''
