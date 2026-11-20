"""Segunda opção de papel de parede: igreja moderna (forro de madeira em duas águas, paredes de travertino,
um vitral alto e estreito atrás do altar com o grande ícone do Cristo Ressuscitado na frente, arcos laterais,
presbitério de mármore e bancos de madeira em leque, vistos do alto do coro)."""
import random
from vitral import CHUMBO, mosaico
from icone_cristo import icone

W, H = 390, 844
VX = 195
PAL = {
 "escuro": dict(fundo="#100c0b", madeira="#3a2214", madeira2="#2a170d", veio="#4e2e1a", borda="#5a361f", led="#ffd98a",
                pedra="#3a3128", pedra2="#453a2f", pedra3="#2f2720", junta="#241d17", luzParede="#ffcf8a", luzForca=.22,
                piso="#2a241f", piso2="#3a322a", onix="#7a4a24", banco="#4a2a16", bancoLuz="#8a5530", bancoSombra="#24140a",
                arco="#1c1712", arcoLuz="#5a4a3c", cadeira="#3a2416", toalha="#d8cfc0"),
 "claro": dict(fundo="#f6f1e7", madeira="#9a5a30", madeira2="#7a4220", veio="#b06a3a", borda="#c88850", led="#fff6d8",
               pedra="#e2d4bf", pedra2="#ecdfcc", pedra3="#d6c6ae", junta="#c9b79c", luzParede="#fff2d8", luzForca=.55,
               piso="#e8dcc8", piso2="#f4ecdd", onix="#b8834a", banco="#a0602e", bancoLuz="#d08a4c", bancoSombra="#6a3a18",
               arco="#cdbca2", arcoLuz="#f2e8d8", cadeira="#7a4a26", toalha="#ffffff"),
}
VIDRO = {"veritas": ["#1f6fd0", "#2fb3d8", "#1aa38a", "#3a8fe0", "#7fd0e8", "#1c4fb0"],
         "defesa": ["#c0392b", "#2c5fd0", "#f2c94c", "#a3192e", "#4ab0e0", "#e08a1a"],
         "reforma": ["#7a3cc0", "#2c5fd0", "#c43a7a", "#4ab0e0", "#f2c94c"],
         "valores": ["#2a9d6a", "#f2c94c", "#e08a1a", "#1d7a4c", "#4ab0e0"],
         "libertacao": ["#f2c94c", "#e08a1a", "#c0392b", "#a3192e", "#2c5fd0"]}


