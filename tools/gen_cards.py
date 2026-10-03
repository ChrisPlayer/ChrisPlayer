"""Genere les cartes de projets du profil (assets/card-*.svg), dans le style sobre de la banniere.
Relancer apres modification : python tools/gen_cards.py
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
W, H = 460, 150
BG, BORDER, CREAM, MUTED, AMBER = "#1e1c21", "#3a3530", "#d9d1c4", "#9d958a", "#b9a477"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "Consolas, 'Cascadia Mono', 'Courier New', monospace"

ICON_BOITE = f'''<g transform="translate(28 34)">
  <rect width="62" height="50" rx="8" fill="none" stroke="{AMBER}" stroke-width="2"/>
  <line x1="0" y1="13" x2="62" y2="13" stroke="{AMBER}" stroke-width="2"/>
  <g fill="{AMBER}"><circle cx="8" cy="6.5" r="2"/><circle cx="15" cy="6.5" r="2"/><circle cx="22" cy="6.5" r="2"/></g>
  <path d="M10 23 l8 6 l-8 6" fill="none" stroke="{CREAM}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="23" y="33" width="12" height="3" fill="{CREAM}">
    <animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
  </rect>
</g>'''

ICON_SKIN = f'''<g transform="translate(28 34)">
  <rect width="62" height="50" rx="8" fill="none" stroke="{AMBER}" stroke-width="2"/>
  <polyline points="8,40 20,30 30,34 42,18 54,12" fill="none" stroke="{CREAM}" stroke-width="2.4"
    stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="70 90" stroke-dashoffset="0">
    <animate attributeName="stroke-dashoffset" values="75;0;0;75" keyTimes="0;0.35;0.85;1" dur="5s" repeatCount="indefinite"/>
  </polyline>
  <circle cx="54" cy="12" r="3" fill="{AMBER}">
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.33;0.38;0.85;1" dur="5s" repeatCount="indefinite"/>
  </circle>
</g>'''


def card(name, title, lines, slug, icon):
    desc = "".join(f'<text x="112" y="{78 + i * 21}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{l}</text>'
                   for i, l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset="0.5" stop-color="{AMBER}" stop-opacity="0.7"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
<g clip-path="url(#c)">
  <rect x="-160" y="{H - 3}" width="160" height="3" fill="url(#sheen)">
    <animate attributeName="x" values="-160;{W};{W}" keyTimes="0;0.6;1" dur="6s" repeatCount="indefinite"/>
  </rect>
</g>
{icon}
<text x="112" y="50" font-family="{SANS}" font-size="23" font-weight="600" fill="{CREAM}">{title}</text>
{desc}
<text x="{W - 22}" y="{H - 18}" font-family="{MONO}" font-size="12" fill="{MUTED}" opacity="0.7" text-anchor="end">{slug}</text>
</svg>
'''
    with open(os.path.join(ROOT, f"card-{name}.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"card-{name}.svg", len(svg.encode()), "octets")


card("boite", "Boite", ["Tout ton travail et tes agents", "au même endroit."], "beboite/boite", ICON_BOITE)
card("skincapital", "SkinCapital", ["Suivi de portefeuille de skins CS2 :", "prix, profit et pertes, alertes."], "ChrisPlayer/SkinCapital", ICON_SKIN)
