"""Símbolos dos vitrais, um por tema e por bloco (desenhados numa caixa 120×120, centro 60,60).
Cada um vira public/fundos/simbolos/<nome>.svg: um medalhão de vidro claro com o símbolo, que o app põe
sobre o vitral do fundo."""
import math
from vitral import C, CHUMBO, SIMB, chave

def _raios(cx, cy, r, passo=30, cor=None, w=4):
    return "".join(f'<path d="M{cx} {cy}L{cx + r * math.cos(math.radians(a)):.1f} {cy + r * math.sin(math.radians(a)):.1f}" stroke="{cor or C["ouro"]}" stroke-width="{w}"/>' for a in range(0, 360, passo))

def _coracao(cx, cy, s, cor):
    return f'<path transform="translate({cx} {cy}) scale({s})" d="M0 22C-16 11 -22 1 -22 -8a11 11 0 0 1 22 -3 11 11 0 0 1 22 3c0 9 -6 19 -22 30z" fill="{cor}"/>'

def _flor_lis(cx, cy, s, cor):
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M0 -46C-12 -30 -12 -12 0 6C12 -12 12 -30 0 -46Z" fill="{cor}"/>'
            f'<path d="M-3 2C-20 6 -34 -4 -30 -20C-40 -12 -40 6 -22 14H-3Z" fill="{cor}"/>'
            f'<path d="M3 2C20 6 34 -4 30 -20C40 -12 40 6 22 14H3Z" fill="{cor}"/>'
            f'<rect x="-22" y="12" width="44" height="9" rx="2" fill="{cor}"/>'
            f'<path d="M-9 21h18l-3 22h-12z" fill="{cor}"/><path d="M-9 30c-10 0-16 6-14 14 4-6 9-7 14-6zM9 30c10 0 16 6 14 14-4-6-9-7-14-6z" fill="{cor}"/></g>')

