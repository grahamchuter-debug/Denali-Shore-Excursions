#!/usr/bin/env python3
"""Generate Denali Shore Excursions static site with clean URLs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://denalishoreexcursions.com"
SITE = "Denali Shore Excursions"
DATE = "2026-06-24"
ENQUIRY_EMAIL = "enquiries@denalishoreexcursions.com"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700"
    "&family=DM+Sans:wght@400;500;600;700&display=swap"
)
HERO_GRADIENT = (
    "linear-gradient(135deg, rgba(12, 74, 110, 0.78) 0%, "
    "rgba(8, 145, 178, 0.62) 52%, rgba(15, 118, 110, 0.58) 100%)"
)
ACCENT = "text-teal-400"

IMG = {
    "home": (
        "images/hero-denali.png",
        "Denali mountain reflected in a tundra lake with autumn-colored foreground on a clear Alaska day",
    ),
    "best": ("images/best-denali-excursions.png", "Best Denali excursions and Alaska land tour options"),
    "park": (
        "images/denali-national-park.png",
        "Caribou on a tundra hillside with snow-capped Alaska Range peaks in Denali National Park",
    ),
    "cruise": ("images/denali-cruise-passengers.png", "Alaska cruise passengers planning a Denali land extension"),
    "anchorage": ("images/anchorage-to-denali.png", "Scenic route from Anchorage toward Denali National Park"),
    "best_time": ("images/best-time.png", "Best time to visit Denali National Park Alaska"),
    "wildlife": (
        "images/denali-wildlife.png",
        "Bull moose crossing the Denali park road in front of a Wonder Lake tour bus",
    ),
    "flightseeing": (
        "images/denali-flightseeing.png",
        "Aerial view of snow-capped Alaska Range peaks and green valleys on a Denali flightseeing tour",
    ),
    "train": ("images/denali-train.png", "Alaska Railroad Denali Star train through interior Alaska"),
    "fairbanks": ("images/fairbanks-to-denali.png", "Route from Fairbanks to Denali National Park"),
    "intro": ("images/intro.png", "Denali National Park tundra and mountain panorama"),
    "faq": ("images/faq.png", "Frequently asked questions about Denali land tours"),
    "planner": ("images/planner.png", "Denali cruise land tour planning checklist"),
    "enquire": ("images/enquire.png", "Enquire about Denali excursions and land tours"),
    "national_park_tour": (
        "images/national-park-tour.png",
        "Caribou on a tundra hillside with snow-capped Alaska Range peaks in Denali National Park",
    ),
    "wildlife_tour": (
        "images/wildlife-tour.png",
        "Bull moose crossing the Denali park road in front of a Wonder Lake tour bus",
    ),
    "tundra_tour": ("images/tundra-tour.png", "Tundra wilderness experience in Denali Alaska"),
    "flightseeing_tour": (
        "images/flightseeing-tour.png",
        "Aerial view of snow-capped Alaska Range peaks and green valleys on a Denali flightseeing tour",
    ),
    "atv_tour": ("images/atv-tour.png", "ATV adventure tour near Denali National Park"),
    "rafting_tour": ("images/rafting-tour.png", "River rafting excursion near Denali Alaska"),
    "zipline_tour": ("images/zipline-tour.png", "Zipline adventure with Alaska mountain views"),
    "hiking_tour": ("images/hiking-tour.png", "Guided hiking and nature walk in Denali region"),
    "anchorage_transfer": (
        "images/anchorage-transfer.png",
        "Anchorage skyline and Chugach Mountains viewed from above on a transfer with sightseeing",
    ),
    "fairbanks_transfer": ("images/fairbanks-transfer.png", "Fairbanks to Denali transfer with scenic routing"),
}


def u(slug: str = "") -> str:
    return "/" if not slug else f"/{slug}"


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


def write_page(slug: str, html: str) -> None:
    path = "index.html" if not slug else f"{slug}/index.html"
    write(path, html)


def breadcrumb_schema(slug: str, name: str) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"}]
    if slug:
        items.append({"@type": "ListItem", "position": 2, "name": name, "item": f"{DOMAIN}/{slug}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def faq_schema(qa: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ],
    }


def inject_schemas(html: str, schemas: list[dict]) -> str:
    block = "".join(
        f'  <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n  </script>\n'
        for s in schemas
    )
    return html.replace('  <meta name="twitter:card"', block + '  <meta name="twitter:card"', 1)


def page_shell(
    *,
    title: str,
    description: str,
    keywords: str,
    slug: str,
    data_page: str,
    hero: str,
    content: str,
    preload: str,
    trust: bool = True,
) -> str:
    canon = f"{DOMAIN}/" if not slug else f"{DOMAIN}/{slug}"
    trust_attr = '\n  data-trust-strip="/partials/trust-strip.html"' if trust else ""
    content_file = content if content.startswith("/content/") else f"/content/{content}"
    hero_path = hero if hero.startswith("/") else f"/{hero}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canon}" />
  <link rel="preload" as="image" href="/{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{DOMAIN}/{preload}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{data_page}" data-hero="{hero_path}" data-content="{content_file}"{trust_attr}>
  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <div id="page-trust-strip"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>
  <script src="/js/site.js"></script>
</body>
</html>
"""


def _wave() -> str:
    return '<div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>'


def hero(
    eyebrow: str,
    title: str,
    lead: str,
    image_key: str,
    breadcrumb: str = "",
    cta: tuple[str, str] | None = None,
    tags: list[str] | None = None,
    section_class: str = "site-hero",
    bg_class: str = "hero-bg-custom",
) -> str:
    image, aria = IMG[image_key]
    bc = ""
    if breadcrumb:
        bc = f"""<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/65" aria-label="Breadcrumb">
        <a href="/" class="hover:text-white transition-colors">Home</a>
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-white/85">{breadcrumb}</span>
      </nav>"""
    cta_html = (
        f'<a href="{u(cta[0])}" class="btn-ocean inline-flex items-center justify-center gap-2 text-white '
        f'font-semibold px-7 py-3 rounded-full text-sm shadow-xl">{cta[1]}</a>'
        if cta
        else ""
    )
    tags_html = ""
    if tags:
        tags_html = '<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">' + "".join(
            f'<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full '
            f'px-3.5 py-1.5 text-xs font-semibold text-white">{t}</span>'
            for t in tags
        ) + "</div>"
    return f"""<section class="{section_class}">
  <div class="absolute inset-0 {bg_class}" style="background-image: {HERO_GRADIENT}, url('/{image}');" role="img" aria-label="{aria}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">{bc}
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{eyebrow}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">{lead}</p>
      <div class="site-hero__actions flex flex-col sm:flex-row gap-3">{cta_html}</div>
      {tags_html}
    </div>
  </div>
  {_wave()}
</section>"""


def internal_links() -> str:
    links = [
        ("best-denali-excursions", "Best Excursions"),
        ("denali-for-cruise-passengers", "Cruise Passengers"),
        ("denali-national-park-guide", "Park Guide"),
        ("anchorage-to-denali-guide", "Anchorage Route"),
        ("denali-wildlife-guide", "Wildlife Guide"),
        ("denali-faq", "FAQ"),
        ("enquire", "Enquire"),
    ]
    parts = []
    for i, (slug, label) in enumerate(links):
        if i:
            parts.append('<span class="text-gray-300">·</span>')
        parts.append(f'<a href="{u(slug)}" class="text-ocean-600 hover:text-ocean-800 font-medium">{label}</a>')
    return f"""<nav class="mt-10 pt-8 border-t border-gray-100" aria-label="Related Denali guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your Denali land extension</p>
  <div class="flex flex-wrap gap-3 text-sm">{"".join(parts)}</div>
</nav>"""


def help_cta() -> str:
    return f"""<div class="text-center mt-8 p-6 bg-alpine-50 rounded-2xl border border-alpine-100">
  <p class="text-gray-700 font-medium mb-3">Need help choosing the right Denali experience?</p>
  <a href="{u('enquire')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Get personalised advice →</a>
</div>"""


def commercial_strip(best_for: str, wildlife: str, typical_time: str, pre_post: str) -> str:
    return f"""<aside class="commercial-strip" aria-label="Cruise passenger highlights">
  <h3>Why cruise passengers choose this</h3>
  <ul>
    <li><strong>Best for cruise passengers:</strong> {best_for}</li>
    <li><strong>Wildlife and scenic highlights:</strong> {wildlife}</li>
    <li><strong>Typical time needed:</strong> {typical_time}</li>
    <li><strong>Pre/post-cruise suitability:</strong> {pre_post}</li>
  </ul>
  {help_cta()}
</aside>"""


