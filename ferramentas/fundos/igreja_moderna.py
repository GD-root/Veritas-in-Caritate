"""Segunda opção de papel de parede: igreja moderna (forro de madeira em duas águas, paredes de travertino,
um vitral alto e estreito atrás do altar com o grande ícone do Cristo Ressuscitado na frente, arcos laterais,
presbitério de mármore e bancos de madeira em leque, vistos do alto do coro)."""
import random
from vitral import CHUMBO, mosaico

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


def icone(x0, y0, w, h, uid):
    """Ícone do Cristo Ressuscitado e Rei: túnica branca, manto vermelho, coroa e auréola com a cruz,
    a mão direita erguida segurando a cruz-estandarte e a esquerda no peito, sobre fundo dourado com folhas."""
    cx = x0 + w / 2
    k = "#5a2410"
    rnd = random.Random(7)
    g = [f'<defs><linearGradient id="{uid}ic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbeed6"/><stop offset=".55" stop-color="#f4cf98"/><stop offset="1" stop-color="#e2a35e"/></linearGradient>'
         f'<linearGradient id="{uid}manto" x1="0" x2="1"><stop offset="0" stop-color="#9a1e12"/><stop offset=".3" stop-color="#e0461f"/><stop offset=".55" stop-color="#f06a2a"/><stop offset=".8" stop-color="#d63a18"/><stop offset="1" stop-color="#8a1a10"/></linearGradient>'
         f'<linearGradient id="{uid}tun" x1="0" x2="1"><stop offset="0" stop-color="#e8ddd0"/><stop offset=".5" stop-color="#fffaf2"/><stop offset="1" stop-color="#dcd0c0"/></linearGradient>'
         f'<radialGradient id="{uid}aur"><stop offset=".6" stop-color="#f6d77a"/><stop offset="1" stop-color="#c9922c"/></radialGradient>'
         f'<clipPath id="{uid}icc"><rect x="{x0}" y="{y0}" width="{w}" height="{h}"/></clipPath></defs>',
         f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#{uid}ic)"/>',
         f'<g clip-path="url(#{uid}icc)">']
    # folhas e flores pelo fundo, mais densas nas laterais
    for _ in range(90):
        lado = rnd.choice((-1, 1))
        x = cx + lado * rnd.uniform(w * .18, w * .55)
        y = y0 + rnd.uniform(6, h - 10)
        cor = rnd.choice(["#e0702a", "#f29a3a", "#c8501e", "#e8b04a", "#8aa05a", "#d06a3a"])
        g.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rnd.uniform(1.4, 3.2):.1f}" ry="{rnd.uniform(1, 2.2):.1f}" transform="rotate({rnd.randint(0, 180)} {x:.1f} {y:.1f})" fill="{cor}" opacity=".8"/>')
    # chão do ícone
    g.append(f'<path d="M{x0} {y0 + h - 22}Q{cx} {y0 + h - 30} {x0 + w} {y0 + h - 22}V{y0 + h}H{x0}Z" fill="#c8843e" opacity=".75"/>')
    # anjinhos nos cantos do alto
    for lado in (-1, 1):
        ax, ay = cx + lado * 30, y0 + 22
        g.append(f'<path d="M{ax} {ay}q{lado * 8} -8 {lado * 14} -2q{lado * -4} 2 {lado * -6} 8z" fill="#f6ead4" stroke="#b07a3a" stroke-width=".5"/><circle cx="{ax}" cy="{ay - 2}" r="2.2" fill="#e8c49a"/>')
    hy = y0 + 46  # centro da cabeça
    # cruz-estandarte na mão direita (à esquerda de quem olha)
    sx = cx - 18
    g.append(f'<path d="M{sx} {y0 + 8}V{y0 + h - 18}" stroke="#a8742a" stroke-width="2"/><path d="M{sx - 6} {y0 + 18}H{sx + 6}M{sx - 4} {y0 + 12}H{sx + 4}" stroke="#a8742a" stroke-width="1.8"/>')
    # manto vermelho: cobre os ombros e cai largo dos dois lados, aberto no meio
    g.append(f'<path d="M{cx - 11} {hy + 10}Q{cx} {hy + 7} {cx + 12} {hy + 10}Q{cx + 22} {hy + 14} {cx + 25} {hy + 40}Q{cx + 34} {hy + 90} {cx + 40} {hy + 128}Q{cx + 22} {hy + 136} {cx + 8} {hy + 128}L{cx + 6} {hy + 30}L{cx - 4} {hy + 30}L{cx - 14} {hy + 130}Q{cx - 30} {hy + 136} {cx - 40} {hy + 124}Q{cx - 30} {hy + 70} {cx - 24} {hy + 30}Q{cx - 21} {hy + 14} {cx - 11} {hy + 10}Z" fill="url(#{uid}manto)" stroke="{k}" stroke-width=".7"/>'
             f'<path d="M{cx + 20} {hy + 30}Q{cx + 26} {hy + 80} {cx + 32} {hy + 126}M{cx + 14} {hy + 40}Q{cx + 16} {hy + 90} {cx + 18} {hy + 128}M{cx - 20} {hy + 40}Q{cx - 26} {hy + 86} {cx - 32} {hy + 124}M{cx - 13} {hy + 50}Q{cx - 16} {hy + 90} {cx - 22} {hy + 128}" fill="none" stroke="#8a1a10" stroke-width=".8" opacity=".7"/>'
             f'<path d="M{cx + 24} {hy + 60}q3 4 1 8M{cx - 28} {hy + 90}q-2 4 0 8M{cx + 30} {hy + 100}q2 3 0 7" fill="none" stroke="#f6c36a" stroke-width=".8"/>')
    # túnica branca com a faixa dourada
    g.append(f'<path d="M{cx - 8} {hy + 12}Q{cx} {hy + 10} {cx + 9} {hy + 12}L{cx + 10} {hy + 60}Q{cx + 12} {hy + 100} {cx + 9} {hy + 128}L{cx - 12} {hy + 128}Q{cx - 13} {hy + 96} {cx - 10} {hy + 60}Z" fill="url(#{uid}tun)" stroke="{k}" stroke-width=".6"/>'
             f'<path d="M{cx + 3} {hy + 14}V{hy + 128}" stroke="#d9a94a" stroke-width="2.2"/><path d="M{cx - 6} {hy + 70}q2 30 0 56M{cx + 7} {hy + 70}q1 28 0 56" fill="none" stroke="#c9bba8" stroke-width=".7"/>')
    # braço direito erguido (manga branca) e a mão na cruz; mão esquerda no peito
    g.append(f'<path d="M{cx - 10} {hy + 14}Q{cx - 18} {hy + 10} {sx + 1} {hy + 2}L{sx + 5} {hy + 4}Q{cx - 12} {hy + 18} {cx - 7} {hy + 22}Z" fill="url(#{uid}tun)" stroke="{k}" stroke-width=".6"/>'
             f'<ellipse cx="{sx + 1}" cy="{hy}" rx="2.6" ry="3.2" fill="#d8a878" stroke="{k}" stroke-width=".5"/>'
             f'<path d="M{cx + 12} {hy + 16}Q{cx + 10} {hy + 26} {cx + 3} {hy + 26}" fill="none" stroke="#e0461f" stroke-width="4.5" stroke-linecap="round"/>'
             f'<ellipse cx="{cx + 2}" cy="{hy + 25}" rx="3" ry="2.4" fill="#d8a878" stroke="{k}" stroke-width=".5"/>')
    # pés descalços
    g.append(f'<path d="M{cx - 9} {hy + 128}q-3 4 -1 6h7l-1 -6zM{cx + 2} {hy + 128}q1 5 4 6h5q-2 -3 -4 -6z" fill="#d8a878" stroke="{k}" stroke-width=".5"/>')
    # auréola com a cruz, cabelo, rosto, barba e coroa
    g.append(f'<circle cx="{cx}" cy="{hy}" r="11.5" fill="url(#{uid}aur)" stroke="#a8742a" stroke-width=".7"/>'
             f'<path d="M{cx} {hy - 11.5}V{hy - 7}M{cx - 11.5} {hy}H{cx - 7}M{cx + 11.5} {hy}H{cx + 7}" stroke="#b8261a" stroke-width="2"/>'
             f'<path d="M{cx - 6} {hy - 4}Q{cx} {hy - 9} {cx + 6} {hy - 4}Q{cx + 8} {hy + 6} {cx + 6} {hy + 12}Q{cx + 3} {hy + 9} {cx + 4} {hy + 4}H{cx - 4}Q{cx - 3} {hy + 9} {cx - 6} {hy + 12}Q{cx - 8} {hy + 6} {cx - 6} {hy - 4}Z" fill="#4a2a16"/>'
             f'<ellipse cx="{cx}" cy="{hy + 1}" rx="4.4" ry="5.6" fill="#e2b488" stroke="{k}" stroke-width=".4"/>'
             f'<path d="M{cx - 4} {hy + 2}Q{cx - 4} {hy + 9} {cx} {hy + 10}Q{cx + 4} {hy + 9} {cx + 4} {hy + 2}Q{cx + 2} {hy + 5} {cx} {hy + 5}Q{cx - 2} {hy + 5} {cx - 4} {hy + 2}Z" fill="#5a3418"/>'
             f'<path d="M{cx - 2.6} {hy - .4}h1.6M{cx + 1} {hy - .4}h1.6" stroke="#2a1a10" stroke-width=".8"/><path d="M{cx} {hy}v2.4" stroke="#b07a52" stroke-width=".5"/>'
             f'<path d="M{cx - 5.5} {hy - 4.5}L{cx - 5} {hy - 9}L{cx - 2.6} {hy - 6.4}L{cx} {hy - 10}L{cx + 2.6} {hy - 6.4}L{cx + 5} {hy - 9}L{cx + 5.5} {hy - 4.5}Z" fill="#e8b83a" stroke="#8a5a14" stroke-width=".5"/>'
             f'<text x="{cx - 15}" y="{hy - 10}" font-family="serif" font-size="5" fill="#a3192e" text-anchor="middle">IC</text><text x="{cx + 15}" y="{hy - 10}" font-family="serif" font-size="5" fill="#a3192e" text-anchor="middle">XC</text>')
    g.append('</g>')
    g.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#b07a3a" stroke-width=".8"/>')
    return "".join(g)


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
    # presbitério: degraus em meia-lua, altar, cadeiras, ambão e cruz processional
    o.append(f'<ellipse cx="{VX}" cy="{chao + 10}" rx="118" ry="34" fill="{p["piso2"]}" stroke="{p["junta"]}" stroke-width="1"/>'
             f'<ellipse cx="{VX}" cy="{chao + 4}" rx="92" ry="24" fill="{p["piso2"]}" stroke="{p["junta"]}" stroke-width="1"/>')
    for k in range(5):
        x = VX - 40 + k * 20
        o.append(f'<rect x="{x - 6}" y="{chao - 18}" width="12" height="16" rx="2" fill="{p["cadeira"]}"/><rect x="{x - 6}" y="{chao - 6}" width="12" height="4" fill="{p["toalha"]}" opacity=".7"/>')
    o.append(f'<rect x="{VX - 26}" y="{chao}" width="52" height="16" fill="{p["toalha"]}" stroke="{p["junta"]}" stroke-width=".8"/><path d="M{VX} {chao + 4}v8M{VX - 4} {chao + 7}h8" stroke="#b8261a" stroke-width="1.6"/>'
             f'<rect x="{VX - 74}" y="{chao - 6}" width="12" height="26" fill="{p["cadeira"]}"/><path d="M{VX - 68} {chao + 4}v6M{VX - 71} {chao + 6}h6" stroke="{p["toalha"]}" stroke-width="1.2"/>'
             f'<path d="M{VX + 66} {chao - 30}V{chao + 18}M{VX + 62} {chao - 24}h8" stroke="#c9a54a" stroke-width="1.6"/>')
    for k in range(5):
        x = VX - 44 + k * 22
        o.append(f'<rect x="{x - 7}" y="{chao + 26}" width="14" height="14" rx="2" fill="{p["cadeira"]}"/><rect x="{x - 7}" y="{chao + 36}" width="14" height="5" rx="1" fill="{p["toalha"]}" opacity=".8"/>')
    # grande ícone do Cristo Ressuscitado diante do vitral
    o.append(icone(VX - 46, 128, 92, 196, uid))
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