def cena(p_nome="escuro", tema="veritas", altura_visivel=.66, uid="m"):
    p = PAL[p_nome]
    cores = VIDRO[tema]
    rnd = random.Random(len(tema) * 11)
    apice, beiral = 26, 262           # topo do frontão e altura onde o forro encontra as paredes
    chao = 318                        # linha do piso no fundo
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMin slice"><defs>',
         f'<filter id="{uid}bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>',
         f'<filter id="{uid}bl2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>',
         f'<radialGradient id="{uid}spot"><stop offset="0" stop-color="{p["luzParede"]}" stop-opacity="{p["luzForca"]}"/><stop offset="1" stop-color="{p["luzParede"]}" stop-opacity="0"/></radialGradient>',
         f'<radialGradient id="{uid}brilho" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></radialGradient>',
         f'<linearGradient id="{uid}forro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["madeira2"]}"/><stop offset="1" stop-color="{p["madeira"]}"/></linearGradient>',
         f'<linearGradient id="{uid}vela" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["fundo"]}" stop-opacity="0"/><stop offset="{altura_visivel - .2}" stop-color="{p["fundo"]}" stop-opacity="0"/><stop offset="{altura_visivel}" stop-color="{p["fundo"]}" stop-opacity=".9"/><stop offset="{altura_visivel + .08}" stop-color="{p["fundo"]}" stop-opacity="1"/></linearGradient>',
         '</defs>']
    # parede de travertino: placas de tamanhos e tons variados
    o.append(f'<rect width="{W}" height="{chao + 10}" fill="{p["pedra"]}"/>')
    tons = [p["pedra"], p["pedra2"], p["pedra3"]]
    y = 0
    while y < chao:
        x, hh = rnd.choice((0, -14)), rnd.choice((26, 32, 38))
        while x < W:
            ww = rnd.choice((30, 38, 46))
            o.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" fill="{rnd.choice(tons)}" stroke="{p["junta"]}" stroke-width=".6" opacity=".9"/>')
            x += ww
        y += hh
    # luz quente dos refletores na parede
    for x, y, r in ((70, 190, 70), (320, 190, 70), (110, 120, 50), (280, 120, 50)):
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 1.4}" fill="url(#{uid}spot)"/>')
    # arcos laterais
    for lado in (-1, 1):
        cxa = VX + lado * 128
        o.append(f'<path d="M{cxa - 56} {chao}V{chao - 26}A56 56 0 0 1 {cxa + 56} {chao - 26}V{chao}Z" fill="{p["arco"]}"/>'
                 f'<path d="M{cxa - 56} {chao}V{chao - 26}A56 56 0 0 1 {cxa + 56} {chao - 26}V{chao}" fill="none" stroke="{p["arcoLuz"]}" stroke-width="5"/>')
    # vitral alto e estreito, com a ponta no frontão: colunas laterais com vãos arredondados e o centro em mosaico
    vx1, vx2, vb = VX - 62, VX + 62, chao - 22
    forma = f"M{vx1} {vb}V{apice + 70}L{VX} {apice}L{vx2} {apice + 70}V{vb}Z"
    o.append(f'<defs><clipPath id="{uid}v"><path d="{forma}"/></clipPath></defs><g clip-path="url(#{uid}v)">'
             f'<g transform="translate({vx1} {apice})" stroke="{CHUMBO}" stroke-width="1">{mosaico(vx2 - vx1, vb - apice, cores, rnd.randint(1, 99), passo=16, jit=5)}</g>'
             f'<rect x="{vx1}" y="{apice}" width="{vx2 - vx1}" height="{vb - apice}" fill="url(#{uid}brilho)"/>')
    # caixilhos: as colunas laterais com segmentos de cantos redondos
    for x in (vx1 + 4, vx2 - 26):
        yy = apice + 80
        while yy < vb - 20:
            o.append(f'<rect x="{x}" y="{yy}" width="22" height="44" rx="11" fill="none" stroke="{CHUMBO}" stroke-width="2.4"/>')
            yy += 50
    o.append(f'<path d="M{vx1 + 30} {apice + 40}V{vb}M{vx2 - 30} {apice + 40}V{vb}" stroke="{CHUMBO}" stroke-width="3"/></g>'
             f'<path d="{forma}" fill="none" stroke="{CHUMBO}" stroke-width="3"/>')
    # moldura do medalhão no alto do vitral: o símbolo do tema ou do bloco é posto por cima pelo app,
    # no centro (195, 100) com 44 de diâmetro
    o.append(f'<circle cx="{VX}" cy="100" r="22" fill="#f6ecd2" stroke="{CHUMBO}" stroke-width="2.4"/>')
    # forro de madeira em duas águas, com as tábuas e a fileira de luzinhas no beiral
    o.append(f'<path d="M0 0H{W}V{beiral}L{VX} {apice - 6}L0 {beiral}Z" fill="url(#{uid}forro)"/>')
    for k in range(1, 14):
        t = k / 14
        o.append(f'<path d="M{VX} {apice - 6 - t * 60:.1f}L{-10 - t * 60:.1f} {beiral - t * 240:.1f}M{VX} {apice - 6 - t * 60:.1f}L{W + 10 + t * 60:.1f} {beiral - t * 240:.1f}" stroke="{p["veio"]}" stroke-width=".8" opacity=".6"/>')
    o.append(f'<path d="M0 {beiral}L{VX} {apice - 6}L{W} {beiral}" fill="none" stroke="{p["borda"]}" stroke-width="7"/>')
    for k in range(1, 15):
        t = k / 15
        for lado in (-1, 1):
            x = VX + lado * VX * t
            yb = apice - 6 + (beiral - apice + 6) * t
            o.append(f'<circle cx="{x:.1f}" cy="{yb + 6:.1f}" r="1.3" fill="{p["led"]}"/>')
    # piso de mármore e o corredor central de ônix
    o.append(f'<path d="M0 {chao}H{W}V{H}H0Z" fill="{p["piso"]}"/>')
    for _ in range(18):
        y = chao + rnd.uniform(10, 500)
        o.append(f'<path d="M{rnd.uniform(-40, W):.0f} {y:.0f}q{rnd.uniform(30, 80):.0f} {rnd.uniform(-10, 10):.0f} {rnd.uniform(80, 160):.0f} {rnd.uniform(-6, 12):.0f}" fill="none" stroke="{p["piso2"]}" stroke-width="1.2" opacity=".7"/>')
    o.append(f'<path d="M{VX - 10} {chao + 46}H{VX + 10}L{VX + 34} {H}H{VX - 34}Z" fill="{p["onix"]}" opacity=".55"/>'
             f'<path d="M{VX - 4} {chao + 50}Q{VX + 8} {chao + 200} {VX - 10} {H}M{VX + 6} {chao + 60}Q{VX - 6} {chao + 260} {VX + 16} {H}" fill="none" stroke="{p["piso2"]}" stroke-width="1.4" opacity=".6"/>')
    # luz azul do vitral refletida no piso
    for _ in range(14):
        x, y = VX + rnd.uniform(-20, 110), chao + rnd.uniform(4, 90)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(10, 24):.0f}" ry="{rnd.uniform(4, 9):.0f}" fill="{rnd.choice(cores)}" opacity=".5" filter="url(#{uid}bl)"/>')
    # grande ícone do Cristo Ressuscitado diante do vitral (ver icone_cristo.py); o altar e as cadeiras ficam na frente
    o.append(icone(VX - 48, 116, 96, uid))
    # presbitério: degraus em meia-lua, altar, cadeiras, ambão e cruz processional
    o.append(f'<ellipse cx="{VX}" cy="{chao + 10}" rx="118" ry="34" fill="{p["piso2"]}" stroke="{p["junta"]}" stroke-width="1"/>'
             f'<ellipse cx="{VX}" cy="{chao + 4}" rx="92" ry="24" fill="{p["piso2"]}" stroke="{p["junta"]}" stroke-width="1"/>')
    for k in range(5):
        x = VX - 40 + k * 20
        o.append(f'<rect x="{x - 6}" y="{chao - 9}" width="12" height="13" rx="2" fill="{p["cadeira"]}"/><rect x="{x - 6}" y="{chao}" width="12" height="4" fill="{p["toalha"]}" opacity=".7"/>')
    o.append(f'<rect x="{VX - 26}" y="{chao + 6}" width="52" height="14" fill="{p["toalha"]}" stroke="{p["junta"]}" stroke-width=".8"/><path d="M{VX} {chao + 9}v8M{VX - 4} {chao + 12}h8" stroke="#b8261a" stroke-width="1.6"/>'
             f'<rect x="{VX - 74}" y="{chao - 6}" width="12" height="26" fill="{p["cadeira"]}"/><path d="M{VX - 68} {chao + 4}v6M{VX - 71} {chao + 6}h6" stroke="{p["toalha"]}" stroke-width="1.2"/>'
             f'<path d="M{VX + 66} {chao - 30}V{chao + 18}M{VX + 62} {chao - 24}h8" stroke="#c9a54a" stroke-width="1.6"/>')
    for k in range(5):
        x = VX - 44 + k * 22
        o.append(f'<rect x="{x - 7}" y="{chao + 26}" width="14" height="14" rx="2" fill="{p["cadeira"]}"/><rect x="{x - 7}" y="{chao + 36}" width="14" height="5" rx="1" fill="{p["toalha"]}" opacity=".8"/>')
    # bancos em leque: os de trás inclinados dos lados, os da frente retos, com o corredor no meio
    def banco(x1, y1, x2, y2, h):
        """Banco visto do alto: encosto (faixa escura), assento (faixa clara) e os pés de madeira nas pontas."""
        e, a = h * .45, h * .55
        pes = "".join(f'<path d="M{x:.1f} {y + e:.1f}v{a + h * .35:.1f}" stroke="{p["bancoSombra"]}" stroke-width="{max(1.2, h * .3):.1f}"/>' for x, y in ((x1 + h * .3, y1), (x2 - h * .3, y2)))
        return (f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}V{y2 + e:.1f}L{x1:.1f} {y1 + e:.1f}Z" fill="{p["banco"]}"/>'
                f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{p["bancoLuz"]}" stroke-width="{max(.8, h * .12):.1f}"/>'
                f'{pes}<path d="M{x1:.1f} {y1 + e:.1f}L{x2:.1f} {y2 + e:.1f}V{y2 + h:.1f}L{x1:.1f} {y1 + h:.1f}Z" fill="{p["bancoLuz"]}"/>'
                f'<path d="M{x1:.1f} {y1 + h:.1f}L{x2:.1f} {y2 + h:.1f}" stroke="{p["bancoSombra"]}" stroke-width="{max(1, h * .14):.1f}"/>')

    for lado in (-1, 1):
        for k in range(6):  # leque ao lado do presbitério
            s = 1 + k * .12
            yi = chao + 6 + k * 15
            xi = VX + lado * (128 + k * 6)
            xo = VX + lado * (210 + k * 18)
            o.append(banco(min(xi, xo), yi + (22 * s if lado < 0 else 0), max(xi, xo), yi + (0 if lado < 0 else 22 * s), 8 * s))
        for k in range(12):  # bancos da frente, retos
            s = .9 + k * .22
            y = chao + 76 + k * (14 + k * 3.2)
            a, b = VX + lado * (22 + k * 2), VX + lado * (130 + k * 16)
            o.append(banco(min(a, b), y, max(a, b), y, 9 * s))
    o.append(f'<ellipse cx="{VX}" cy="{chao + 120}" rx="110" ry="70" fill="{p["luzParede"]}" opacity=".12" filter="url(#{uid}bl2)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#{uid}vela)"/></svg>')
    return "".join(o)
