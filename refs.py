# Curated reference list for the PH Boat pack.
# URLs taken verbatim from the research doc's Works Cited (not invented).
# Shared by build.py (site) and make_doc.py (Google Doc source).

REFS = [
    ("seas",            "MARINA MC DS-2026-01 - SEAS online-ticketing mandate (Apr 2026)", "https://marina.gov.ph/2026/04/11/safer-travel-thru-seas-marina-mandates-online-ticketing-system-for-domestic-passenger-ships/"),
    ("ra11659",         "RA 11659 - foreign-ownership liberalization (NDV Law analysis)", "https://ndvlaw.com/how-foreigners-can-own-100-of-philippine-telecom-and-transport-firms/"),
    ("marina2024",      "MARINA 2024 Statistical Report", "https://marina.gov.ph/wp-content/uploads/2025/11/2024-MARINA-STATISTICAL-REPORT.pdf"),
    ("marina2023",      "MARINA 2023 Statistical Report", "https://marina.gov.ph/wp-content/uploads/2025/01/MARINA-Stat-Report-2023-Final-v2.pdf"),
    ("marina2019",      "MARINA 2019 Statistical Report", "https://marina.gov.ph/wp-content/uploads/2020/10/2019-marina-statistical-report.pdf"),
    ("eo305",           "EO 305 - sub-3GT banca registration devolved to LGUs (NAST / DOST)", "https://nast.dost.gov.ph/index.php/downloads/category/109-day-2-march-14-2017?download=351:2-engr-lanoy-municipal-fishing-boats"),
    ("mc2016",          "MARINA MC 2016-02 - wooden-hull passenger phase-out", "https://marina.gov.ph/wp-content/uploads/2018/06/MC-2016-02.pdf"),
    ("guimaras",        "MARINA denies Guimaras wooden-hull extension (Guimaras LGU)", "https://guimaras.gov.ph/news-and-updates/marina-denies-guimaras-appeal-to-extend-operation-of-wooden-hulled-boats/"),
    ("ppa",             "PPA 2025 passenger movements & targets (PortCalls)", "https://portcalls.com/ppa-poised-to-hit-2025-targets-optimistic-of-steady-performance/"),
    ("ppa_holiday",     "PPA record 6.2M Yuletide port passengers (Manila Bulletin)", "https://mb.com.ph/2026/01/07/ppa-logs-record-breaking-62-m-port-passengers-during-yuletide-travel-rush"),
    ("ppa_holiday_pna", "PPA 4.7M holiday passengers (Philippine News Agency)", "https://www.pna.gov.ph/articles/1241120"),
    ("dot",             "DOT international tourist arrivals (ABS-CBN)", "https://www.abs-cbn.com/business/01/04/24/philippines-eyes-77-million-foreign-tourists-in-2024"),
    ("elnido",          "El Nido 500,408 arrivals, 2023 (PIA)", "https://mirror.pia.gov.ph/news/2024/01/08/el-nido-sets-tourism-record-with-over-half-million-visitors-in-2023"),
    ("mdpi",            "Spatial analysis of PH maritime disasters 2015-2020 (MDPI)", "https://www.mdpi.com/2220-9964/14/1/31"),
    ("uwan",            "6,607 stranded, Super Typhoon Uwan (Inquirer / PCG)", "https://newsinfo.inquirer.net/2136756/over-6000-passengers-stranded-in-ports-nationwide-due-to-uwan-pcg"),
    ("ramil",           "4,388 stranded, TS Ramil (Inquirer)", "https://newsinfo.inquirer.net/2126619/over-3200-passengers-stranded-as-typhoon-ramil-disrupts-port-operations"),
    ("ferry12go",       "El Nido-Coron ferry fares (12Go)", "https://12go.asia/en/ferry/el-nido/coron"),
    ("seatours",        "Seatours Palawan - charter & expedition rate card", "https://seatourspalawan.com/"),
    ("gyg",             "GetYourGuide - El Nido private tours", "https://www.getyourguide.com/el-nido-l974/private-tours-tc221/"),
    ("elnidoparadise",  "El Nido Paradise - Tour A booking (group fares)", "https://www.elnidoparadise.com/booking/main-island-hopping-tours/tour-a/"),
    ("barkota",         "Barkota - ferry aggregator & booking SaaS", "https://www.barkota.com/"),
    ("tripket",         "Tripket PH - mobile ferry aggregator", "https://apps.apple.com/us/app/tripket-ph/id6475034217"),
    ("klook",           "Klook supplier commission structure (Bokun guide)", "https://www.bokun.io/klook-supplier"),
    ("twelvego",        "12Go affiliate program (~$3 per booking)", "https://agent.12go.asia/"),
    ("getmyboat",       "GetMyBoat - Philippines boat rentals", "https://www.getmyboat.com/boat-rental/Philippines/"),
    ("caticlan",        "Caticlan co-op vs Montenegro Lines (Aklan Forum)", "https://aklanforum.blogspot.com/2008/09/boracay-boat-coop-opposes-montenegro.html"),
    ("biyaheroes",      "Biyaheroes shutdown (Tracxn profile)", "https://tracxn.com/d/companies/biyaheroes/__l0rxxMH0I55i0_Gi8jwxkvFjcaDUhbA2-Ezge4xFqgY"),
    ("tripsta",         "Tripsta collapse (PhocusWire)", "https://www.phocuswire.com/Tripsta-suspends-travel-travel-agency-operations"),
    ("paymongo",        "PayMongo / Maya / GCash fee schedules", "https://www.paymongo.com/blog/maya-vs-gcash-vs-paymongo-for-business"),
]

