"""Vitrais em SVG: vidros coloridos com linhas de chumbo, em três formatos (ogiva em mosaico, rosácea, ogiva geométrica)."""
import math, random

CHUMBO = "#1c1a20"
C = dict(cobalto="#1f4fa8", rubi="#a3192e", esmeralda="#1d7a4c", ambar="#e0a526", violeta="#6a3fa0", ceu="#6fa8dc",
         rosa="#c2577f", ouro="#f0c75e", claro="#f3e6c4", branco="#fbf6ea", prata="#c9cfd8", laranja="#e2712b", azulnoite="#173a7a")

def _var(hexc, rnd, amp=18):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    d = rnd.randint(-amp, amp)
    f = lambda v: max(0, min(255, v + d))
    return "#%02x%02x%02x" % (f(r), f(g), f(b))

def arco_path(w, h, x=0, y=0):
    r = w / 2
    return f"M{x} {y + h} V{y + r} A{r} {r} 0 0 1 {x + w} {y + r} V{y + h} Z"

def mosaico(w, h, cores, seed, passo=22, jit=6):
    """Triângulos com leve irregularidade, cobrindo w×h; cores escolhidas da lista (com variação)."""
    rnd = random.Random(seed)
    nx, ny = int(w / passo) + 2, int(h / passo) + 2
    pts = [[(i * passo + (rnd.uniform(-jit, jit) if 0 < i < nx - 1 else 0), j * passo + (rnd.uniform(-jit, jit) if 0 < j < ny - 1 else 0)) for i in range(nx)] for j in range(ny)]
    out = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a, b, c, d = pts[j][i], pts[j][i + 1], pts[j + 1][i], pts[j + 1][i + 1]
            tris = [(a, b, d), (a, d, c)] if (i + j) % 2 else [(a, b, c), (b, d, c)]
            for t in tris:
                cy = sum(p[1] for p in t) / 3
                cor = cores[min(len(cores) - 1, int(cy / h * len(cores) + rnd.uniform(-.6, .6)) % len(cores))]
                out.append(f'<path d="M{t[0][0]:.1f} {t[0][1]:.1f}L{t[1][0]:.1f} {t[1][1]:.1f}L{t[2][0]:.1f} {t[2][1]:.1f}Z" fill="{_var(cor, rnd)}"/>')
    return "".join(out)

# ---------------- símbolos (desenhados numa caixa 120×120, centro 60,60) ----------------
def chave(cor, ang):
    return (f'<g transform="rotate({ang} 60 60)"><circle cx="60" cy="24" r="13" fill="{cor}"/><circle cx="60" cy="24" r="5" fill="{C["azulnoite"]}"/>'
            f'<rect x="56" y="36" width="8" height="58" fill="{cor}"/><rect x="64" y="78" width="14" height="7" fill="{cor}"/><rect x="64" y="88" width="10" height="7" fill="{cor}"/></g>')
