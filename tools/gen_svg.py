"""Genere la banniere animee du profil (assets/header.svg) : un chat sur un muret, la nuit.
Relancer apres modification : python tools/gen_svg.py
"""
import os, random

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(ROOT, exist_ok=True)
rnd = random.Random(3)

W, H = 1200, 380
WALL = 300                  # haut du muret
CAT_X = 960                 # centre du chat
NAME = "CHRIS"
FONT = "'Segoe UI Light', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

SKY_TOP, SKY_BOT = "#1b1a1e", "#2a2729"
CAT = "#0f0e10"
CREAM = "#d9d1c4"
EYE = "#b9a477"

# etoiles discretes
stars = []
for _ in range(45):
    x, y = rnd.uniform(10, W - 10), rnd.uniform(10, 200)
    d, b = rnd.uniform(3, 7), rnd.uniform(0, 7)
    stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([0.6, 0.9, 1.2])}" fill="{CREAM}">'
                 f'<animate attributeName="opacity" values="0.1;0.6;0.1" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>')

# toits au loin + fenetres qui s'allument et s'eteignent
roofs, windows, x = [], [], -20
while x < W:
    w = rnd.randint(60, 140)
    h = rnd.randint(40, 110)
    top = WALL - h
    roofs.append(f"M{x} {WALL} L{x} {top} L{x + w // 2} {top - rnd.randint(8, 26)} L{x + w} {top} L{x + w} {WALL} Z")
    if rnd.random() < 0.5:
        cx = x + rnd.randint(10, w - 25)
        roofs.append(f"M{cx} {top} l0 -18 l10 0 l0 18 Z")
    for _ in range(rnd.randint(0, 3)):
        wx, wy = x + rnd.randint(8, w - 16), rnd.randint(top + 8, WALL - 18)
        d = rnd.uniform(8, 20)
        on = rnd.uniform(0.2, 0.6)
        windows.append(f'<rect x="{wx}" y="{wy}" width="7" height="9" fill="#8f7d5c">'
                       f'<animate attributeName="opacity" values="0.45;0.45;0.05;0.05;0.45" keyTimes="0;{on:.2f};{on + 0.02:.2f};{on + 0.3:.2f};1" '
                       f'dur="{d:.0f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></rect>')
    x += w + rnd.randint(-10, 6)

# empreintes de pattes qui menent au chat
def paw(px, py, rot):
    return (f'<g transform="translate({px} {py}) rotate({rot}) scale(1.5)"><ellipse cx="0" cy="3" rx="4.2" ry="3.4"/>'
            f'<circle cx="-4.6" cy="-3" r="1.6"/><circle cx="-1.6" cy="-5.4" r="1.6"/>'
            f'<circle cx="1.8" cy="-5.4" r="1.6"/><circle cx="4.8" cy="-3" r="1.6"/></g>')

PAWS, STEP, T = 9, 0.45, 14
paws = []
for i in range(PAWS):
    px = 470 + i * 50
    py = 330 + (6 if i % 2 else -6)
    a = i * STEP / T
    paws.append(f'<g opacity="0">{paw(px, py, 90)}'
                f'<animate attributeName="opacity" values="0;0;0.5;0.5;0;0" keyTimes="0;{a:.3f};{a + 0.02:.3f};{0.75:.3f};{0.85:.3f};1" '
                f'dur="{T}s" repeatCount="indefinite"/></g>')

