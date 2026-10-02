"""Genere la banniere animee du profil (assets/header.svg).
Relancer apres modification : python tools/gen_svg.py
"""
import os, random

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(ROOT, exist_ok=True)
rnd = random.Random(7)

W, H = 1200, 380
CX, CY = W // 2, 205
NAME = "CHRIS"
LOOP = 12  # secondes : trace du contour, remplissage, pause, effacement
FONT = "'Segoe UI Black', 'Arial Black', 'Helvetica Neue', Arial, sans-serif"

# taches d'aurore floues qui derivent
blobs = []
for color, (x, y), r, (dx, dy), d in [
    ("#7c3aed", (250, 120), 230, (180, 60), 18),
    ("#06b6d4", (950, 260), 210, (-200, -50), 21),
    ("#ec4899", (620, 330), 190, (120, -110), 16),
    ("#2563eb", (820, 60), 170, (-150, 90), 23),
]:
    blobs.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="0.55">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};0 0" '
                 f'dur="{d}s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></circle>')

# poussiere lumineuse
dust = []
for _ in range(60):
    x, y = rnd.uniform(0, W), rnd.uniform(0, H)
    r = rnd.choice([0.7, 1, 1.3, 1.8])
    d, b = rnd.uniform(14, 30), rnd.uniform(0, 30)
    tw = rnd.uniform(2, 5)
    dust.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff">'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;{rnd.uniform(-60, 60):.0f} {rnd.uniform(-80, -20):.0f}" dur="{d:.0f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;0.9;0.2;0.9;0" dur="{tw * 3:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>')

# timeline du nom (fractions de LOOP)
k = "0;0.25;0.33;0.85;0.93;1"
dash = "700;0;0;0;700;700"
fill = "0;0;1;1;0;0"

header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
  <filter id="glow" x="-10%" y="-40%" width="120%" height="180%">
    <feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.07 0"/>
  </filter>
  <linearGradient id="ink" gradientUnits="userSpaceOnUse" x1="250" y1="0" x2="950" y2="0">
    <stop offset="0" stop-color="#a5f3fc"/><stop offset="0.35" stop-color="#c4b5fd"/>
    <stop offset="0.7" stop-color="#f9a8d4"/><stop offset="1" stop-color="#fde68a"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-300 0;300 0;-300 0" dur="10s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="ring" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
    <stop offset="0" stop-color="#22d3ee"/><stop offset="0.5" stop-color="#a855f7" stop-opacity="0.15"/><stop offset="1" stop-color="#ec4899"/>
    <animateTransform attributeName="gradientTransform" type="rotate" values="0 {CX} {H // 2};360 {CX} {H // 2}" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="nameMask"><text x="{CX}" y="{CY}" font-family="{FONT}" font-weight="900" font-size="150" letter-spacing="22" text-anchor="middle" fill="#fff">{NAME}</text></mask>
  <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#22d3ee" stop-opacity="0"/><stop offset="0.5" stop-color="#e9d5ff"/><stop offset="1" stop-color="#ec4899" stop-opacity="0"/>
  </linearGradient>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="#05040d"/>
  <g filter="url(#blur)">{"".join(blobs)}</g>
  <rect width="{W}" height="{H}" fill="#05040d" opacity="0.35"/>
  <g opacity="0.08" stroke="#fff" stroke-width="1">
    {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W + 1, 60))}
    {"".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(20, H, 60))}
  </g>
  <g>{"".join(dust)}</g>

  <g font-family="{FONT}" font-weight="900" font-size="150" letter-spacing="22" text-anchor="middle">
    <text x="{CX}" y="{CY}" fill="url(#ink)" filter="url(#glow)" opacity="0">{NAME}
      <animate attributeName="opacity" values="{fill}" keyTimes="{k}" dur="{LOOP}s" repeatCount="indefinite"/>
    </text>
    <text x="{CX}" y="{CY}" fill="none" stroke="url(#ink)" stroke-width="2.2" stroke-dasharray="700" stroke-dashoffset="700" filter="url(#glow)">{NAME}
      <animate attributeName="stroke-dashoffset" values="{dash}" keyTimes="{k}" dur="{LOOP}s" repeatCount="indefinite"/>
    </text>
  </g>
  <g mask="url(#nameMask)">
    <rect x="-300" y="0" width="260" height="{H}" fill="url(#sweep)" opacity="0.55" transform="skewX(-20)">
      <animate attributeName="x" values="-300;-300;1500;1500" keyTimes="0;0.4;0.6;1" dur="{LOOP / 2}s" repeatCount="indefinite"/>
    </rect>
  </g>

  <rect x="{CX - 160}" y="{CY + 42}" width="320" height="2" fill="url(#line)">
    <animate attributeName="width" values="0;320;320;0" keyTimes="0;0.3;0.85;1" dur="{LOOP}s" repeatCount="indefinite"/>
    <animate attributeName="x" values="{CX};{CX - 160};{CX - 160};{CX}" keyTimes="0;0.3;0.85;1" dur="{LOOP}s" repeatCount="indefinite"/>
  </rect>

  <rect width="{W}" height="{H}" filter="url(#grain)"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="21" fill="none" stroke="url(#ring)" stroke-width="2"/>
</svg>
'''

with open(os.path.join(ROOT, "header.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(header)
print("header.svg", len(header.encode()), "octets")