def land_tour_snapshot(**kw: str) -> str:
    defaults = dict(
        days_needed="2-4 days for a balanced park visit with one major activity day",
        hub_connection="Anchorage, Fairbanks, Seward, Whittier — by road, rail or transfer",
        best_for="National park tours, wildlife viewing, flightseeing and guided adventures",
        activity_level="Easy coach tours to moderate hiking and active excursions",
        wildlife="Moose, caribou, Dall sheep, bears and wolves depending on season",
        popular="Park road tour, wildlife tour, flightseeing, rafting and nature walks",
        pre_post="Designed as a pre- or post-cruise Alaska interior land extension",
    )
    defaults.update(kw)
    rows = "".join(
        f'<div class="cruise-snapshot__item"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in [
            ("Days Needed", defaults["days_needed"]),
            ("Best Hub Connection", defaults["hub_connection"]),
            ("Best For", defaults["best_for"]),
            ("Activity Level", defaults["activity_level"]),
            ("Wildlife Opportunities", defaults["wildlife"]),
            ("Popular Experience Types", defaults["popular"]),
            ("Pre/Post-Cruise Fit", defaults["pre_post"]),
        ]
    )
    return f"""<aside class="cruise-snapshot mb-10 px-4 sm:px-0" aria-label="Land tour snapshot">
  <h3 class="font-display font-bold text-lg text-gray-900 mb-4">Land Tour Snapshot</h3>
  <dl class="cruise-snapshot__grid">{rows}</dl>
</aside>"""


def excursion_meta(
    duration: str,
    fitness: str,
    wildlife: str,
    scenic_highlights: str,
    best_for: str,
    hub_connection: str,
    pre_post: str,
) -> str:
    cards = [
        ("Duration", duration),
        ("Fitness Level", fitness),
        ("Wildlife Opportunities", wildlife),
        ("Scenic Highlights", scenic_highlights),
        ("Best For", best_for),
        ("Hub Connection", hub_connection),
        ("Pre/Post-Cruise Suitability", pre_post),
    ]
    body = "".join(
        f'<div class="excursion-meta__card"><h4>{h}</h4><p>{p}</p></div>' for h, p in cards
    )
    return f'<div class="excursion-meta max-w-5xl mx-auto px-4">{body}</div>'


def faq_block(items: list[tuple[str, str]]) -> str:
    body = "".join(
        f'<details class="faq-item rounded-2xl border border-alpine-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">{q}</summary><p class="mt-4 text-sm text-gray-500">{a}</p></details>'
        for q, a in items
    )
    return f'<section class="py-8"><div class="max-w-3xl mx-auto px-4 space-y-4"><h2 class="text-2xl font-display font-bold text-gray-900 mb-6">Frequently Asked Questions</h2>{body}</div></section>'


def card_grid(cards: list[tuple[str, str, str, str, str]]) -> str:
    items = []
    for img_key, title, desc, slug, label in cards:
        img, alt = IMG[img_key]
        items.append(f"""<div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-alpine-50 flex flex-col">
      <div class="card-media h-44 relative overflow-hidden"><img src="/{img}" alt="{alt}" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1">
        <h3 class="text-lg font-display font-semibold text-gray-900 mb-2">{title}</h3>
        <p class="text-sm text-gray-500 leading-relaxed flex-1">{desc}</p>
        <a href="{u(slug)}" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">{label}</a>
      </div>
    </div>""")
    return '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">' + "".join(items) + "</div>"


def comparison_table() -> str:
    rows = [
        ("Denali National Park Tour", "6-8 hrs", "Park road scenery and interpretation", "Easy", "denali-national-park-tour"),
        ("Denali Wildlife Tour", "4-6 hrs", "Big-game viewing focus", "Easy", "denali-wildlife-tour"),
        ("Tundra Wilderness Tour", "4-5 hrs", "Open tundra and alpine views", "Easy to moderate", "denali-tundra-wilderness-tour"),
        ("Denali Flightseeing Tour", "1.5-3 hrs", "Aerial views of Denali peak", "Easy", "denali-flightseeing-tour"),
        ("Denali ATV Tour", "2-3 hrs", "Active off-road adventure", "Moderate", "denali-atv-tour"),
        ("Denali River Rafting", "2-4 hrs", "Scenic float or whitewater", "Easy to moderate", "denali-rafting-tour"),
        ("Denali Zipline Adventure", "2-3 hrs", "Forest canopy and mountain views", "Moderate", "denali-zipline-tour"),
        ("Hiking & Nature Walk", "3-5 hrs", "Guided trails and ecology", "Moderate", "denali-hiking-nature-walk"),
        ("Anchorage Transfer + Sightseeing", "7-9 hrs", "One-way with scenic stops", "Easy", "anchorage-to-denali-transfer-with-sightseeing"),
        ("Fairbanks Transfer + Sightseeing", "3-5 hrs", "Interior transfer plus stops", "Easy", "fairbanks-to-denali-transfer-with-sightseeing"),
    ]
    body = "".join(
        f"""<tr class="border-b border-alpine-50 hover:bg-sand-50/80">
      <td class="py-4 pr-4 font-semibold text-gray-900"><a href="{u(link)}" class="text-ocean-600 hover:text-ocean-800">{name}</a></td>
      <td class="py-4 px-3 text-gray-600">{dur}</td>
      <td class="py-4 px-3 text-gray-600">{best}</td>
      <td class="py-4 px-3 text-gray-600">{act}</td>
      <td class="py-4 pl-3"><a href="{u(link)}" class="text-teal-600 font-medium text-xs whitespace-nowrap">Guide →</a></td>
    </tr>"""
        for name, dur, best, act, link in rows
    )
    return f"""<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 text-center mb-4">Which Denali Experience Is Right for Me?</h2>
  <p class="text-center text-gray-600 text-sm max-w-2xl mx-auto mb-10">Compare durations, fitness, wildlife potential and pre/post-cruise fit across Denali's most-booked land tour experiences.</p>
  <div class="overflow-x-auto rounded-3xl border border-alpine-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[720px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold rounded-tl-3xl">Excursion</th>
        <th class="py-4 px-3 font-semibold">Duration</th>
        <th class="py-4 px-3 font-semibold">Best For</th>
        <th class="py-4 px-3 font-semibold">Fitness Level</th>
        <th class="py-4 px-4 font-semibold rounded-tr-3xl">Details</th>
      </tr></thead>
      <tbody class="bg-white">{body}</tbody>
    </table>
  </div>
</div></section>"""


def excursion_page(ex: dict) -> str:
    img, alt = IMG[ex["image"]]
    bullets = "".join(
        f'<li class="flex gap-2 text-sm text-gray-600"><span class="text-ocean-500">✓</span>{b}</li>'
        for b in ex["bullets"]
    )
    snap = land_tour_snapshot(**ex.get("land_tour_snapshot", {}))
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div><p class="text-gray-600 leading-relaxed mb-6">{ex["intro"]}</p><ul class="space-y-3 mb-6">{bullets}</ul></div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{img}" alt="{alt}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-4 bg-white">{excursion_meta(ex["duration"], ex["fitness"], ex["wildlife"], ex["scenic_highlights"], ex["best_for"], ex["hub_connection"], ex["pre_post"])}</section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip(ex["best_for"], ex["wildlife"], ex["typical_time"], ex["pre_post"])}</div></section>
{faq_block(ex["faq"])}
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <a href="{u('enquire')}" class="btn-ocean inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full shadow-lg">{ex["cta"]}</a>
  {internal_links()}
</div></section>"""


def content_home() -> str:
    cards = card_grid([
        ("national_park_tour", "Denali National Park Tour", "Classic park road experience with Alaska Range views and naturalist interpretation.", "denali-national-park-tour", "View Guide"),
        ("wildlife_tour", "Denali Wildlife Tour", "Focused wildlife viewing along proven routes with expert guides.", "denali-wildlife-tour", "View Guide"),
        ("flightseeing_tour", "Denali Flightseeing", "Aerial perspective on North America's highest peak and surrounding glaciers.", "denali-flightseeing-tour", "View Guide"),
        ("anchorage_transfer", "Anchorage Transfer + Sightseeing", "Scenic one-way transfer that turns travel day into part of the adventure.", "anchorage-to-denali-transfer-with-sightseeing", "View Guide"),
    ])
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Alaska Interior · Land Tours</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Cruise land extension.<br/><span class="text-ocean-600">Denali National Park access.</span></h2>
    <p class="text-gray-600 leading-relaxed mb-5">Denali is not a cruise port — it is Alaska's premier interior destination for pre- and post-cruise land tours. This guide helps cruise passengers plan national park visits, wildlife experiences and flightseeing around realistic travel days from Anchorage or Fairbanks.</p>
    <a href="{u('best-denali-excursions')}" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Browse All Excursions</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden"><img src="/{IMG['intro'][0]}" alt="{IMG['intro'][1]}" width="800" height="600" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{land_tour_snapshot()}</div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-12"><h2 class="text-3xl font-display font-bold text-gray-900">Top Denali Experiences</h2></div>
  {cards}
</div></section>
{comparison_table()}
<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Plan Your Denali Land Extension</h2>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <a href="{u('denali-for-cruise-passengers')}" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Cruise Passenger Guide</a>
    <a href="{u('denali-cruise-tour-planner')}" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Tour Planner</a>
  </div>
</div></section>"""