_ALL = [k for k, _, _ in REFS]

PAGE_REFS = {
    "s1": ["seas", "eo305", "ra11659", "marina2024", "marina2019", "mdpi", "uwan"],
    "s2": ["ppa", "ppa_holiday", "ppa_holiday_pna", "dot", "elnido", "marina2019", "marina2023",
           "marina2024", "eo305", "mc2016", "guimaras", "ferry12go", "seatours", "gyg",
           "elnidoparadise", "barkota", "tripket", "klook", "twelvego", "getmyboat", "caticlan",
           "seas", "ra11659", "mdpi", "uwan", "ramil", "biyaheroes", "tripsta", "paymongo"],
    "s3": ["marina2024", "mc2016", "seatours", "elnidoparadise"],
    "s5": ["mdpi", "mc2016", "eo305", "seas", "caticlan", "ra11659"],
    "s6": ["seatours", "klook", "paymongo", "elnido", "marina2024", "mdpi"],
    "s7": _ALL,
}

# Inline footnote markers: (page, anchor text to place a superscript AFTER, ref key).
# Anchors must be distinctive visible strings that appear in NON-SVG page HTML (a marker
# inserted inside <svg> text would corrupt the figure), and only the first match is marked.
CITES = [
    # Section 1 - Problem
    ("s1", "24,483 motorbancas", "marina2019"),
    ("s1", "81% of accredited entities", "marina2024"),
    ("s1", "Executive Order 305", "eo305"),
    ("s1", "DS-2026-01", "seas"),
    ("s1", "RA 11659 removed", "ra11659"),
    ("s1", "most fatal accident category", "mdpi"),
    ("s1", "strand thousands", "uwan"),
    # Section 2 - Research & Data
    ("s2", "85.41M", "ppa"),
    ("s2", "4.7M", "ppa_holiday"),
    ("s2", "PPA / PNA / Manila Bulletin", "ppa_holiday_pna"),
    ("s2", "5.45M", "dot"),
    ("s2", "500,408", "elnido"),
    ("s2", "28,210", "marina2019"),
    ("s2", "16,000", "marina2023"),
    ("s2", "3,438", "marina2024"),
    ("s2", "Devolved to LGUs", "eo305"),
    ("s2", "FRP replacement ₱5", "mc2016"),
    ("s2", "Guimaras LGU", "guimaras"),
    ("s2", "Consumer aggregator (13+ lines", "barkota"),
    ("s2", "Mobile-first aggregator", "tripket"),
    ("s2", "Klook 20", "klook"),
    ("s2", "12Go affiliate", "twelvego"),
    ("s2", "GetMyBoat", "getmyboat"),
    ("s2", "30,000+ guests/yr", "seatours"),
    ("s2", "GetYourGuide and integrated locals", "gyg"),
    ("s2", "Caticlan coop", "caticlan"),
    ("s2", "MC DS-2026-01 (Apr 2026)", "seas"),
    ("s2", "RA 11659 (2022)", "ra11659"),
    ("s2", "4,467 maritime accidents", "mdpi"),
    ("s2", "6,607 stranded", "uwan"),
    ("s2", "4,388", "ramil"),
    ("s2", "Biyaheroes", "biyaheroes"),
    ("s2", "Tripsta", "tripsta"),
    # Section 3 - Personas
    ("s3", "private charter day: $150", "seatours"),
    ("s3", "threatens a ₱5", "mc2016"),
    ("s3", "₱1,800 group tours", "elnidoparadise"),
    # Section 5 - Econ concepts
    ("s5", "EO 305's devolution", "eo305"),
    ("s5", "with a ₱5", "mc2016"),
    ("s5", "Caticlan coop blocking", "caticlan"),
    ("s5", "SEAS's own justification", "seas"),
    # Section 6 - Business model
    ("s6", "Sea Quest/operator rate cards", "seatours"),
    ("s6", "vs. Klook 20", "klook"),
    ("s6", "PayMongo/Maya rate cards", "paymongo"),
    ("s6", "500K visitors/yr", "elnido"),
    # Section 7 - Slides
    ("s7", "4,467 accidents", "mdpi"),
    ("s7", "6,607 stranded", "uwan"),
    ("s7", "El Nido 500K", "elnido"),
    ("s7", "SEAS (MC DS-2026-01)", "seas"),
]

LUT = {k: (label, url) for k, label, url in REFS}