SIMB = {
 "chaves": chave(C["ouro"], -38) + chave(C["prata"], 38) + f'<circle cx="60" cy="60" r="5" fill="{C["rubi"]}"/>',
 "escudo": f'<path d="M60 14l38 14v26c0 26-17 44-38 54-21-10-38-28-38-54V28z" fill="{C["branco"]}"/><path d="M54 28h12v24h22v12H66v34H54V64H32V52h22z" fill="{C["rubi"]}"/>',
 "livro": f'<path d="M12 40c16-8 32-8 46 2v58c-14-10-30-10-46-2z" fill="{C["branco"]}"/><path d="M108 40c-16-8-32-8-46 2v58c14-10 30-10 46-2z" fill="{C["claro"]}"/>'
          f'<path d="M34 50v30M26 60h16" stroke="{C["rubi"]}" stroke-width="5"/><path d="M78 52l14 24M92 52l-14 24" stroke="{C["cobalto"]}" stroke-width="5"/>'
          + "".join(f'<path d="M60 34L{60 + 40 * math.cos(math.radians(a)):.0f} {34 + 40 * math.sin(math.radians(a)):.0f}" stroke="{C["ouro"]}" stroke-width="4"/>' for a in (-150, -120, -90, -60, -30)),
 "coracao": f'<path d="M60 104C30 84 16 66 16 48a22 22 0 0 1 44-6 22 22 0 0 1 44 6c0 18-14 36-44 56z" fill="{C["rubi"]}"/>'
            f'<path d="M50 26c4-10 16-10 20 0-2-8 6-14 6-14 0 10 6 14 0 24H48c-6-6-2-14 2-10z" fill="{C["laranja"]}"/><path d="M57 4h6v14h8v6h-8v8h-6v-8h-8v-6h8z" fill="{C["ouro"]}"/>'
            f'<path d="M36 64l48 0M60 44v40" stroke="{C["ouro"]}" stroke-width="4"/>',
 "calice": "".join(f'<path d="M60 28L{60 + 52 * math.cos(math.radians(a)):.0f} {28 + 52 * math.sin(math.radians(a)):.0f}" stroke="{C["ouro"]}" stroke-width="4"/>' for a in range(0, 360, 30))
           + f'<circle cx="60" cy="28" r="17" fill="{C["branco"]}"/><path d="M53 22h14M60 15v26" stroke="{C["ambar"]}" stroke-width="3"/>'
           f'<path d="M34 48h52c0 20-11 32-26 32S34 68 34 48z" fill="{C["ouro"]}"/><rect x="56" y="80" width="8" height="16" fill="{C["ouro"]}"/><path d="M38 108c4-12 40-12 44 0z" fill="{C["ouro"]}"/>',
 "maria": f'<path d="M30 30l8 12 10-14 12 14 12-14 10 14 8-12-4 22H34z" fill="{C["ouro"]}"/>'
          f'<path d="M26 104V56h12l22 26 22-26h12v48H82V76L60 100 38 76v28z" fill="{C["branco"]}"/>'
          + "".join(f'<circle cx="{60 + 54 * math.cos(math.radians(a)):.1f}" cy="{60 + 54 * math.sin(math.radians(a)):.1f}" r="3.2" fill="{C["ouro"]}"/>' for a in range(0, 360, 30)),
 "pomba": f'<path d="M20 64c18-4 30-14 40-30 6 10 6 20 0 30l40-8c-10 16-26 26-44 28l-8 18-6-16c-8-2-16-10-22-22z" fill="{C["branco"]}"/><circle cx="56" cy="44" r="2.5" fill="{CHUMBO}"/>'
          + "".join(f'<path d="M60 60L{60 + 58 * math.cos(math.radians(a)):.0f} {60 + 58 * math.sin(math.radians(a)):.0f}" stroke="{C["ouro"]}" stroke-width="3"/>' for a in range(200, 345, 24)),
}

def medalhao(cx, cy, r, simb, fundo1, fundo2):
    """Medalhão de vidro claro em setores, com o símbolo no centro."""
    setores = ""
    for k in range(12):
        a1, a2 = math.radians(k * 30), math.radians(k * 30 + 30)
        setores += f'<path d="M{cx} {cy}L{cx + r * math.cos(a1):.1f} {cy + r * math.sin(a1):.1f}A{r} {r} 0 0 1 {cx + r * math.cos(a2):.1f} {cy + r * math.sin(a2):.1f}Z" fill="{fundo1 if k % 2 else fundo2}"/>'
    s = r * 1.5 / 120
    return (setores + f'<g transform="translate({cx - 60 * s} {cy - 60 * s}) scale({s})" stroke="{CHUMBO}" stroke-width="{2.6 / s:.1f}" stroke-linejoin="round">{SIMB[simb]}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CHUMBO}" stroke-width="5"/><circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="none" stroke="{C["ouro"]}" stroke-width="3"/>')

def brilho(uid, w, h):
    return (f'<defs><radialGradient id="l{uid}" cx="50%" cy="25%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".6" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></radialGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#l{uid})" pointer-events="none"/>')

def ogiva(simb, cores, seed, medal=("#f6ecd2", "#e8d7a8"), w=200, h=300, uid="a"):
    """Janela em arco com mosaico de vidros e medalhão central."""
    p = arco_path(w, h)
    return (f'<svg viewBox="-8 -8 {w + 16} {h + 16}" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="c{uid}"><path d="{p}"/></clipPath></defs>'
            f'<g clip-path="url(#c{uid})"><g stroke="{CHUMBO}" stroke-width="2.2" stroke-linejoin="round">{mosaico(w, h, cores, seed)}</g>'
            f'{medalhao(w / 2, h * 0.52, w * 0.34, simb, *medal)}{brilho(uid, w, h)}</g>'
            f'<path d="{p}" fill="none" stroke="{CHUMBO}" stroke-width="9"/><path d="{arco_path(w - 10, h - 5, 5, 5)}" fill="none" stroke="{C["ouro"]}" stroke-width="2"/></svg>')