def content_best() -> str:
    cards = card_grid([
        ("national_park_tour", "Denali National Park Tour", "Essential park road experience for first-time visitors.", "denali-national-park-tour", "Guide"),
        ("wildlife_tour", "Denali Wildlife Tour", "Highest wildlife focus with guided interpretation.", "denali-wildlife-tour", "Guide"),
        ("flightseeing_tour", "Denali Flightseeing", "Unmatched aerial views when weather cooperates.", "denali-flightseeing-tour", "Guide"),
        ("anchorage_transfer", "Anchorage Transfer + Sightseeing", "Best for guests arriving from or returning to Anchorage.", "anchorage-to-denali-transfer-with-sightseeing", "Guide"),
    ])
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Best Denali Excursions</h2>
  <p class="text-gray-600 leading-relaxed text-sm">Independent comparison for cruise passengers choosing between park tours, wildlife experiences, adventure activities and scenic transfers.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip('Guests adding an Alaska interior land extension', 'Moose, caribou, Dall sheep, bears and dramatic mountain scenery', 'Most experiences need 1-3 days beyond travel time', 'Built for pre- or post-cruise itineraries with flexible scheduling')}</div></section>
{comparison_table()}
<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Most Booked Guides</h2>
  {cards}
  <div class="mt-12 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


