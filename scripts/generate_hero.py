"""Generate assets/hero-light.svg and assets/hero-dark.svg for the profile README.

Run:  uv run python3 scripts/generate_hero.py

Design mirrors ubaidbinwaris.com: monochrome palette, terminal window with
traffic-light dots, eyebrow label, typed headline, deploy line with a status
dot, and the four hero stats. Edit HEADLINE or the stat() calls below when the
numbers on the site change, then re-run. Only SVG + SMIL is used so GitHub's
image proxy renders it unchanged (no external fonts, scripts or styles).
"""
from pathlib import Path

W, H = 1200, 320
MONO = "ui-monospace, 'SFMono-Regular', Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"

THEMES = {
    "light": dict(bg="#ffffff", surface="#fafafa", line="#e5e5e5", fg="#0a0a0a", muted="#525252", subtle="#6b6b6b"),
    "dark":  dict(bg="#0a0a0a", surface="#111111", line="#262626", fg="#fafafa", muted="#a3a3a3", subtle="#737373"),
}

HEADLINE = "I engineer the whole product."
HSIZE = 40
PITCH = 24                      # fixed advance per glyph (0.6em) enforced via textLength
X0 = 64
TYPE_START, TYPE_STEP = 0.4, 0.075
n = len(HEADLINE)
TYPE_END = TYPE_START + n * TYPE_STEP

def typing_values():
    widths = ";".join(str(i * PITCH) for i in range(n + 1))
    xs = ";".join(str(X0 + i * PITCH) for i in range(n + 1))
    keytimes = ";".join(f"{i / n:.4f}" for i in range(n + 1))
    return widths, xs, keytimes

def stat(x, num, label, t):
    return (f'<text x="{x}" y="268" font-family="{MONO}" font-size="14">'
            f'<tspan font-weight="600" fill="{t["fg"]}">{num}</tspan>'
            f'<tspan dx="8" fill="{t["muted"]}">{label}</tspan></text>')

def build(t):
    widths, xs, keytimes = typing_values()
    dur = f"{n * TYPE_STEP:.3f}s"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ubaid Bin Waris, full-stack developer. I engineer the whole product. 15 case studies, 4 live in production, 2 public on GitHub, 24h typical reply.">
  <defs>
    <clipPath id="type"><rect x="{X0}" y="150" width="0" height="56">
      <animate attributeName="width" values="{widths}" keyTimes="{keytimes}" calcMode="discrete" begin="{TYPE_START}s" dur="{dur}" fill="freeze"/>
    </rect></clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>

  <!-- terminal window -->
  <rect x="40" y="40" width="1120" height="240" rx="12" fill="{t["surface"]}" stroke="{t["line"]}"/>
  <line x1="40" y1="86" x2="1160" y2="86" stroke="{t["line"]}"/>
  <circle cx="66" cy="63" r="6" fill="#ff5f56"/>
  <circle cx="86" cy="63" r="6" fill="#ffbd2e"/>
  <circle cx="106" cy="63" r="6" fill="#27c93f"/>
  <text x="600" y="68" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["subtle"]}">ubaid@arch: ~/products</text>

  <!-- eyebrow -->
  <text x="{X0}" y="124" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{t["subtle"]}">UBAID BIN WARIS / FULL-STACK DEVELOPER</text>

  <!-- typed headline -->
  <g clip-path="url(#type)">
    <text x="{X0}" y="192" font-family="{MONO}" font-size="{HSIZE}" font-weight="600" fill="{t["fg"]}" textLength="{n * PITCH}" lengthAdjust="spacing">{HEADLINE}</text>
  </g>
  <rect x="{X0}" y="158" width="3" height="42" fill="{t["fg"]}">
    <animate attributeName="x" values="{xs}" keyTimes="{keytimes}" calcMode="discrete" begin="{TYPE_START}s" dur="{dur}" fill="freeze"/>
    <animate attributeName="opacity" values="1;0;1" dur="1s" begin="{TYPE_END:.3f}s" repeatCount="indefinite"/>
  </rect>

  <!-- deploy line + status (fades in after typing) -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{TYPE_END + 0.2:.3f}s" dur="0.4s" fill="freeze"/>
    <text x="{X0}" y="232" font-family="{MONO}" font-size="15" fill="{t["muted"]}">$ deploy --env production</text>
    <circle cx="372" cy="227" r="4" fill="#27c93f"/>
    <text x="384" y="232" font-family="{MONO}" font-size="15" fill="{t["fg"]}">system stable</text>
  </g>

  <!-- stats -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{TYPE_END + 0.5:.3f}s" dur="0.4s" fill="freeze"/>
    {stat(X0, "15", "case studies", t)}
    {stat(X0 + 262, "4", "live in production", t)}
    {stat(X0 + 560, "2", "public on GitHub", t)}
    {stat(X0 + 836, "24h", "typical reply", t)}
  </g>
</svg>
'''

out = Path(__file__).resolve().parent.parent / "assets"
for name, theme in THEMES.items():
    p = out / f"hero-{name}.svg"
    p.write_text(build(theme), encoding="utf-8")
    print(f"wrote {p} ({p.stat().st_size} bytes)")