# poussiere chaude qui flotte
motes = []
for _ in range(14):
    mx, my = rnd.uniform(0, W), rnd.uniform(60, WALL)
    d, b = rnd.uniform(12, 24), rnd.uniform(0, 24)
    motes.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="1.4" fill="#c2ab7c">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;{rnd.uniform(-40, 40):.0f} {rnd.uniform(-50, -15):.0f};0 0" dur="{d:.0f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0.5;0" dur="{d / 2:.0f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>')

# queue : trois courbes de meme structure, interpolees
tails = ["M36 -6 C70 0 78 40 62 76", "M36 -6 C68 6 58 46 38 80", "M36 -6 C74 -2 94 34 86 72"]
tail_vals = ";".join([tails[0], tails[1], tails[0], tails[2], tails[0]])

blink = "4.6;4.6;0.4;4.6;4.6;0.4;4.6;4.6"
blink_k = "0;0.46;0.48;0.5;0.9;0.92;0.94;1"
pupil = "3.6;3.6;0.3;3.6;3.6;0.3;3.6;3.6"

FUR, FUR_D, BELLY, PINK, INK = "#c38c5f", "#a3714b", "#e6d7c2", "#cf9e95", "#2a2321"
eye_ry = "8.5;8.5;0.9;8.5;8.5;0.9;8.5;8.5"
hl_op = "1;1;0;1;1;0;1;1"

def eye(x):
    return (f'<ellipse cx="{x}" cy="-94" rx="8" ry="8.5" fill="{INK}"><animate attributeName="ry" values="{eye_ry}" keyTimes="{blink_k}" dur="9s" repeatCount="indefinite"/></ellipse>'
            f'<g fill="#fff"><animate attributeName="opacity" values="{hl_op}" keyTimes="{blink_k}" dur="9s" repeatCount="indefinite"/>'
            f'<circle cx="{x - 2.6}" cy="-97.5" r="3"/><circle cx="{x + 3}" cy="-90.5" r="1.3"/></g>')

cat = f'''<g transform="translate({CAT_X} {WALL}) scale(1.12)">
  <path d="{tails[0]}" fill="none" stroke="{FUR}" stroke-width="13" stroke-linecap="round">
    <animate attributeName="d" values="{tail_vals}" dur="6s" repeatCount="indefinite" calcMode="spline"
      keySplines="0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1"/>
  </path>
  <path d="M-44 0 C-52 -30 -40 -64 0 -66 C40 -64 52 -30 44 0 Z" fill="{FUR}"/>
  <path d="M-40 -30 q8 -4 12 2 M40 -30 q-8 -4 -12 2 M-43 -16 q8 -4 12 2 M43 -16 q-8 -4 -12 2" stroke="{FUR_D}" stroke-width="3" fill="none" stroke-linecap="round"/>
  <ellipse cx="0" cy="-28" rx="20" ry="25" fill="{BELLY}"/>
  <g fill="{BELLY}"><ellipse cx="-14" cy="-4" rx="11" ry="7"/><ellipse cx="14" cy="-4" rx="11" ry="7"/></g>
  <path d="M-17 -2 v-4 M-11 -2 v-4 M11 -2 v-4 M17 -2 v-4" stroke="#c9b8a2" stroke-width="1.4" stroke-linecap="round"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 0 -62;0 0 -62;-10 0 -62;-10 0 -62;0 0 -62;0 0 -62"
      keyTimes="0;0.55;0.6;0.8;0.85;1" dur="11s" repeatCount="indefinite"/>
    <g>
      <path d="M-42 -100 Q-50 -150 -10 -124 Z" fill="{FUR}" stroke="{FUR}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M-36 -106 Q-41 -136 -17 -122 Z" fill="{PINK}"/>
    </g>
    <g>
      <animateTransform attributeName="transform" type="rotate" values="0 24 -116;0 24 -116;16 24 -116;0 24 -116;0 24 -116"
        keyTimes="0;0.7;0.72;0.75;1" dur="7s" repeatCount="indefinite"/>
      <path d="M42 -100 Q50 -150 10 -124 Z" fill="{FUR}" stroke="{FUR}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M36 -106 Q41 -136 17 -122 Z" fill="{PINK}"/>
    </g>
    <ellipse cx="0" cy="-90" rx="48" ry="39" fill="{FUR}"/>
    <path d="M-8 -127 q2 8 0 14 M0 -128 v15 M8 -127 q-2 8 0 14" stroke="{FUR_D}" stroke-width="3" fill="none" stroke-linecap="round"/>
    <ellipse cx="-11" cy="-74" rx="15" ry="11" fill="{BELLY}"/><ellipse cx="11" cy="-74" rx="15" ry="11" fill="{BELLY}"/>
    <g fill="{PINK}" opacity="0.55"><ellipse cx="-31" cy="-78" rx="8" ry="4.5"/><ellipse cx="31" cy="-78" rx="8" ry="4.5"/></g>
    {eye(-18)}{eye(18)}
    <path d="M-3.6 -82 h7.2 l-3.6 4 Z" fill="{PINK}" stroke="{PINK}" stroke-width="1.5" stroke-linejoin="round"/>
    <path d="M-7 -74 q3.5 4 7 0 q3.5 4 7 0" stroke="{INK}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <g stroke="#e9dfd0" stroke-width="1.1" stroke-linecap="round" opacity="0.8">
      <line x1="-28" y1="-76" x2="-60" y2="-82"/><line x1="-28" y1="-72" x2="-60" y2="-70"/>
      <line x1="28" y1="-76" x2="60" y2="-82"/><line x1="28" y1="-72" x2="60" y2="-70"/>
    </g>
  </g>
  <path d="M0 0 c-3 -3 -7 -1 -7 2 c0 3 4 5 7 8 c3 -3 7 -5 7 -8 c0 -3 -4 -5 -7 -2 Z" fill="{PINK}" opacity="0">
    <animateTransform attributeName="transform" type="translate" values="34 -130;34 -130;48 -175;48 -175" keyTimes="0;0.6;0.85;1" dur="10s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0;0.8;0;0" keyTimes="0;0.6;0.66;0.85;1" dur="10s" repeatCount="indefinite"/>
  </path>
</g>'''

bricks = []
for row, y in enumerate(range(WALL + 22, H, 22)):
    bricks.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    for bx in range(-40 + (35 if row % 2 else 0), W, 70):
        bricks.append(f'<line x1="{bx}" y1="{y - 22}" x2="{bx}" y2="{y}"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY_TOP}"/><stop offset="1" stop-color="{SKY_BOT}"/></linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="{CREAM}" stop-opacity="0.18"/><stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.06 0"/>
  </filter>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <g>{"".join(stars)}</g>
  <circle cx="{CAT_X}" cy="150" r="150" fill="url(#halo)">
    <animate attributeName="r" values="140;158;140" dur="8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{CAT_X}" cy="150" r="66" fill="#d4ccbd" opacity="0.92"/>
  <circle cx="{CAT_X - 22}" cy="132" r="9" fill="#c3baa9" opacity="0.6"/>
  <circle cx="{CAT_X + 18}" cy="172" r="13" fill="#c3baa9" opacity="0.5"/>
  <path d="{" ".join(roofs)}" fill="#232125"/>
  <g>{"".join(windows)}</g>
  <text x="400" y="200" font-family="{FONT}" font-weight="300" font-size="118" letter-spacing="34" text-anchor="middle" fill="{CREAM}" opacity="0">{NAME}
    <animate attributeName="opacity" values="0;0.88" dur="2.5s" fill="freeze"/>
  </text>
  <g>{"".join(motes)}</g>
  <rect y="{WALL}" width="{W}" height="{H - WALL}" fill="#2e2a28"/>
  <rect y="{WALL}" width="{W}" height="5" fill="#3b3633"/>
  <g stroke="#262220" stroke-width="2">{"".join(bricks)}</g>
  <g fill="#1a1817">{"".join(paws)}</g>
  {cat}
  <rect width="{W}" height="{H}" filter="url(#grain)"/>
</g>
</svg>
'''

with open(os.path.join(ROOT, "header.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print("header.svg", len(svg.encode()), "octets")
