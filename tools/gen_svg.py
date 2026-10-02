"""Genere les SVG animes du profil (assets/header.svg, assets/typing.svg).
Relancer apres modification : python tools/gen_svg.py
"""
import os, random

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(ROOT, exist_ok=True)
rnd = random.Random(42)

# ---------------------------------------------------------------- header
W, H, HZ = 1200, 320, 232          # largeur, hauteur, ligne d'horizon
CX = W // 2

stars = []
for _ in range(70):
    x, y = rnd.uniform(10, W - 10), rnd.uniform(8, HZ - 20)
    if 280 < x < 920 and 40 < y < 200:
        continue
    r = rnd.choice([0.8, 1, 1.2, 1.6])
    d, b = rnd.uniform(2, 5), rnd.uniform(0, 5)
    stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff">'
                 f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>')

# grille du sol : lignes vers le point de fuite + lignes horizontales qui defilent
grid = [f'<line x1="{CX}" y1="{HZ}" x2="{CX + k * 150}" y2="{H}" />' for k in range(-12, 13)]
moving, N, DUR = [], 7, 2.4
for k in range(N):
    ys = [HZ + (H - HZ) * (t / 10) ** 2.2 for t in range(11)]
    vals = ";".join(f"{y:.1f}" for y in ys)
    ops = ";".join(f"{min(1, t / 4):.2f}" for t in range(11))
    beg = f"-{k * DUR / N:.2f}s"
    moving.append(f'<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}">'
                  f'<animate attributeName="y1" values="{vals}" dur="{DUR}s" begin="{beg}" repeatCount="indefinite"/>'
                  f'<animate attributeName="y2" values="{vals}" dur="{DUR}s" begin="{beg}" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="{ops}" dur="{DUR}s" begin="{beg}" repeatCount="indefinite"/></line>')

# pixels qui montent depuis le sol
pixels = []
for _ in range(22):
    x = rnd.uniform(40, W - 40)
    s = rnd.choice([3, 4, 5])
    d, b = rnd.uniform(5, 10), rnd.uniform(0, 10)
    c = rnd.choice(["#36e2ff", "#ff4fd8", "#ffd319"])
    pixels.append(f'<rect x="{x:.0f}" y="{H}" width="{s}" height="{s}" fill="{c}">'
                  f'<animateTransform attributeName="transform" type="translate" values="0 0;{rnd.uniform(-30, 30):.0f} -{H}" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="0;0.9;0.9;0" keyTimes="0;0.15;0.7;1" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></rect>')

# bandes du soleil retro (trous de plus en plus larges vers le bas)
stripes = []
y, gap = HZ - 52, 3
while y < HZ:
    stripes.append(f'<rect x="0" y="{y:.0f}" width="{W}" height="{gap:.0f}" fill="#000"/>')
    y += gap + 9
    gap += 1.6

FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#07021a"/><stop offset="0.6" stop-color="#240845"/><stop offset="1" stop-color="#5a1468"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffd319"/><stop offset="0.55" stop-color="#ff2975"/><stop offset="1" stop-color="#8c1eff"/>
  </linearGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
    <stop offset="0" stop-color="#36e2ff"/><stop offset="0.5" stop-color="#ff4fd8"/><stop offset="1" stop-color="#ffd319"/>
    <animate attributeName="x1" values="0;1;0" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="1;2;1" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1a0433"/><stop offset="1" stop-color="#05010f"/>
  </linearGradient>
  <mask id="sunMask"><rect width="{W}" height="{H}" fill="#fff"/>{"".join(stripes)}</mask>
  <clipPath id="aboveHz"><rect width="{W}" height="{HZ}"/></clipPath>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
  <style>
    .glitch {{ animation: glitch 4s steps(1) infinite; }}
    .g2 {{ animation-delay: -0.15s; }}
    @keyframes glitch {{
      0%, 86%, 100% {{ transform: translate(0, 0); opacity: 0; }}
      88% {{ transform: translate(-6px, 2px); opacity: 0.8; }}
      90% {{ transform: translate(5px, -2px); opacity: 0.8; }}
      92% {{ transform: translate(-3px, 0); opacity: 0.6; }}
      94% {{ transform: translate(0, 0); opacity: 0; }}
    }}
    .flicker {{ animation: flicker 5s linear infinite; }}
    @keyframes flicker {{ 0%, 41%, 43%, 45%, 100% {{ opacity: 1; }} 42%, 44% {{ opacity: 0.55; }} }}
  </style>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <g>{"".join(stars)}</g>
  <g clip-path="url(#aboveHz)">
    <circle cx="{CX}" cy="{HZ}" r="118" fill="#ff2975" opacity="0.35" filter="url(#softGlow)">
      <animate attributeName="r" values="112;126;112" dur="4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{CX}" cy="{HZ}" r="100" fill="url(#sun)" mask="url(#sunMask)"/>
  </g>
  <rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>
  <g stroke="#ff2975" stroke-width="1.4" opacity="0.55">{"".join(grid)}</g>
  <g stroke="#ff4fd8" stroke-width="1.4">{"".join(moving)}</g>
  <line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="#ff9de6" stroke-width="2" filter="url(#glow)"/>
  <g>{"".join(pixels)}</g>
  <g font-family="{FONT}" font-weight="900" font-size="104" text-anchor="middle" letter-spacing="16">
    <text class="glitch" x="{CX}" y="128" fill="#36e2ff">CHRIS</text>
    <text class="glitch g2" x="{CX}" y="128" fill="#ff2975">CHRIS</text>
    <text class="flicker" x="{CX}" y="128" fill="url(#title)" filter="url(#glow)">CHRIS</text>
  </g>
  <text x="{CX}" y="170" font-family="{FONT}" font-weight="600" font-size="21" letter-spacing="9" text-anchor="middle" fill="#f5e8ff" opacity="0.92">GAME DEVELOPER · UNITY · C#</text>
</g>
</svg>
'''

# ---------------------------------------------------------------- typing
PHRASES = [
    ("Je crée des jeux vidéo avec Unity", "#8b5cf6"),
    ("Un prototype toujours en cours...", "#ec4899"),
    ("Bienvenue sur mon GitHub !", "#0891b2"),
]
TW, TH, FS, CW = 760, 54, 26, 15.6     # CW = largeur imposee d'un caractere (textLength)
SLOT, TYPE, HOLD_END, ERASE = 4.5, 0.07, 3.6, 0.025
T = SLOT * len(PHRASES)
X0 = (TW - max(len(p) for p, _ in PHRASES) * CW) / 2

texts, cursor_pts = [], [(0.0, 0.0)]
for i, (p, color) in enumerate(PHRASES):
    s, n = i * SLOT, len(p)
    pts = [(0.0, 0.0), (s, 0.0)]
    pts += [(s + c * TYPE, c * CW) for c in range(1, n + 1)]
    end_type = s + n * TYPE
    pts += [(s + HOLD_END + c * ERASE, (n - c) * CW) for c in range(1, n + 1)]
    pts = sorted(set(pts))
    cursor_pts += pts[1:]
    kt = ";".join(f"{t / T:.4f}" for t, _ in pts)
    vs = ";".join(f"{w:.1f}" for _, w in pts)
    texts.append(f'''<clipPath id="c{i}"><rect x="{X0:.1f}" y="0" height="{TH}" width="0">
    <animate attributeName="width" values="{vs}" keyTimes="{kt}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>
  <text clip-path="url(#c{i})" x="{X0:.1f}" y="{TH / 2 + FS * 0.36:.1f}" textLength="{n * CW:.1f}" lengthAdjust="spacingAndGlyphs" fill="{color}">{p}</text>''')

cursor_pts = sorted(set(cursor_pts))
ckt = ";".join(f"{t / T:.4f}" for t, _ in cursor_pts)
cvs = ";".join(f"{X0 + w + 3:.1f}" for _, w in cursor_pts)
typing = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">
<g font-family="Consolas, 'Cascadia Mono', 'Courier New', monospace" font-size="{FS}" font-weight="600">
  {"".join(texts)}
</g>
<rect y="{TH / 2 - FS / 2:.1f}" width="3" height="{FS}" fill="#ec4899">
  <animate attributeName="x" values="{cvs}" keyTimes="{ckt}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="1;0" dur="0.9s" calcMode="discrete" repeatCount="indefinite"/>
</rect>
</svg>
'''

for name, svg in (("header.svg", header), ("typing.svg", typing)):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(name, len(svg.encode()), "octets")
