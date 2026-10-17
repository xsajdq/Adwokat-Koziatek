import sys, math, os
SP = sys.argv[1]; OUT = sys.argv[2]
sys.path.insert(0, SP + "/tools")
from textpath import text_path, font
CIN = SP + "/fonts/Cinzel[wght].ttf"
INK = "#111"

# Custom roman K, cap height 200, baseline y=200, top y=0.
SER = 7
K_D = ("M30 0H62V200H30Z "                     # stem
       "M14 0H78V%(s)sH14Z M14 %(b)sH78V200H14Z "  # stem serifs
       "M62 113.4L142.1 0H153.3L62 128.6Z "      # thin arm
       "M126 0H172V%(s)sH126Z "                   # arm serif
       "M76.2 109.3L91.9 80.6L170.2 180Q181 196 214 200H147.7Z") % {"s": SER, "b": 200 - SER}
K_W = 214  # advance-ish extent

def K(x, y, cap):
    s = cap / 200.0
    return f'<path transform="translate({x:.2f} {y - cap:.2f}) scale({s:.4f})" d="{K_D}"/>'

def svg(vb, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n  <title>{title}</title>\n  <g fill="{INK}">\n{body}\n  </g>\n</svg>\n'

def arch(x0, x1, ytop, ybot):
    r = (x1 - x0) / 2; cx = x0 + r
    return f"M{x0} {ybot}V{ytop + r}A{r} {r} 0 0 1 {x1} {ytop + r}V{ybot}Z"

def ring(r, t, cx=128, cy=128):
    ro, ri = r, r - t
    return (f"M{cx-ro} {cy}A{ro} {ro} 0 1 0 {cx+ro} {cy}A{ro} {ro} 0 1 0 {cx-ro} {cy}Z "
            f"M{cx-ri} {cy}A{ri} {ri} 0 1 1 {cx+ri} {cy}A{ri} {ri} 0 1 1 {cx-ri} {cy}Z")

def circle_text(text, r_base, cap, wght, cx=128, cy=128, start_deg=0, tracking=120):
    """Glyphs standing on a circle of radius r_base (baseline), reading clockwise from start angle (0 = top)."""
    f = font(CIN, wght); upm = f["head"].unitsPerEm; cmap = f.getBestCmap(); hmtx = f["hmtx"]
    size = cap / 0.7  # Cinzel cap height ~0.7 em
    s = size / upm
    widths = [hmtx[cmap[ord(c)]][0] * s + tracking * size / 1000 for c in text]
    total = sum(widths); circ = 2 * math.pi * r_base
    scale = circ / total  # spread evenly round the full circle
    parts = []; acc = 0
    for c, w in zip(text, widths):
        if c != " ":
            gw = hmtx[cmap[ord(c)]][0] * s
            mid = acc + w * scale / 2
            ang = start_deg + mid / circ * 360
            d, _ = text_path(c, CIN, wght, size, -gw / 2, 0)
            parts.append(f'<path transform="rotate({ang:.3f} {cx} {cy}) translate({cx} {cy - r_base})" d="{d}"/>')
        acc += w * scale
    return "\n".join(parts)

def arc_text(text, R, cap, wght, top=True, cx=128, cy=128, tracking=300):
    f = font(CIN, wght); upm = f["head"].unitsPerEm; cmap = f.getBestCmap(); hmtx = f["hmtx"]
    size = cap / 0.7; s_ = size / upm
    gws = [hmtx[cmap[ord(c)]][0] * s_ for c in text]
    tr = tracking * size / 1000
    total = sum(gws) + tr * (len(text) - 1)
    Rm = R + (cap / 2 if top else -cap / 2)  # measure along the mid-height of the letters
    span = total / Rm; acc = 0; parts = []
    for c, gw in zip(text, gws):
        phi = -span / 2 + (acc + gw / 2) / Rm
        d, _ = text_path(c, CIN, wght, size, -gw / 2, 0)
        deg = math.degrees(phi)
        if top:
            x, y = cx + R * math.sin(phi), cy - R * math.cos(phi); rot = deg
        else:
            x, y = cx + R * math.sin(phi), cy + R * math.cos(phi); rot = -deg
            # bottom reads left->right: mirror the progression
            x = cx + R * math.sin(phi)
        parts.append(f'<path transform="translate({x:.2f} {y:.2f}) rotate({rot:.3f})" d="{d}"/>')
        acc += gw + tr
    return "\n".join(parts)

os.makedirs(OUT, exist_ok=True)
def write(name, s): open(os.path.join(OUT, name), "w").write(s)

# ---------- A: Portal (K in a round-top arch) ----------
capA = 104; kwA = K_W * capA / 200
def open_arch(x0, x1, ytop, ybot, t):
    r = (x1 - x0) / 2; cx = x0 + r; ri = r - t
    return (f"M{x0} {ybot}V{ytop + r}A{r} {r} 0 0 1 {x1} {ytop + r}V{ybot}H{x1 - t}V{ytop + r}"
            f"A{ri} {ri} 0 0 0 {x0 + t} {ytop + r}V{ybot}Z")
a_body = (f'<path d="{open_arch(60, 196, 20, 210, 6)}"/>\n'
          f'<rect x="40" y="210" width="176" height="7"/>\n<rect x="52" y="223" width="152" height="4"/>\n'
          + K(128 - kwA / 2 + 4, 196, capA))
write("a-symbol.svg", svg("0 0 256 256", a_body, "A – Portal"))
write("a-small.svg", svg("0 0 256 256", K(128 - K_W * 0.8 / 2 + 6, 208, 160), "A – small"))

# ---------- B: Pieczęć (seal) ----------
capB = 96; kwB = K_W * capB / 200
b_body = (f'<path fill-rule="evenodd" d="{ring(116, 5)}"/>\n<path fill-rule="evenodd" d="{ring(84, 2.5)}"/>\n'
          + arc_text("ADWOKAT", 92, 15, 600, top=True) + "\n" + arc_text("KOZIATEK", 107, 15, 600, top=False)
          + '\n<circle cx="27" cy="128" r="3"/><circle cx="229" cy="128" r="3"/>'
          + "\n" + K(128 - kwB / 2 + 3, 128 + capB / 2, capB))
write("b-symbol.svg", svg("0 0 256 256", b_body, "B – Pieczęć"))
# simplified inner mark for small sizes
write("b-small.svg", svg("0 0 256 256", f'<path fill-rule="evenodd" d="{ring(116, 10)}"/>\n' + K(128 - K_W * 0.6 / 2 + 3, 128 + 60, 120), "B – small"))

# ---------- C: Wordmark with toga trim line ----------
def wordmark(x, base, cap, trim=True):
    """KOZIATEK with custom K's, ADWOKAT above. Returns (svg, width)."""
    size = cap / 0.7
    parts = []; cx = x
    parts.append(K(cx, base, cap)); cx += K_W * cap / 200 * 0.86
    d, w = text_path("OZIATE", CIN, 600, size, cx, base, 60)
    parts.append(f'<path d="{d}"/>'); cx += w + 60 * size / 1000 + 4
    parts.append(K(cx, base, cap)); cx += K_W * cap / 200
    width = cx - x
    d2, w2 = text_path("ADWOKAT", CIN, 600, size * 0.34, 0, 0, 420)
    parts.insert(0, f'<path transform="translate({x + (width - w2) / 2:.2f} {base - cap - cap * 0.42:.2f})" d="{d2}"/>')
    return "\n".join(parts), width

wm, wmw = wordmark(70, 176, 84)
trim = f'<rect x="40" y="{176 - 84 - 84 * 0.42 - 84 / 0.7 * 0.34 * 0.7:.1f}" width="7" height="{84 + 84 * 0.42 + 84 / 0.7 * 0.34 * 0.7:.1f}" fill="#1F4D3A"/>'
write("c-lockup.svg", svg(f"0 0 {70 + wmw + 40:.0f} 204", trim + "\n" + wm, "C – Lamówka"))
write("c-symbol.svg", svg("0 0 256 256", '<rect x="48" y="40" width="12" height="176" fill="#1F4D3A"/>\n' + K(84, 216, 176 * 0.0 + 160 - 0, ) if False else
      '<rect x="44" y="56" width="12" height="144" fill="#1F4D3A"/>\n' + K(72, 200, 144), "C – Lamówka"))

# ---------- lockups for A and B: symbol + wordmark ----------
for key, title in (("a", "A – Portal"), ("b", "B – Pieczęć")):
    sym = open(os.path.join(OUT, f"{key}-symbol.svg")).read().split('<g fill="#111">')[1].split("</g>")[0]
    wm2, w2 = wordmark(300, 166, 70)
    write(f"{key}-lockup.svg", svg(f"0 0 {300 + w2 + 20:.0f} 256", f'<g transform="translate(8 0)">{sym}</g>\n' + wm2, title))
print("ok", wmw)