def content_park_guide() -> str:
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <p class="text-gray-600 leading-relaxed text-sm">Denali National Park protects six million acres of subarctic wilderness. Private vehicles are limited beyond Mile 15 on the park road, so most visitors explore by narrated bus tour, transit bus or guided excursion.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{land_tour_snapshot(popular='Park road tour, wildlife tour, tundra wilderness, flightseeing')}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-7xl mx-auto px-4">
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8 max-w-5xl mx-auto"><img src="/{IMG['park'][0]}" alt="{IMG['park'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <div class="grid lg:grid-cols-2 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-alpine-100"><h3 class="font-display font-bold text-lg mb-2">Park Road Access</h3><p class="text-gray-600">The 92-mile park road winds through tundra, river valleys and mountain passes. Tour buses reach deeper sections where wildlife sightings are most common.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-alpine-100"><h3 class="font-display font-bold text-lg mb-2">What To Expect</h3><p class="text-gray-600">Weather changes quickly. Dress in layers, bring binoculars and plan for a full day when booking a deep-park tour. Denali peak is visible only on clear days.</p></div>
  </div>
</div></section>
<section class="py-12 bg-white"><div class="max-w-7xl mx-auto px-4">
  <div class="grid sm:grid-cols-3 gap-6 text-sm">
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Season</strong><p class="mt-2 text-gray-600">Main visitor season runs mid-May through mid-September when park road transit operates fully.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Wildlife</strong><p class="mt-2 text-gray-600">The park's Big Five — moose, caribou, Dall sheep, wolves and bears — are seen regularly on bus routes.</p></div>
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Booking</strong><p class="mt-2 text-gray-600">Reserve park tours and lodges early for peak summer weeks, especially for cruise-linked travel dates.</p></div>
  </div>
  <p class="text-center mt-8"><a href="{u('denali-national-park-tour')}" class="text-ocean-600 font-semibold text-sm">National park tour guide →</a></p>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


CRUISE_FAQ = [
    ("Is Denali worth adding to an Alaska cruise?", "For many travelers, yes. Denali delivers interior wilderness, wildlife and mountain scenery that Gulf of Alaska cruises do not include."),
    ("How many days do I need for Denali?", "Plan at least two nights and one full activity day. Three to four nights allows a park tour plus a second experience like flightseeing or rafting."),
    ("Should I visit Denali before or after my cruise?", "Both work. Pre-cruise visits from Anchorage are common; post-cruise routing through Fairbanks suits northbound itineraries."),
    ("Can I book independently instead of through my cruise line?", "Yes. Independent booking often offers more choice and better value, but you manage your own transport and timing."),
]


def content_cruise_passengers() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6"><strong>Denali is not a cruise port.</strong> It is an interior land destination reached by road, rail or air from Anchorage, Fairbanks or Alaska cruise embarkation points. Most cruise passengers add Denali as a pre- or post-cruise extension rather than a port-day stop.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Before or After Your Cruise?</h2>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Pre-cruise from Anchorage</strong><p class="mt-2 text-gray-600">Fly into Anchorage, spend 2-4 nights in Denali, then continue to your cruise port by motorcoach, rail or transfer service. Works well for southbound Gulf itineraries.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Post-cruise to Fairbanks</strong><p class="mt-2 text-gray-600">Disembark at an Alaska port, travel to Denali, then continue north to Fairbanks for your flight home. Suits itineraries ending in interior Alaska.</p></div>
  </div>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">How Many Days Do You Need?</h2>
  <p class="text-gray-600 text-sm mb-6">A rushed overnight barely allows one park tour. We recommend a minimum of two nights and one full day for a park bus tour, plus travel days on each end. Add a night for flightseeing, rafting or a second guided activity.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Getting There From Cruise Hubs</h2>
  <ul class="space-y-3 text-sm text-gray-600 mb-8">
    <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Anchorage:</strong> 4-5 hours by road or ~8 hours on the Alaska Railroad Denali Star. Most popular pre-cruise routing.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Fairbanks:</strong> 2-3 hours south by road or rail. Natural post-cruise connection for northbound travel.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Seward:</strong> Connect north through Anchorage by motorcoach, rail or transfer. Allow two travel days minimum.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Whittier:</strong> Connect via Anchorage or a transfer package after disembarking. Allow a full travel day.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Other Alaska ports:</strong> Most require a transfer through Anchorage or Fairbanks. Plan overnight stops if distances are long.</li>
  </ul>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Cruise Line Tours vs Independent</h2>
  <p class="text-gray-600 text-sm mb-4">Cruise line land packages bundle transport, lodging and tours with minimal planning. Independent booking gives you control over hotel choice, tour operators and pace — often at lower cost for the same experiences.</p>
  <p class="text-gray-600 text-sm mb-8">If you book independently, confirm transfer timing around embarkation and disembarkation, and reserve park tours early for July and August.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Best Excursions for Cruise Passengers</h2>
  <p class="text-gray-600 text-sm mb-4">Start with a <a href="{u('denali-national-park-tour')}" class="text-ocean-600 font-semibold">national park bus tour</a> for wildlife and scenery. Add <a href="{u('denali-flightseeing-tour')}" class="text-ocean-600 font-semibold">flightseeing</a> if weather allows, or choose an adventure activity like <a href="{u('denali-rafting-tour')}" class="text-ocean-600 font-semibold">rafting</a> or a <a href="{u('denali-hiking-nature-walk')}" class="text-ocean-600 font-semibold">guided hike</a> for a second day.</p>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8"><img src="/{IMG['cruise'][0]}" alt="{IMG['cruise'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <div class="mb-8">{land_tour_snapshot(days_needed='2-4 nights recommended for cruise-linked itineraries')}</div>
  {faq_block(CRUISE_FAQ)}
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_anchorage_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">Anchorage is the most common gateway for cruise passengers heading to Denali. The route north follows the Parks Highway through Matanuska Valley, Talkeetna and broad river corridors toward the Alaska Range.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Travel Options</h2>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Rental car</strong><p class="mt-2 text-gray-600">Roughly 4-5 hours driving without long stops. Flexibility to pause at viewpoints, Talkeetna or Willow.</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Motorcoach</strong><p class="mt-2 text-gray-600">Scheduled coaches run daily in summer. Sit back and enjoy narration while someone else handles the road.</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Alaska Railroad</strong><p class="mt-2 text-gray-600">The Denali Star departs Anchorage mid-morning and arrives early evening. Scenic dome cars available. See our <a href="{u('denali-train-guide')}" class="text-ocean-600 font-semibold">train guide</a>.</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Transfer with sightseeing</strong><p class="mt-2 text-gray-600">Guided transfer packages combine transport with curated stops. Ideal when you want highlights without driving.</p></div>
  </div>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Time Needed</h2>
  <p class="text-gray-600 text-sm mb-8">Allow a full day for the journey if you include scenic stops or rail travel. Driving alone takes 4-5 hours; the Denali Star train is roughly 8 hours. Same-day arrival plus a park tour is possible only with very early departures — most cruise passengers prefer to travel one day and tour the next.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Should You Overnight En Route?</h2>
  <p class="text-gray-600 text-sm mb-4">An overnight at the Denali park gateway is essential for a proper visit — you need at least one night before your first park tour. A midway stop in Talkeetna or Denali State Park viewpoints is worthwhile if you want to break up the drive or add flightseeing without rushing.</p>
  <p class="text-gray-600 text-sm mb-8">Pre-cruise travellers often overnight in Anchorage the night before heading north. Post-cruise guests disembarking at Seward or Whittier should plan an Anchorage stop before the Denali leg unless using a multi-day transfer package.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Scenic Stops Worth Considering</h2>
  <ul class="space-y-2 text-sm text-gray-600 mb-8">
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Matanuska Glacier viewpoints and glacier-access tours near Sutton</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Talkeetna — flightseeing base with views of the Alaska Range</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Byers Lake and Denali State Park viewpoints south of the park entrance</li>
  </ul>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Sample Itineraries</h2>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-sand-50 rounded-2xl p-5"><strong>2 nights:</strong> Day 1 travel north, Day 2 park tour, Day 3 return or continue.</div>
    <div class="bg-sand-50 rounded-2xl p-5"><strong>3 nights:</strong> Travel day, park tour, second activity (flightseeing or rafting), depart.</div>
    <div class="bg-sand-50 rounded-2xl p-5"><strong>4 nights:</strong> Add Talkeetna flightseeing or a slower drive with overnight midway.</div>
  </div>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8"><img src="/{IMG['anchorage'][0]}" alt="{IMG['anchorage'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <a href="{u('anchorage-to-denali-transfer-with-sightseeing')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Transfer with sightseeing guide →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_fairbanks_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">Fairbanks sits roughly 120 miles north of Denali, making it a natural post-cruise hub for travelers ending their Alaska trip in the interior. The drive south follows the Parks Highway through Nenana and broad river valleys.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Travel Options</h2>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Rental car</strong><p class="mt-2 text-gray-600">About 2-3 hours without stops. Straightforward summer driving on paved highway.</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Motorcoach</strong><p class="mt-2 text-gray-600">Regular summer service connects Fairbanks and the Denali park entrance area.</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Alaska Railroad</strong><p class="mt-2 text-gray-600">Northbound and southbound Denali Star service links Fairbanks and Denali in roughly 4 hours.</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Transfer with sightseeing</strong><p class="mt-2 text-gray-600">Shorter than the Anchorage route but still benefits from guided interpretation and planned stops.</p></div>
  </div>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Why Fairbanks Works Post-Cruise</h2>
  <p class="text-gray-600 text-sm mb-6">Many northbound Alaska cruises end at interior or northern ports. Routing through Denali before flying home from Fairbanks avoids backtracking to Anchorage and distributes travel days evenly across your land extension.</p>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8"><img src="/{IMG['fairbanks'][0]}" alt="{IMG['fairbanks'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <a href="{u('fairbanks-to-denali-transfer-with-sightseeing')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Fairbanks transfer guide →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


BEST_TIME_FAQ = [
    ("When is the best month for cruise passengers to visit Denali?", "June through early September offers full park road access, active wildlife and the best chance of clear views of Denali peak."),
    ("Can I visit Denali in May?", "The park road typically opens fully by late May. Shoulder-season visits mean fewer crowds but cooler weather and less predictable wildlife activity."),
    ("Is September a good time?", "Yes. Fewer visitors, autumn colours and good wildlife viewing, though some services begin closing by mid-September."),
]


def content_best_time() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-8">Denali's visitor season aligns with Alaska's summer cruise window. Month choice affects wildlife activity, road access, crowd levels and your odds of seeing the mountain itself.</p>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">May</strong><p class="mt-2 text-gray-600">Park road opens progressively. Cooler temperatures, fewer visitors, bears emerging from dens. Denali peak visible roughly one third of days.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">June</strong><p class="mt-2 text-gray-600">Long daylight hours, calving season for caribou, wildflowers on tundra. Popular for pre-cruise land tours before peak July demand.</p></div>
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">July</strong><p class="mt-2 text-gray-600">Peak season. Warmest weather, busiest bookings, highest wildlife activity on park road. Reserve lodges and tours well ahead.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">August</strong><p class="mt-2 text-gray-600">Berry season brings bears to open areas. Still busy but slightly less crowded than July. Good post-cruise timing.</p></div>
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">September</strong><p class="mt-2 text-gray-600">Autumn colours, moose rut, fewer tour groups. Some facilities close mid-month. Cooler but often excellent wildlife viewing.</p></div>
  </div>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Denali Visibility</h2>
  <p class="text-gray-600 text-sm mb-8">The mountain is shrouded by clouds roughly two thirds of the time in summer. Flightseeing improves your odds dramatically because planes can fly above cloud layers. Ground tours still deliver outstanding wildlife and tundra scenery regardless.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Best Months for Cruise Passengers</h2>
  <p class="text-gray-600 text-sm mb-8">June and early September balance weather, availability and crowd levels. July and August suit travelers who prioritise maximum wildlife activity and accept peak-season pricing.</p>
  {faq_block(BEST_TIME_FAQ)}
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_wildlife_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Denali National Park is one of the best places in Alaska to see large mammals in their natural habitat. The park road traverses prime wildlife territory where animals are accustomed to — but never dependent on — human presence.</p>
    <h2 class="text-xl font-display font-bold text-gray-900 mb-3">The Denali Big Five</h2>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Moose:</strong> Common along rivers and willow thickets, especially in early morning and evening.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Caribou:</strong> Herds graze open tundra; calving peaks in late May and June.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Dall sheep:</strong> White coats visible on rocky slopes above the road, particularly near Polychrome Pass.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Wolves:</strong> Elusive but regularly spotted by patient observers on deep-park bus routes.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Grizzly bears:</strong> Foraging on tundra and berry patches; most active in July through September.</li>
    </ul>
    <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Seasonal Patterns</h2>
    <p class="text-gray-600 text-sm mb-4">Spring brings bears and migrating birds. Summer offers the highest overall sighting frequency. Autumn concentrates moose and bears near food sources before winter.</p>
    <a href="{u('denali-wildlife-tour')}" class="text-ocean-600 font-semibold text-sm">Wildlife tour guide →</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{IMG['wildlife'][0]}" alt="{IMG['wildlife'][1]}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip('Wildlife-focused land extension travelers', 'Big Five mammals plus golden eagles, ptarmigan and arctic ground squirrels', 'One full day minimum for a dedicated wildlife tour', 'Pairs well with a second day for flightseeing or hiking')}</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


def content_flightseeing_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">Flightseeing offers the most reliable way to see Denali peak and surrounding glaciers. Two main bases serve visitors: the park gateway area and Talkeetna, each with distinct advantages.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Park Gateway Flights</h2>
  <p class="text-gray-600 text-sm mb-6">Operators near the park entrance offer shorter flights with less transit time. Convenient when you are already staying in the Denali area and want to fit flightseeing into a packed itinerary.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Talkeetna Flights</h2>
  <p class="text-gray-600 text-sm mb-6">Talkeetna is the classic flightseeing hub, with more operators, glacier landing options and routes that circle the full massif. Worth a day trip from Denali or a stop on the Anchorage drive north.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Glacier Landings</h2>
  <p class="text-gray-600 text-sm mb-6">Some packages include a landing on a glacier or moraine field. These add time and cost but deliver an unforgettable on-ice experience with mountain views in every direction.</p>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8"><img src="/{IMG['flightseeing'][0]}" alt="{IMG['flightseeing'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <a href="{u('denali-flightseeing-tour')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Flightseeing tour guide →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_train_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">The Alaska Railroad Denali Star connects Anchorage, Talkeetna, Denali and Fairbanks on a scenic route through interior Alaska. For cruise passengers who prefer not to drive, rail is the classic way to reach the park.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Routes and Timing</h2>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Anchorage to Denali</strong><p class="mt-2 text-gray-600">Departs mid-morning, arrives early evening (~8 hours). Glass-dome cars available for panoramic views.</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Denali to Fairbanks</strong><p class="mt-2 text-gray-600">Continues north from Denali, arriving Fairbanks mid-afternoon (~4 hours).</p></div>
    <div class="bg-white rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">Talkeetna stop</strong><p class="mt-2 text-gray-600">Optional stop for flightseeing or an overnight in this historic mountaineering town.</p></div>
  </div>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Tips for Cruise Passengers</h2>
  <ul class="space-y-2 text-sm text-gray-600 mb-8">
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Book early for peak summer dates and dome-car seating.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Allow a full travel day — rail is slower than driving but far more scenic.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Coordinate luggage if you are connecting from a cruise port transfer.</li>
  </ul>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8"><img src="/{IMG['train'][0]}" alt="{IMG['train'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_planner() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Checklist your priorities, then match the right experiences on our <a href="{u('best-denali-excursions')}" class="text-ocean-600 font-semibold">best excursions page</a>.</p>
  <div class="planner-checklist space-y-3 mb-10">
    <label><input type="checkbox" /> I want maximum wildlife sightings</label>
    <label><input type="checkbox" /> Seeing Denali peak is my top priority</label>
    <label><input type="checkbox" /> I prefer an easy, low-walking option</label>
    <label><input type="checkbox" /> I need family-friendly activities</label>
    <label><input type="checkbox" /> I need transfer support from Anchorage or Fairbanks</label>
    <label><input type="checkbox" /> I want a pre- or post-cruise land extension</label>
    <label><input type="checkbox" /> I want an active adventure (ATV, rafting or zipline)</label>
    <label><input type="checkbox" /> I am travelling by Alaska Railroad</label>
  </div>
  {help_cta()}
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_enquire() -> str:
    return f"""<section class="pt-8 pb-16 bg-white"><div class="max-w-xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Tell us your cruise dates, travel hub and priorities and we will suggest the best Denali land tour options for your itinerary.</p>
  <form class="enquire-form" action="mailto:{ENQUIRY_EMAIL}" method="post" enctype="text/plain">
    <label for="name">Your name</label>
    <input id="name" name="name" type="text" required />
    <label for="email">Email</label>
    <input id="email" name="email" type="email" required />
    <label for="ship">Cruise ship and dates</label>
    <input id="ship" name="ship" type="text" placeholder="e.g. Ship name, sailing 15 July 2026" required />
    <label for="interest">Interested in</label>
    <select id="interest" name="interest">
      <option>Denali National Park Tour</option>
      <option>Denali Wildlife Tour</option>
      <option>Tundra Wilderness Tour</option>
      <option>Denali Flightseeing Tour</option>
      <option>Denali ATV Tour</option>
      <option>Denali River Rafting</option>
      <option>Denali Zipline Adventure</option>
      <option>Hiking &amp; Nature Walk</option>
      <option>Anchorage to Denali Transfer with Sightseeing</option>
      <option>Fairbanks to Denali Transfer with Sightseeing</option>
      <option>Not sure, help me choose</option>
    </select>
    <label for="message">Message</label>
    <textarea id="message" name="message" rows="4" placeholder="Group size, mobility needs, pre/post-cruise timing..."></textarea>
    <button type="submit" class="btn-ocean w-full text-white font-semibold py-3 rounded-full">Send enquiry</button>
  </form>
  <p class="text-xs text-gray-400 text-center mt-6">We respond within 1-2 business days. Not affiliated with any cruise line.</p>
</div></section>"""


FAQ_QA = [
    ("Is Denali a cruise port?", "No. Denali is an interior land destination. Cruise passengers visit as a pre- or post-cruise extension from Anchorage, Fairbanks or an Alaska embarkation port."),
    ("How many days should I spend in Denali?", "Two to four nights works well. Allow one full day for a park tour and add days for flightseeing, rafting or a second guided activity."),
    ("What is the best way to get to Denali from Anchorage?", "Drive (4-5 hours), motorcoach, Alaska Railroad or a transfer-with-sightseeing package. Rail is the most scenic; driving offers the most flexibility."),
    ("When is the best time to visit?", "June through early September for full park road access and active wildlife. June and September offer lighter crowds than peak July."),
    ("Can I see Denali peak from the ground?", "Sometimes, on clear days. The mountain is visible roughly one third of summer days. Flightseeing dramatically improves your odds."),
    ("Should I book tours independently or through my cruise line?", "Independent booking usually offers more choice and better value. Cruise line packages simplify logistics but cost more and limit flexibility."),
]


def content_faq() -> str:
    return f"""<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{land_tour_snapshot(best_for='Quick planning answers for Denali land tours')}</div></section>
{faq_block(FAQ_QA)}
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


EXCURSIONS = [
    {
        "slug": "denali-national-park-tour",
        "label": "Denali National Park Tour",
        "hero_title": f"Denali National<br/><span class=\"{ACCENT}\">Park Tour</span>",
        "hero_lead": "The essential bus tour along Denali's park road for wildlife, tundra scenery and Alaska Range views.",
        "image": "national_park_tour",
        "intro": "This is the cornerstone Denali experience: a narrated bus journey deep into the park where private vehicles cannot go. Naturalist guides share ecology, geology and wildlife spotting tips while you traverse river valleys and high tundra passes.",
        "bullets": [
            "Access to the restricted park road beyond Mile 15",
            "Regular wildlife sightings of moose, caribou, Dall sheep and bears",
            "Multiple tour depths from shorter turnaround trips to Eielson Visitor Center",
            "Ideal first-day activity for any Denali land extension",
        ],
        "duration": "6-8 hours depending on turnaround point",
        "fitness": "Easy — seated bus touring with optional short walks at stops",
        "wildlife": "Moose, caribou, Dall sheep, grizzly bears and wolves on most routes",
        "scenic_highlights": "Polychrome Pass, Toklat River, Eielson Visitor Center and Alaska Range panoramas",
        "best_for": "First-time Denali visitors wanting the complete park introduction",
        "hub_connection": "Anchorage or Fairbanks with overnight at park gateway",
        "pre_post": "Core pre/post-cruise activity — plan one full day",
        "typical_time": "One full day plus travel days on each end",
        "faq": [
            ("How far does the bus go?", "Options range from shorter turnaround trips to Eielson Visitor Center at Mile 66. Deeper routes require lottery permits."),
            ("Will I see wildlife?", "Wildlife is never guaranteed, but this route offers among the best odds in Alaska."),
            ("What should I bring?", "Layers, rain jacket, binoculars, snacks and a camera with zoom lens."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"popular": "Top-booked Denali experience for cruise land extensions"},
    },
    {
        "slug": "denali-wildlife-tour",
        "label": "Denali Wildlife Tour",
        "hero_title": f"Denali<br/><span class=\"{ACCENT}\">Wildlife Tour</span>",
        "hero_lead": "Wildlife-focused guided tour along proven sighting routes in Denali National Park.",
        "image": "wildlife_tour",
        "intro": "While all park bus tours offer wildlife potential, dedicated wildlife tours prioritise routes and timing known for mammal activity. Guides carry spotting scopes and coordinate with other drivers to share sightings.",
        "bullets": [
            "Expert guides trained in animal behaviour and park ecology",
            "Routes selected for current wildlife activity patterns",
            "Spotting scopes and binoculars often provided",
            "Smaller groups on some premium departures",
        ],
        "duration": "4-6 hours",
        "fitness": "Easy — mostly seated with brief stops",
        "wildlife": "Focused on the Big Five: moose, caribou, Dall sheep, wolves and grizzly bears",
        "scenic_highlights": "Open tundra, river corridors and mountain backdrops",
        "best_for": "Travelers whose primary goal is wildlife photography and observation",
        "hub_connection": "Anchorage or Fairbanks with 2+ nights at park gateway",
        "pre_post": "Excellent standalone day or paired with flightseeing",
        "typical_time": "One full day",
        "faq": [
            ("How is this different from a standard park tour?", "Wildlife tours use routes and timing optimised for animal sightings rather than maximum distance."),
            ("What is the best season?", "June through September. July and August typically offer the highest activity."),
            ("Can children join?", "Yes, though patience is needed during quiet stretches between sightings."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"best_for": "Wildlife-first travelers on a land extension"},
    },
    {
        "slug": "denali-tundra-wilderness-tour",
        "label": "Tundra Wilderness Tour",
        "hero_title": f"Tundra<br/><span class=\"{ACCENT}\">Wilderness Tour</span>",
        "hero_lead": "Explore Denali's open subarctic tundra and alpine landscapes on a guided wilderness experience.",
        "image": "tundra_tour",
        "intro": "The tundra wilderness tour immerses you in Denali's signature landscape: vast open plains, braided rivers and the Alaska Range rising above tree line. It combines scenic grandeur with wildlife opportunities in a slightly more adventurous format.",
        "bullets": [
            "Experience Denali's iconic treeless tundra ecosystem",
            "Opportunities for short guided walks at scenic stops",
            "Strong photography potential in changing light conditions",
            "Less crowded than peak-season deep-park departures",
        ],
        "duration": "4-5 hours",
        "fitness": "Easy to moderate — optional short walks on uneven ground",
        "wildlife": "Caribou, Dall sheep, ground squirrels and raptors common on tundra",
        "scenic_highlights": "Expansive tundra vistas, braided glacial rivers and alpine ridges",
        "best_for": "Guests wanting landscape immersion beyond a standard bus tour",
        "hub_connection": "Anchorage or Fairbanks",
        "pre_post": "Good second-day option after a park road tour",
        "typical_time": "Half to full day",
        "faq": [
            ("Is there hiking involved?", "Most tours include optional short walks. Check your specific itinerary for distance."),
            ("What is the tundra like?", "Treeless subarctic plain with low shrubs, wildflowers in summer and permafrost beneath."),
            ("When is best for wildflowers?", "Late June through July for peak tundra wildflower displays."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"activity_level": "Easy to moderate with optional walking"},
    },
    {
        "slug": "denali-flightseeing-tour",
        "label": "Denali Flightseeing Tour",
        "hero_title": f"Denali<br/><span class=\"{ACCENT}\">Flightseeing</span>",
        "hero_lead": "Aerial views of Denali peak, glaciers and the Alaska Range from a small aircraft.",
        "image": "flightseeing_tour",
        "intro": "When clouds hide the mountain from the ground, flightseeing is your best bet. Small planes depart from the park gateway area and Talkeetna, circling the massif and offering perspectives impossible from any road or trail.",
        "bullets": [
            "Best odds of seeing Denali peak and surrounding glaciers",
            "Routes circle the mountain for views from all angles",
            "Glacier landing options available on premium packages",
            "Fits into a half-day window alongside other activities",
        ],
        "duration": "1.5-3 hours depending on route and landings",
        "fitness": "Easy — seated in small aircraft",
        "wildlife": "Occasional mountain goat and caribou sightings from the air",
        "scenic_highlights": "Denali summit, Ruth Glacier, Great Gorge and surrounding ice fields",
        "best_for": "Travelers prioritising mountain views and willing to invest in weather-dependent activity",
        "hub_connection": "Anchorage, Fairbanks or park gateway; Talkeetna for premium routes",
        "pre_post": "Ideal second-day add-on for any land extension",
        "typical_time": "Half day including briefing and transport",
        "faq": [
            ("What if weather is bad?", "Operators cancel or reroute when conditions are unsafe. Build flexibility into your schedule."),
            ("Are glacier landings worth it?", "If budget allows, landing on ice with mountain views all around is a highlight of many Alaska trips."),
            ("Will I get airsick?", "Flights are generally smooth, but sensitive travelers should take precautions."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"best_for": "Mountain views when ground visibility is limited"},
    },
    {
        "slug": "denali-atv-tour",
        "label": "Denali ATV Tour",
        "hero_title": f"Denali<br/><span class=\"{ACCENT}\">ATV Tour</span>",
        "hero_lead": "Off-road adventure through boreal forest and mountain trails near Denali National Park.",
        "image": "atv_tour",
        "intro": "ATV tours offer an active alternative to bus-based sightseeing. Guided convoys follow established trails through spruce forest and open ridges with mountain views, delivering adrenaline alongside Alaska scenery.",
        "bullets": [
            "No prior ATV experience needed — full instruction provided",
            "Helmets, gear and safety briefing included",
            "Mountain and forest scenery beyond the park road corridor",
            "Good option for active travelers wanting variety",
        ],
        "duration": "2-3 hours",
        "fitness": "Moderate — active riding, gripping handlebars over varied terrain",
        "wildlife": "Occasional moose and spruce grouse along forest trails",
        "scenic_highlights": "Boreal forest, ridge viewpoints and Alaska Range glimpses",
        "best_for": "Active travelers and groups wanting an adventure break from bus tours",
        "hub_connection": "Anchorage or Fairbanks with park gateway overnight",
        "pre_post": "Best as a second or third day activity",
        "typical_time": "Half day including gear-up",
        "faq": [
            ("Do I need a driving licence?", "Requirements vary by operator; most accept standard licences with minimum age limits."),
            ("What should I wear?", "Closed-toe shoes, long pants and layers. Operators provide helmets and often gloves."),
            ("Can two people share one ATV?", "Some tours offer double machines; confirm when booking."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"activity_level": "Moderate — most active standard tour option"},
    },
    {
        "slug": "denali-rafting-tour",
        "label": "Denali River Rafting",
        "hero_title": f"Denali<br/><span class=\"{ACCENT}\">River Rafting</span>",
        "hero_lead": "Scenic float or whitewater rafting on rivers near Denali National Park.",
        "image": "rafting_tour",
        "intro": "Denali-area rivers range from gentle scenic floats suitable for all ages to moderate whitewater for adventurous groups. Rafting adds a water-based perspective on the landscape and works well as a second-day activity.",
        "bullets": [
            "Scenic float and whitewater options available",
            "Professional guides handle paddling and safety",
            "Dry suits or splash gear provided on most trips",
            "River corridors offer different scenery from the park road",
        ],
        "duration": "2-4 hours on water plus transport",
        "fitness": "Easy (scenic float) to moderate (whitewater)",
        "wildlife": "Waterfowl, beaver, moose along riverbanks",
        "scenic_highlights": "Glacial rivers, forested canyons and mountain views from the water",
        "best_for": "Families (scenic float) or active groups (whitewater)",
        "hub_connection": "Anchorage or Fairbanks",
        "pre_post": "Popular second-day activity on a 3+ night itinerary",
        "typical_time": "Half day",
        "faq": [
            ("Is rafting safe for children?", "Scenic floats welcome younger guests; whitewater has age and size minimums."),
            ("Will I get wet?", "On scenic floats, usually minimally. Whitewater trips expect splashing — dress accordingly."),
            ("When does rafting season run?", "Typically June through August when river levels and weather are suitable."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"popular": "Top adventure add-on for multi-day land extensions"},
    },
    {
        "slug": "denali-zipline-tour",
        "label": "Denali Zipline Adventure",
        "hero_title": f"Denali<br/><span class=\"{ACCENT}\">Zipline</span>",
        "hero_lead": "Canopy zipline course with forest and mountain views near the Denali park area.",
        "image": "zipline_tour",
        "intro": "The Denali zipline course combines adrenaline with boreal forest scenery. Multiple lines of varying length and height let you progress at a comfortable pace with professional guides managing safety at every platform.",
        "bullets": [
            "Multiple ziplines with increasing length and height",
            "Full safety harness and guide supervision throughout",
            "Forest canopy and mountain peek-a-boo views",
            "Compact time commitment for packed itineraries",
        ],
        "duration": "2-3 hours including briefing",
        "fitness": "Moderate — short hikes between platforms, gripping harness",
        "wildlife": "Forest birds and occasional squirrel sightings",
        "scenic_highlights": "Boreal forest canopy and Alaska Range views from platforms",
        "best_for": "Adventure seekers and families with older children",
        "hub_connection": "Anchorage or Fairbanks",
        "pre_post": "Fits well as an afternoon activity after a morning tour",
        "typical_time": "Half day",
        "faq": [
            ("Is there a weight limit?", "Most courses have minimum and maximum weight requirements for safety."),
            ("What if I am afraid of heights?", "Guides are experienced with nervous guests, but this activity requires comfort with elevation."),
            ("What is the minimum age?", "Typically 10-12 years depending on operator; confirm when booking."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"best_for": "Adventure-focused groups wanting a compact thrill"},
    },
    {
        "slug": "denali-hiking-nature-walk",
        "label": "Hiking & Nature Walk",
        "hero_title": f"Hiking &amp;<br/><span class=\"{ACCENT}\">Nature Walk</span>",
        "hero_lead": "Guided hiking and nature walks on trails in and around Denali National Park.",
        "image": "hiking_tour",
        "intro": "Guided hikes offer a slower, closer look at Denali's ecology than bus tours allow. Naturalist guides identify plants, tracks and birds while leading manageable trails suited to your group's fitness level.",
        "bullets": [
            "Trails matched to group fitness from easy nature walks to moderate hikes",
            "Naturalist interpretation of flora, fauna and geology",
            "Smaller group sizes than bus tours",
            "Off-trail bus experience — intimate ground-level perspective",
        ],
        "duration": "3-5 hours depending on trail",
        "fitness": "Moderate — sustained walking on uneven, sometimes muddy terrain",
        "wildlife": "Track and sign interpretation; occasional direct sightings of smaller mammals and birds",
        "scenic_highlights": "Trail-level tundra, taiga forest and river valley views",
        "best_for": "Active travelers who want exercise and education combined",
        "hub_connection": "Anchorage or Fairbanks with park gateway stay",
        "pre_post": "Best on a second or third day when you have energy for walking",
        "typical_time": "Half to full day",
        "faq": [
            ("What footwear do I need?", "Sturdy waterproof hiking boots are strongly recommended."),
            ("How strenuous are the trails?", "Options range from easy nature walks (2-3 km) to moderate hikes with elevation gain."),
            ("Are hiking poles available?", "Some operators provide poles; bring your own if you use them regularly."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"activity_level": "Moderate — most walking-intensive standard option"},
    },
    {
        "slug": "anchorage-to-denali-transfer-with-sightseeing",
        "label": "Anchorage Transfer with Sightseeing",
        "hero_title": f"Anchorage to Denali<br/><span class=\"{ACCENT}\">Transfer</span>",
        "hero_lead": "Scenic one-way transfer from Anchorage to Denali with curated stops along the Parks Highway.",
        "image": "anchorage_transfer",
        "intro": "Turn your travel day into part of the adventure. This transfer combines Anchorage-to-Denali transport with scenic stops, narration and photo opportunities so you arrive having already experienced Alaska interior highlights.",
        "bullets": [
            "Eliminates the need to drive an unfamiliar rental car",
            "Curated stops at viewpoints, rivers and towns en route",
            "Luggage handling and hotel drop-off at Denali",
            "Ideal first day of a pre-cruise land extension from Anchorage",
        ],
        "duration": "7-9 hours including stops",
        "fitness": "Easy — vehicle-based with short stops",
        "wildlife": "Occasional moose and eagle sightings from roadside stops",
        "scenic_highlights": "Matanuska Valley, Talkeetna views and Alaska Range approach",
        "best_for": "Cruise passengers flying into Anchorage before their land extension",
        "hub_connection": "Anchorage departure to Denali park gateway",
        "pre_post": "Primary use case is pre-cruise land tour transport",
        "typical_time": "One full travel day",
        "faq": [
            ("Can I bring luggage?", "Yes — transfer products are designed for travelers with bags."),
            ("Are meals included?", "Some packages include a lunch stop; confirm inclusions when booking."),
            ("Can I stop in Talkeetna?", "Some transfers offer optional Talkeetna stops or connections."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"pre_post": "Top pre-cruise logistics product from Anchorage"},
    },
    {
        "slug": "fairbanks-to-denali-transfer-with-sightseeing",
        "label": "Fairbanks Transfer with Sightseeing",
        "hero_title": f"Fairbanks to Denali<br/><span class=\"{ACCENT}\">Transfer</span>",
        "hero_lead": "Scenic transfer from Fairbanks to Denali with guided stops through interior Alaska.",
        "image": "fairbanks_transfer",
        "intro": "For post-cruise travelers heading south from Fairbanks, this transfer delivers efficient transport with scenic and cultural stops along the shorter Parks Highway section between Fairbanks and the park entrance.",
        "bullets": [
            "Shorter route than Anchorage transfer — more time for stops",
            "Ideal for post-cruise routing toward Denali",
            "Luggage handling and park-area hotel drop-off",
            "Narration on interior Alaska history and ecology",
        ],
        "duration": "3-5 hours including stops",
        "fitness": "Easy — vehicle-based touring",
        "wildlife": "Occasional moose along river corridors",
        "scenic_highlights": "Nenana River, Alaska Range views and interior valleys",
        "best_for": "Post-cruise travelers ending their trip via Fairbanks airport",
        "hub_connection": "Fairbanks departure to Denali park gateway",
        "pre_post": "Primary use case is post-cruise land tour transport",
        "typical_time": "Half to full travel day",
        "faq": [
            ("How does this compare to the Anchorage transfer?", "Shorter distance means less travel time and more flexibility for stops."),
            ("Can I connect to a park tour the same day?", "Possible with early departures, but an overnight before touring is recommended."),
            ("Is hotel pickup included in Fairbanks?", "Most operators offer Fairbanks hotel or airport pickup."),
        ],
        "cta": "Enquire about this tour →",
        "land_tour_snapshot": {"pre_post": "Top post-cruise logistics product from Fairbanks"},
    },
]


EXC_NAV = {ex["slug"]: ex["label"] for ex in EXCURSIONS}


def content_map() -> dict[str, str]:
    return {
        "home.html": content_home(),
        "best-denali-excursions.html": content_best(),
        "denali-national-park-guide.html": content_park_guide(),
        "denali-for-cruise-passengers.html": content_cruise_passengers(),
        "anchorage-to-denali-guide.html": content_anchorage_guide(),
        "fairbanks-to-denali-guide.html": content_fairbanks_guide(),
        "best-time-to-visit-denali.html": content_best_time(),
        "denali-wildlife-guide.html": content_wildlife_guide(),
        "denali-flightseeing-guide.html": content_flightseeing_guide(),
        "denali-train-guide.html": content_train_guide(),
        "denali-cruise-tour-planner.html": content_planner(),
        "denali-faq.html": content_faq(),
        "enquire.html": content_enquire(),
    }


def heroes() -> dict[str, str]:
    return {
        "home": hero(
            "Denali National Park · Alaska Interior",
            f"Denali Excursions &amp;<br/><span class=\"{ACCENT}\">Alaska Cruise Land Tour Planning</span>",
            "Plan Denali National Park tours, wildlife experiences, flightseeing and pre- or post-cruise Alaska adventures with guidance built around cruise passengers.",
            "home",
            cta=("best-denali-excursions", "Compare Excursions"),
            tags=["National Park Tours", "Wildlife", "Flightseeing", "Pre/Post-Cruise"],
            section_class="site-hero site-hero--denali",
            bg_class="hero-bg-custom hero-bg-denali",
        ),
        "best": hero("Independent Guide", f"Best Denali<br/><span class=\"{ACCENT}\">Excursions</span>", "Compare 10 Denali land tours by duration, fitness, wildlife payoff and pre/post-cruise suitability.", "best", breadcrumb="Best Excursions", cta=("enquire", "Need help choosing? →")),
        "park": hero("National Park Guide", f"Denali National<br/><span class=\"{ACCENT}\">Park Guide</span>", "Park road access, wildlife expectations and practical planning for your Denali visit.", "park", breadcrumb="Park Guide"),
        "cruise": hero("Cruise Passenger Guide", f"Denali for<br/><span class=\"{ACCENT}\">Cruise Passengers</span>", "How to add Denali as a pre- or post-cruise land extension with realistic days and routing.", "cruise", breadcrumb="Cruise Passengers"),
        "anchorage": hero("Route Guide", f"Anchorage to<br/><span class=\"{ACCENT}\">Denali Guide</span>", "Drive, rail, coach and transfer options north from Anchorage to Denali National Park.", "anchorage", breadcrumb="Anchorage Route"),
        "fairbanks": hero("Route Guide", f"Fairbanks to<br/><span class=\"{ACCENT}\">Denali Guide</span>", "Travel options south from Fairbanks to Denali for post-cruise land extensions.", "fairbanks", breadcrumb="Fairbanks Route"),
        "best_time": hero("Seasonal Planning", f"Best Time To Visit<br/><span class=\"{ACCENT}\">Denali</span>", "Month-by-month tradeoffs for wildlife, weather, road access and Denali visibility.", "best_time", breadcrumb="Best Time To Visit"),
        "wildlife": hero("Wildlife Planning", f"Denali<br/><span class=\"{ACCENT}\">Wildlife Guide</span>", "The Big Five, seasonal patterns and which tours maximise wildlife opportunities.", "wildlife", breadcrumb="Wildlife Guide"),
        "flightseeing": hero("Aerial Adventures", f"Denali<br/><span class=\"{ACCENT}\">Flightseeing Guide</span>", "Talkeetna vs park gateway flights, glacier landings and weather planning.", "flightseeing", breadcrumb="Flightseeing Guide"),
        "train": hero("Rail Travel", f"Denali<br/><span class=\"{ACCENT}\">Train Guide</span>", "Alaska Railroad Denali Star routes, timing and tips for cruise passengers.", "train", breadcrumb="Train Guide"),
        "planner": hero("Plan Your Trip", f"Denali<br/><span class=\"{ACCENT}\">Tour Planner</span>", "Checklist your priorities and build the right Denali land extension in minutes.", "planner", breadcrumb="Tour Planner"),
        "faq": hero("Planning Answers", f"Denali<br/><span class=\"{ACCENT}\">FAQ</span>", "Quick answers to timing, wildlife, transport and booking questions.", "faq", breadcrumb="FAQ"),
        "enquire": hero("Book and Enquire", f"Enquire About<br/><span class=\"{ACCENT}\">Denali Tours</span>", "Tell us your cruise timing and we'll recommend best-fit Denali land tour options.", "enquire", breadcrumb="Enquire"),
    }


def pages_meta() -> list[dict]:
    return [
        dict(slug="", file_content="home.html", title=f"{SITE} | Denali National Park Tours & Cruise Land Extensions", description="Plan Denali excursions and Alaska cruise land tours with independent comparisons across national park tours, wildlife, flightseeing and pre/post-cruise transfers.", keywords="Denali excursions, Denali National Park tours, Alaska cruise land tour Denali", data_page="home", hero="partials/hero-home.html", preload=IMG["home"][0], extra_schema=[{"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/"}]),
        dict(slug="best-denali-excursions", file_content="best-denali-excursions.html", title="Best Denali Excursions | Compare 10 Land Tour Options", description="Compare the best Denali excursions by timing, activity level, wildlife focus and pre/post-cruise suitability.", keywords="best Denali excursions, Denali land tours, Denali excursion comparison", data_page="excursions", hero="partials/hero-best.html", preload=IMG["best"][0]),
        dict(slug="denali-national-park-guide", file_content="denali-national-park-guide.html", title="Denali National Park Guide | Planning for Cruise Passengers", description="Denali National Park guide with park road access, wildlife expectations and booking tips for land tour travelers.", keywords="Denali National Park guide, Denali park road tour, Denali planning", data_page="park", hero="partials/hero-park.html", preload=IMG["park"][0]),
        dict(slug="denali-for-cruise-passengers", file_content="denali-for-cruise-passengers.html", title="Denali for Cruise Passengers | Pre & Post-Cruise Land Extension", description="Complete guide to adding Denali to your Alaska cruise: days needed, routing from Anchorage and Fairbanks, cruise line vs independent booking.", keywords="Denali cruise passengers, Denali pre cruise, Denali post cruise land tour", data_page="cruise", hero="partials/hero-cruise.html", preload=IMG["cruise"][0], extra_schema=[faq_schema(CRUISE_FAQ)]),
        dict(slug="anchorage-to-denali-guide", file_content="anchorage-to-denali-guide.html", title="Anchorage to Denali Guide | Drive, Rail & Transfer Options", description="How to travel from Anchorage to Denali by car, coach, Alaska Railroad or sightseeing transfer with scenic stops and sample itineraries.", keywords="Anchorage to Denali, Anchorage Denali transfer, Parks Highway Denali", data_page="guides", hero="partials/hero-anchorage.html", preload=IMG["anchorage"][0]),
        dict(slug="fairbanks-to-denali-guide", file_content="fairbanks-to-denali-guide.html", title="Fairbanks to Denali Guide | Post-Cruise Travel Options", description="Travel from Fairbanks to Denali by road, rail or transfer for post-cruise Alaska land extensions.", keywords="Fairbanks to Denali, Fairbanks Denali transfer, post cruise Denali", data_page="guides", hero="partials/hero-fairbanks.html", preload=IMG["fairbanks"][0]),
        dict(slug="best-time-to-visit-denali", file_content="best-time-to-visit-denali.html", title="Best Time to Visit Denali | Month-by-Month Guide", description="Best time to visit Denali by month, including wildlife, weather, road access, Denali visibility and cruise passenger timing.", keywords="best time to visit Denali, Denali season guide, Denali weather months", data_page="park", hero="partials/hero-best_time.html", preload=IMG["best_time"][0], extra_schema=[faq_schema(BEST_TIME_FAQ)]),
        dict(slug="denali-wildlife-guide", file_content="denali-wildlife-guide.html", title="Denali Wildlife Guide | Big Five & Seasonal Viewing", description="Denali wildlife guide covering the Big Five mammals, seasonal patterns and best tours for wildlife-focused travelers.", keywords="Denali wildlife guide, Denali Big Five, Denali wildlife tour", data_page="wildlife", hero="partials/hero-wildlife.html", preload=IMG["wildlife"][0]),
        dict(slug="denali-flightseeing-guide", file_content="denali-flightseeing-guide.html", title="Denali Flightseeing Guide | Talkeetna vs Park Gateway", description="Guide to Denali flightseeing options including Talkeetna vs park gateway departures and glacier landing packages.", keywords="Denali flightseeing guide, Denali glacier landing, Talkeetna flightseeing", data_page="park", hero="partials/hero-flightseeing.html", preload=IMG["flightseeing"][0]),
        dict(slug="denali-train-guide", file_content="denali-train-guide.html", title="Denali Train Guide | Alaska Railroad Denali Star", description="Alaska Railroad Denali Star guide with routes, timing and tips for cruise passengers traveling by rail.", keywords="Denali train guide, Alaska Railroad Denali Star, Denali rail travel", data_page="guides", hero="partials/hero-train.html", preload=IMG["train"][0]),
        dict(slug="denali-cruise-tour-planner", file_content="denali-cruise-tour-planner.html", title="Denali Cruise Tour Planner | Build Your Land Extension", description="Interactive Denali land tour planner checklist to match excursions with your cruise travel priorities.", keywords="Denali tour planner, Denali cruise land extension planner", data_page="cruise", hero="partials/hero-planner.html", preload=IMG["planner"][0], trust=False),
        dict(slug="denali-faq", file_content="denali-faq.html", title="Denali Excursions FAQ | Land Tour Planning Answers", description="Denali excursion FAQ with practical answers about timing, wildlife, transport, visibility and independent booking.", keywords="Denali excursions FAQ, Denali land tour questions", data_page="faq", hero="partials/hero-faq.html", preload=IMG["faq"][0], extra_schema=[faq_schema(FAQ_QA)]),
        dict(slug="enquire", file_content="enquire.html", title="Enquire | Denali Shore Excursions", description="Enquire about Denali excursions and land tours and get recommendations matched to your cruise itinerary.", keywords="enquire Denali excursions, Denali tour advice", data_page="excursions", hero="partials/hero-enquire.html", preload=IMG["enquire"][0], trust=False),
    ]


def main() -> None:
    print(f"Building {SITE} site...")

    write("partials/nav.html", f"""<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-alpine-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C8 2 4 5 4 9c0 5 4 9 8 13 4-4 8-8 8-13 0-4-4-7-8-7z"/></svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Denali<br/><span class="text-[10px] font-body font-normal text-teal-600 tracking-widest uppercase">Shore Excursions</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-4 text-sm font-medium">
        <a href="/" data-nav="home" class="text-gray-600 hover:text-ocean-600 transition-colors">Home</a>
        <a href="{u('best-denali-excursions')}" data-nav="excursions" class="text-gray-600 hover:text-ocean-600 transition-colors">Excursions</a>
        <a href="{u('denali-for-cruise-passengers')}" data-nav="cruise" class="text-gray-600 hover:text-ocean-600 transition-colors">Cruise Passengers</a>
        <a href="{u('denali-national-park-guide')}" data-nav="park" class="text-gray-600 hover:text-ocean-600 transition-colors">Park Guide</a>
        <a href="{u('denali-wildlife-guide')}" data-nav="wildlife" class="text-gray-600 hover:text-ocean-600 transition-colors">Wildlife</a>
        <a href="{u('anchorage-to-denali-guide')}" data-nav="guides" class="text-gray-600 hover:text-ocean-600 transition-colors">Guides</a>
        <a href="{u('denali-faq')}" data-nav="faq" class="text-gray-600 hover:text-ocean-600 transition-colors">FAQ</a>
      </div>
      <a href="{u('enquire')}" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">Enquire</a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>""")

    exc_links = "".join(
        f'<li><a href="{u(s)}" class="hover:text-white transition-colors">{lbl}</a></li>'
        for s, lbl in EXC_NAV.items()
    )
    write("partials/footer.html", f"""<footer class="bg-gray-900 text-gray-400 py-14">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
      <div class="sm:col-span-2 lg:col-span-1">
        <a href="/" class="font-display font-semibold text-white text-lg">{SITE}</a>
        <p class="mt-3 text-sm leading-relaxed">Independent planning guide for Alaska cruise land tours and Denali National Park excursions. Focused on pre- and post-cruise land extension planning.</p>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="{u('best-denali-excursions')}" class="hover:text-white transition-colors">All Excursions</a></li>
          {exc_links}
        </ul>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Resources</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="{u('denali-for-cruise-passengers')}" class="hover:text-white transition-colors">Cruise Passengers</a></li>
          <li><a href="{u('denali-national-park-guide')}" class="hover:text-white transition-colors">Park Guide</a></li>
          <li><a href="{u('anchorage-to-denali-guide')}" class="hover:text-white transition-colors">Anchorage to Denali</a></li>
          <li><a href="{u('fairbanks-to-denali-guide')}" class="hover:text-white transition-colors">Fairbanks to Denali</a></li>
          <li><a href="{u('denali-wildlife-guide')}" class="hover:text-white transition-colors">Wildlife Guide</a></li>
          <li><a href="{u('denali-flightseeing-guide')}" class="hover:text-white transition-colors">Flightseeing Guide</a></li>
          <li><a href="{u('denali-train-guide')}" class="hover:text-white transition-colors">Train Guide</a></li>
          <li><a href="{u('best-time-to-visit-denali')}" class="hover:text-white transition-colors">Best Time To Visit</a></li>
          <li><a href="{u('denali-cruise-tour-planner')}" class="hover:text-white transition-colors">Tour Planner</a></li>
          <li><a href="{u('denali-faq')}" class="hover:text-white transition-colors">FAQ</a></li>
          <li><a href="{u('enquire')}" class="hover:text-white transition-colors">Enquire</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
      <p>&copy; 2026 {SITE}. Verify timings and prices directly before booking.</p>
    </div>
  </div>
</footer>""")

    write("partials/trust-strip.html", """<section class="trust-strip" aria-label="Denali excursion highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Denali National Park</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Wildlife Viewing</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Flightseeing</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Pre/Post-Cruise Planning</li>
    </ul>
  </div>
</section>""")

    for key, html in heroes().items():
        write(f"partials/hero-{key}.html", html)

    for ex in EXCURSIONS:
        write(
            f"partials/hero-{ex['slug']}.html",
            hero(
                "Denali Land Tour",
                ex["hero_title"],
                ex["hero_lead"],
                ex["image"],
                breadcrumb=ex["label"],
                cta=("enquire", "Enquire about this tour →"),
            ),
        )
        write(f"content/{ex['slug']}.html", excursion_page(ex))

    for name, html in content_map().items():
        write(f"content/{name}", html)

    pages = pages_meta()
    for ex in EXCURSIONS:
        pages.append(
            dict(
                slug=ex["slug"],
                file_content=f"{ex['slug']}.html",
                title=f"{ex['label']} | Denali Shore Excursion Guide",
                description=ex["intro"].split(". ")[0].rstrip(".") + ".",
                keywords=f"Denali {ex['slug'].replace('-', ' ')}, Denali land tour, Alaska cruise extension",
                data_page="excursions",
                hero=f"partials/hero-{ex['slug']}.html",
                preload=IMG[ex["image"]][0],
                extra_schema=[faq_schema(ex["faq"])],
            )
        )

    for p in pages:
        slug = p["slug"]
        name = p["title"].split("|")[0].strip()
        schemas = [breadcrumb_schema(slug, name)] + p.get("extra_schema", [])
        html = page_shell(
            title=p["title"],
            description=p["description"],
            keywords=p["keywords"],
            slug=slug,
            data_page=p["data_page"],
            hero=p["hero"],
            content=p["file_content"],
            preload=p["preload"],
            trust=p.get("trust", True),
        )
        write_page(slug, inject_schemas(html, schemas))

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    priorities = {
        "": "1.0",
        "best-denali-excursions": "0.9",
        "denali-for-cruise-passengers": "0.9",
        "anchorage-to-denali-guide": "0.8",
    }
    for slug in [p["slug"] for p in pages]:
        loc = f"{DOMAIN}/" if not slug else f"{DOMAIN}/{slug}"
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{DATE}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            f"    <priority>{priorities.get(slug, '0.7')}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")

    write("package.json", '{\n  "name": "denali-shore-excursions",\n  "private": true,\n  "scripts": {\n    "build": "python3 scripts/build-denali-site.py",\n    "deploy": "wrangler deploy",\n    "preview": "python3 -m http.server 8904"\n  },\n  "devDependencies": {\n    "wrangler": "^4.94.0"\n  }\n}\n')
    write("wrangler.jsonc", '{\n  "$schema": "node_modules/wrangler/config-schema.json",\n  "name": "denali-shore-excursions",\n  "compatibility_date": "2026-06-24",\n  "observability": { "enabled": true },\n  "assets": {\n    "directory": ".",\n    "html_handling": "auto-trailing-slash"\n  },\n  "routes": [\n    {\n      "pattern": "denalishoreexcursions.com",\n      "custom_domain": true\n    }\n  ]\n}\n')
    write("deploy.sh", f"#!/bin/bash\nset -euo pipefail\ncd \"$(dirname \"$0\")\"\nif [[ ! -f node_modules/.bin/wrangler ]]; then npm install; fi\necho \"Deploying {SITE} to Cloudflare...\"\nnpx wrangler deploy\necho \"Done. Check {DOMAIN}/ shortly.\"\n")
    (ROOT / "deploy.sh").chmod(0o755)
    write("images/ATTRIBUTION.md", "# Image attribution\n\nLocal Alaska photography assets for Denali Shore Excursions.\n")
    print("Done.")


if __name__ == "__main__":
    main()