def rosacea(simb, cores, uid="r", n=16):
    """Rosácea: anéis de pétalas em volta do medalhão."""
    cx = cy = 150
    s = ""
    for k in range(n):
        a = 2 * math.pi * k / n
        x, y = cx + 112 * math.cos(a), cy + 112 * math.sin(a)
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="{cores[k % len(cores)]}"/>'
    for k in range(n):
        a1, a2 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        s += f'<path d="M{cx + 52 * math.cos(a1):.1f} {cy + 52 * math.sin(a1):.1f}L{cx + 96 * math.cos(a1):.1f} {cy + 96 * math.sin(a1):.1f}A96 96 0 0 1 {cx + 96 * math.cos(a2):.1f} {cy + 96 * math.sin(a2):.1f}L{cx + 52 * math.cos(a2):.1f} {cy + 52 * math.sin(a2):.1f}Z" fill="{cores[(k + 2) % len(cores)]}"/>'
    return (f'<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg"><circle cx="150" cy="150" r="146" fill="{C["azulnoite"]}"/>'
            f'<g stroke="{CHUMBO}" stroke-width="3">{s}</g>{medalhao(cx, cy, 52, simb, "#f6ecd2", "#e8d7a8")}'
            f'<g clip-path="circle(146px at 150px 150px)">{brilho(uid, 300, 300)}</g>'
            f'<circle cx="150" cy="150" r="146" fill="none" stroke="{CHUMBO}" stroke-width="8"/><circle cx="150" cy="150" r="139" fill="none" stroke="{C["ouro"]}" stroke-width="2"/></svg>')

def geometrica(simb, cores, uid="g", w=200, h=300):
    """Ogiva moderna: poucos vidros grandes, em faixas, e o símbolo sobre um losango."""
    p = arco_path(w, h)
    faixas = ""
    n = 6
    for k in range(n):
        faixas += f'<rect x="{k * w / n:.1f}" y="0" width="{w / n:.1f}" height="{h}" fill="{cores[k % len(cores)]}"/>'
    faixas += "".join(f'<path d="M0 {y} L{w} {y - 40}" />' for y in range(60, h + 60, 70))
    return (f'<svg viewBox="-8 -8 {w + 16} {h + 16}" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="c{uid}"><path d="{p}"/></clipPath></defs>'
            f'<g clip-path="url(#c{uid})"><g stroke="{CHUMBO}" stroke-width="3">{faixas}</g>'
            f'<path d="M{w / 2} {h * .52 - 74}L{w / 2 + 74} {h * .52}L{w / 2} {h * .52 + 74}L{w / 2 - 74} {h * .52}Z" fill="#f6ecd2" stroke="{CHUMBO}" stroke-width="4"/>'
            f'<g transform="translate({w / 2 - 45} {h * .52 - 45}) scale(.75)" stroke="{CHUMBO}" stroke-width="3.4" stroke-linejoin="round">{SIMB[simb]}</g>{brilho(uid, w, h)}</g>'
            f'<path d="{p}" fill="none" stroke="{CHUMBO}" stroke-width="9"/></svg>')

TEMAS_VITRAL = {
 "veritas": ("chaves", [C["azulnoite"], C["cobalto"], C["rubi"], C["cobalto"], C["violeta"], C["rubi"]]),
 "defesa": ("escudo", [C["rubi"], C["cobalto"], C["rubi"], C["ambar"], C["cobalto"], C["rubi"]]),
 "reforma": ("livro", [C["violeta"], C["cobalto"], C["violeta"], C["ceu"], C["violeta"], C["cobalto"]]),
 "valores": ("coracao", [C["esmeralda"], C["ambar"], C["esmeralda"], C["ouro"], C["esmeralda"], C["ambar"]]),
 "libertacao": ("calice", [C["ambar"], C["rubi"], C["ouro"], C["ambar"], C["rubi"], C["laranja"]]),
 "maria": ("maria", [C["cobalto"], C["ceu"], C["cobalto"], C["branco"], C["ceu"], C["cobalto"]]),
}
