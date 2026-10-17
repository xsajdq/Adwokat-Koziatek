"""Outline text to an SVG path string using fontTools (variable font instancing + tracking + simple kerning)."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

_cache = {}

def font(path, wght):
    key = (path, wght)
    if key not in _cache:
        f = TTFont(path)
        if 'fvar' in f:
            f = instantiateVariableFont(f, {"wght": wght}, inplace=False)
        _cache[key] = f
    return _cache[key]

def kern_pairs(f):
    pairs = {}
    try:
        gpos = f['GPOS'].table
    except KeyError:
        return pairs
    for lookup in gpos.LookupList.Lookup:
        if lookup.LookupType not in (2, 9):
            continue
        for st in lookup.SubTable:
            if lookup.LookupType == 9:
                st = st.ExtSubTable
            if st.Format == 1:
                cov = st.Coverage.glyphs
                for i, ps in enumerate(st.PairSet):
                    for pvr in ps.PairValueRecord:
                        v = getattr(pvr.Value1, 'XAdvance', 0) or 0
                        pairs.setdefault((cov[i], pvr.SecondGlyph), v)
            elif st.Format == 2:
                cov = st.Coverage.glyphs
                c1 = st.ClassDef1.classDefs; c2 = st.ClassDef2.classDefs
                for g1 in cov:
                    k1 = c1.get(g1, 0)
                    rec = st.Class1Record[k1]
                    for g2, k2 in c2.items():
                        v = getattr(rec.Class2Record[k2].Value1, 'XAdvance', 0) or 0
                        if v:
                            pairs.setdefault((g1, g2), v)
    return pairs

def text_path(text, fpath, wght=400, size=100, x=0, y=0, tracking=0, kern=True, extra=None):
    """Return (d, width). size = font size in user units, y = baseline, tracking in em/1000."""
    f = font(fpath, wght)
    upm = f['head'].unitsPerEm
    s = size / upm
    cmap = f.getBestCmap(); gs = f.getGlyphSet(); hmtx = f['hmtx']
    kp = kern_pairs(f) if kern else {}
    pen = SVGPathPen(gs)
    cx = 0
    names = [cmap[ord(ch)] for ch in text]
    for i, g in enumerate(names):
        tp = TransformPen(pen, (s, 0, 0, -s, x + cx * s, y))
        gs[g].draw(tp)
        cx += hmtx[g][0]
        if i < len(names) - 1:
            cx += kp.get((g, names[i + 1]), 0) + tracking * upm / 1000
            if extra and i in extra:
                cx += extra[i] * upm / 1000
    return pen.getCommands(), cx * s

if __name__ == "__main__":
    d, w = text_path(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 400)
    print(w); print(d[:200])