NOVOS = {
 # Maria: o M da Medalha Milagrosa, com a cruz sobre a barra e as doze estrelas
 "mariaMM": (f'<rect x="56" y="10" width="8" height="40" fill="{C["ouro"]}"/><rect x="34" y="44" width="52" height="7" fill="{C["ouro"]}"/>'
             f'<path d="M26 104V56h13l21 25 21-25h13v48H82V76L60 101 38 76v28z" fill="{C["cobalto"]}"/>'
             + "".join(f'<path transform="translate({60 + 53 * math.cos(math.radians(a)):.1f} {62 + 53 * math.sin(math.radians(a)):.1f})" d="M0 -5L1.4 -1.4 5 0 1.4 1.4 0 5 -1.4 1.4 -5 0 -1.4 -1.4Z" fill="{C["ouro"]}" stroke-width="1"/>' for a in range(-180, 180, 30))),
 # Igreja e o Papa: as chaves de Pedro cruzadas sob a tiara papal
 "tiara": (f'<g transform="translate(18 46) scale(.7)">{chave(C["ouro"], -38)}{chave(C["prata"], 38)}</g>'
           f'<path d="M36 58Q34 18 60 10Q86 18 84 58Z" fill="{C["branco"]}"/>'
           f'<path d="M37 52h46M37 39h46M42 26h36" stroke="{C["ouro"]}" stroke-width="5"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="{C["rubi"]}" stroke-width="1"/>' for y in (52, 39, 26) for x in (48, 60, 72))
           + f'<rect x="57" y="-2" width="6" height="14" fill="{C["ouro"]}"/><rect x="53" y="2" width="14" height="4" fill="{C["ouro"]}"/>'
           f'<path d="M40 58l-6 18M80 58l6 18" stroke="{C["rubi"]}" stroke-width="5"/>'),
 # Bíblia e Tradição: o livro aberto com a pomba do Espírito Santo
 "pombaLivro": (_raios(60, 40, 40, 30, w=3)
                + f'<path d="M14 66c16-8 32-8 44 2v40c-12-10-28-10-44-2z" fill="{C["branco"]}"/><path d="M106 66c-16-8-32-8-44 2v40c12-10 28-10 44-2z" fill="{C["claro"]}"/>'
                f'<path d="M24 78h24M24 86h24M72 78h24M72 86h24" stroke="{C["cobalto"]}" stroke-width="2"/>'
                f'<path d="M30 34c10-1 18-6 24-16 5 7 5 14 1 19l28-5c-6 12-18 18-30 20l-7 12-4-11c-6-2-10-9-12-19z" fill="{C["branco"]}"/>'),
 # Cristo: o Chi-Rho com Alfa e Ômega
 "chiRho": (f'<rect x="30" y="56" width="60" height="10" rx="2" fill="{C["ouro"]}" transform="rotate(42 60 61)"/><rect x="30" y="56" width="60" height="10" rx="2" fill="{C["ouro"]}" transform="rotate(-42 60 61)"/>'
            f'<rect x="54" y="12" width="12" height="94" fill="{C["rubi"]}"/><path d="M66 12h10a17 17 0 0 1 0 34H66V35h10a6 6 0 0 0 0-12H66z" fill="{C["rubi"]}"/>'
            f'<text x="20" y="74" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="24" fill="{C["cobalto"]}" stroke="none">Α</text>'
            f'<text x="100" y="74" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="24" fill="{C["cobalto"]}" stroke="none">Ω</text>'),
 # Imagens, santos e relíquias: a coroa e a palma dos mártires
 "palmaCoroa": (f'<path d="M30 44l6-26 12 14 12-22 12 22 12-14 6 26z" fill="{C["ouro"]}"/><rect x="30" y="44" width="60" height="9" fill="{C["ouro"]}"/>'
                f'<circle cx="60" cy="48" r="3" fill="{C["rubi"]}"/><circle cx="44" cy="48" r="2.4" fill="{C["cobalto"]}"/><circle cx="76" cy="48" r="2.4" fill="{C["cobalto"]}"/>'
                f'<g transform="rotate(28 60 84)"><path d="M60 116V60" stroke="{C["esmeralda"]}" stroke-width="4"/>'
                + "".join(f'<path d="M60 {y}q{-L} {-L * .35:.1f} {-L - 4} {-L * .9:.1f}q{L * .55:.1f} {L * .1:.1f} {L + 4} {L * .9:.1f}zM60 {y}q{L} {-L * .35:.1f} {L + 4} {-L * .9:.1f}q{-L * .55:.1f} {L * .1:.1f} {-L - 4} {L * .9:.1f}z" fill="{C["esmeralda"]}" stroke-width="1.6"/>' for y, L in ((112, 16), (102, 18), (92, 18), (82, 16), (72, 12)))
                + f'<path d="M60 62c-4-6-4-12 0-16 4 4 4 10 0 16z" fill="{C["esmeralda"]}"/></g>'),
 # Solas (Solus Christus): o Bom Pastor, com o cajado e a ovelha
 "bomPastor": (f'<path d="M34 110V42Q34 16 54 16Q72 16 72 34" fill="none" stroke="{C["ouro"]}" stroke-width="7" stroke-linecap="round"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C["branco"]}"/>' for x, y, r in ((66, 78, 13), (80, 72, 13), (94, 80, 12), (70, 92, 12), (86, 94, 12)))
               + f'<ellipse cx="104" cy="70" rx="8" ry="10" fill="#3a3530"/><circle cx="106" cy="68" r="1.6" fill="#fff" stroke="none"/>'
               f'<rect x="68" y="100" width="5" height="14" fill="#3a3530"/><rect x="88" y="102" width="5" height="12" fill="#3a3530"/>'),
 # Virtudes teologais: a cruz (fé), a âncora (esperança) e o coração (caridade)
 "ancora": (f'<circle cx="60" cy="16" r="8" fill="none" stroke="{C["prata"]}" stroke-width="5"/><rect x="56" y="22" width="8" height="82" fill="{C["prata"]}"/>'
            f'<rect x="34" y="34" width="52" height="8" fill="{C["prata"]}"/>'
            f'<path d="M24 78Q26 106 60 106Q94 106 96 78" fill="none" stroke="{C["prata"]}" stroke-width="8"/><path d="M16 82l10-10 6 12zM104 82l-10-10-6 12z" fill="{C["prata"]}"/>'
            + _coracao(60, 70, .95, C["rubi"])),
 # Virtudes cardeais: a balança da justiça
 "balanca": (f'<circle cx="60" cy="16" r="6" fill="{C["ouro"]}"/><rect x="57" y="20" width="6" height="80" fill="{C["ouro"]}"/><rect x="18" y="30" width="84" height="6" rx="2" fill="{C["ouro"]}"/>'
             f'<path d="M22 36L12 72M22 36L32 72M98 36L88 72M98 36L108 72" stroke="{CHUMBO}" stroke-width="1.6" fill="none"/>'
             f'<path d="M6 72h32a16 10 0 0 1 -32 0zM82 72h32a16 10 0 0 1 -32 0z" fill="{C["ouro"]}"/><path d="M38 108h44l-6 -10H44z" fill="{C["ouro"]}"/>'),
 # Vida, matrimônio e família: as alianças entrelaçadas sob a cruz
 "aliancas": (f'<rect x="56" y="8" width="8" height="34" fill="{C["rubi"]}"/><rect x="45" y="18" width="30" height="8" fill="{C["rubi"]}"/>'
              f'<circle cx="47" cy="76" r="20" fill="none" stroke="{C["ouro"]}" stroke-width="8"/><circle cx="73" cy="76" r="20" fill="none" stroke="{C["ouro"]}" stroke-width="8"/>'
              f'<path d="M62 60a20 20 0 0 1 0 32" fill="none" stroke="{C["ouro"]}" stroke-width="8"/>'),
 # Teologia da Libertação · o que a Igreja ensina: a Medalha de São Bento
 "saoBento": (f'<circle cx="60" cy="60" r="48" fill="{C["ouro"]}"/><circle cx="60" cy="60" r="40" fill="#f3d98a"/>'
              f'<path d="M54 22h12v32h32v12H66v32H54V66H22V54h32z" fill="{CHUMBO}"/>'
              + "".join(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="15" fill="{C["rubi"]}" stroke="none">{l}</text>' for l, x, y in (("C", 37, 46), ("S", 83, 46), ("P", 37, 88), ("B", 83, 88)))),
 # Teologia da Libertação · os erros corrigidos: a Cruz de Santiago
 "santiago": (f'<path d="M55 40h10v52l-5 18-5-18z" fill="{C["rubi"]}"/><rect x="26" y="40" width="68" height="9" fill="{C["rubi"]}"/>'
              f'<path d="M60 8c-8 8-8 18 0 28 8-10 8-20 0-28zM48 30c-6 0-10 6-6 12h12zM72 30c6 0 10 6 6 12H66z" fill="{C["rubi"]}"/>'
              f'<path d="M14 44c8-8 18-8 26 0-8 8-18 8-26 0zM106 44c-8-8-18-8-26 0 8 8 18 8 26 0z" fill="{C["rubi"]}"/>'),
 # Teologia da Libertação · Eucaristia, ritos e música: a custódia
 "custodia": (_raios(60, 44, 40, 20, w=3) + f'<circle cx="60" cy="44" r="22" fill="{C["ouro"]}"/><circle cx="60" cy="44" r="15" fill="{C["branco"]}"/>'
              f'<path d="M60 36v16M53 43h14" stroke="{C["ambar"]}" stroke-width="3"/><rect x="56" y="66" width="8" height="26" fill="{C["ouro"]}"/>'
              f'<ellipse cx="60" cy="80" rx="9" ry="5" fill="{C["ouro"]}"/><path d="M34 110c4-14 48-14 52 0z" fill="{C["ouro"]}"/>'),
 # Tema Teologia da Libertação: a flor-de-lis
 "florLis": _flor_lis(60, 58, 1.15, C["ouro"]),
}
SIMB.update(NOVOS)

def medalhao(nome):
    """SVG do medalhão: vidro claro em setores, o símbolo e a moldura (diâmetro 44 na cena)."""
    setores = ""
    for k in range(12):
        a1, a2 = math.radians(k * 30), math.radians(k * 30 + 30)
        setores += f'<path d="M30 30L{30 + 28 * math.cos(a1):.2f} {30 + 28 * math.sin(a1):.2f}A28 28 0 0 1 {30 + 28 * math.cos(a2):.2f} {30 + 28 * math.sin(a2):.2f}Z" fill="{"#f6ecd2" if k % 2 else "#ece0bf"}"/>'
    s = 46 / 120
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60">{setores}'
            f'<g transform="translate({30 - 60 * s:.2f} {30 - 60 * s:.2f}) scale({s:.4f})" stroke="{CHUMBO}" stroke-width="3.4" stroke-linejoin="round">{SIMB[nome]}</g>'
            f'<circle cx="30" cy="30" r="28" fill="none" stroke="{CHUMBO}" stroke-width="2.4"/><circle cx="30" cy="30" r="29.3" fill="none" stroke="{C["ouro"]}" stroke-width="1.2"/></svg>')

# nome do arquivo -> símbolo: os quatro temas, o início e cada bloco (id do bloco em src/dados/temas.json)
USO = {
 "veritas": "chaves", "defesa": "escudo", "reforma": "livro", "valores": "coracao", "libertacao": "florLis",
 "maria": "mariaMM", "igreja": "tiara", "escritura": "pombaLivro", "sacramentos": "calice", "cristo": "chiRho", "imagens": "palmaCoroa",
 "solas": "bomPastor", "teologais": "ancora", "cardeais": "balanca", "vida": "aliancas",
 "libertacao-bloco": "saoBento", "desvios": "santiago", "liturgia": "custodia",
}
