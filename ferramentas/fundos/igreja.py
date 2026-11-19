"""Nave com bancos: grande vitral gótico ao fundo com o crucifixo na frente, raios de luz, arcadas laterais,
bancos de madeira dos dois lados e as cores do vitral refletidas no piso do corredor central."""
import math, random
from vitral import SIMB, CHUMBO, mosaico

W, H = 390, 844
V = (195, 318)  # ponto de fuga: base do altar
PAL = {
 "escuro": dict(fundo="#100c0b", pedra="#1c1714", pedra2="#2a221d", pedraLuz="#4a3c32", madeira="#2e1a10", madeiraLuz="#6a4226", piso="#120e0c", luz="#ffe2a8", cruz="#3a2414", corpo="#e9d6b6", contorno="#1a0f08"),
 "claro": dict(fundo="#f6f1e7", pedra="#b8a58a", pedra2="#cdbb9e", pedraLuz="#e8dcc6", madeira="#6a4228", madeiraLuz="#a8724a", piso="#d8cbb4", luz="#fff6dc", cruz="#4a2e1a", corpo="#ead9bc", contorno="#2a1a0e"),
}
VIDRO = {"veritas": ["#2c5fd0", "#e08a1a", "#c0392b", "#f2c94c", "#2a9d6a", "#7a3cc0", "#4ab0e0"],
         "defesa": ["#c0392b", "#2c5fd0", "#f2c94c", "#a3192e", "#4ab0e0", "#e08a1a"],
         "reforma": ["#7a3cc0", "#2c5fd0", "#c43a7a", "#4ab0e0", "#f2c94c"],
         "valores": ["#2a9d6a", "#f2c94c", "#e08a1a", "#1d7a4c", "#4ab0e0"],
         "libertacao": ["#f2c94c", "#e08a1a", "#c0392b", "#a3192e", "#2c5fd0"],
         "maria": ["#2c5fd0", "#4ab0e0", "#9ab8ea", "#f3e6c4", "#1c3a9a", "#f2c94c"]}

def cena(p_nome="escuro", tema="veritas", altura_visivel=.66, uid="x"):
    p = PAL[p_nome]
    cores = VIDRO[tema]
    simb = {"veritas": "chaves", "defesa": "escudo", "reforma": "livro", "valores": "coracao", "libertacao": "calice", "maria": "maria"}[tema]
    rnd = random.Random(len(tema) * 7)
    vx, vy = V
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMin slice"><defs>',
         f'<filter id="{uid}bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>',
         f'<filter id="{uid}bl2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>',
         f'<linearGradient id="{uid}raio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["luz"]}" stop-opacity=".45"/><stop offset="1" stop-color="{p["luz"]}" stop-opacity="0"/></linearGradient>',
         f'<radialGradient id="{uid}brilho" cx="50%" cy="45%" r="55%"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></radialGradient>',
         f'<radialGradient id="{uid}chama"><stop offset="0" stop-color="#fff6d0"/><stop offset=".4" stop-color="#ffc54a" stop-opacity=".9"/><stop offset="1" stop-color="#ff9a1f" stop-opacity="0"/></radialGradient>',
         f'<linearGradient id="{uid}vela" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["fundo"]}" stop-opacity="0"/><stop offset="{altura_visivel - .2}" stop-color="{p["fundo"]}" stop-opacity="0"/><stop offset="{altura_visivel}" stop-color="{p["fundo"]}" stop-opacity=".9"/><stop offset="{altura_visivel + .08}" stop-color="{p["fundo"]}" stop-opacity="1"/></linearGradient>',
         f'</defs><rect width="{W}" height="{H}" fill="{p["pedra"]}"/>']
    # abóbada: arcos transversais (do fundo para a frente)
    for s in (.32, .45, .62, .85, 1.15):
        half = 120 + 220 * (s - .32)
        top = vy - 240 * s - 30
        o.append(f'<path d="M{vx - half:.1f} {vy - 120 * s:.1f}Q{vx - half:.1f} {top:.1f} {vx:.1f} {top - 40 * s:.1f}Q{vx + half:.1f} {top:.1f} {vx + half:.1f} {vy - 120 * s:.1f}" fill="none" stroke="{p["pedra2"]}" stroke-width="{10 * s:.1f}"/>')
    # parede do fundo e o grande vitral
    o.append(f'<rect x="{vx - 110}" y="40" width="220" height="{vy - 40}" fill="{p["pedra2"]}"/>')
    wx1, wx2, wt, wb = vx - 66, vx + 66, 64, vy - 34
    arco = f"M{wx1} {wb}V150Q{wx1} 82 {vx} {wt}Q{wx2} 82 {wx2} 150V{wb}Z"
    o.append(f'<defs><clipPath id="{uid}w"><path d="{arco}"/></clipPath></defs><g clip-path="url(#{uid}w)">'
             f'<g transform="translate({wx1} {wt})" stroke="{CHUMBO}" stroke-width="1.2">{mosaico(wx2 - wx1, wb - wt, cores, rnd.randint(1, 99), passo=11, jit=3)}</g>'
             f'<rect x="{wx1}" y="{wt}" width="{wx2 - wx1}" height="{wb - wt}" fill="url(#{uid}brilho)"/></g>')
    for k in range(1, 5):  # mainéis
        x = wx1 + k * (wx2 - wx1) / 5
        o.append(f'<path d="M{x:.1f} 150V{wb}" stroke="{CHUMBO}" stroke-width="3"/>')
    for k in range(3):  # rendilhado do topo
        o.append(f'<circle cx="{vx + (k - 1) * 30}" cy="{126 - (k % 2) * 18}" r="13" fill="none" stroke="{CHUMBO}" stroke-width="3"/>')
    o.append(f'<path d="{arco}" fill="none" stroke="{p["pedraLuz"]}" stroke-width="5"/>')
    # medalhão do tema no alto do vitral
    s = 50 / 120
    o.append(f'<circle cx="{vx}" cy="100" r="22" fill="#f6ecd2" stroke="{CHUMBO}" stroke-width="2.4"/><g transform="translate({vx - 25} 75) scale({s:.3f})" stroke="{CHUMBO}" stroke-width="6" stroke-linejoin="round">{SIMB[simb]}</g>')
    # grande crucifixo diante do vitral, com Cristo crucificado
    cy0, cy1, bx = 128, vy - 20, 170          # topo e pé da cruz, altura da trave
    o.append(f'<path d="M{vx - 4.5} {cy0}h9v{cy1 - cy0}h-9zM{vx - 40} {bx - 4}h80v9h-80z" fill="{p["cruz"]}" stroke="{p["contorno"]}" stroke-width="1"/>')
    o.append(f'<rect x="{vx - 11}" y="{cy0 + 4}" width="22" height="10" rx="1.5" fill="{p["corpo"]}" stroke="{p["contorno"]}" stroke-width="1"/>'
             f'<text x="{vx}" y="{cy0 + 11.6}" text-anchor="middle" font-family="Georgia,serif" font-size="7" font-weight="700" fill="{p["contorno"]}">INRI</text>')
    c, k = p["corpo"], p["contorno"]
    def membro(d, w):  # traço com contorno escuro por baixo
        return f'<path d="{d}" fill="none" stroke="{k}" stroke-width="{w + 2}" stroke-linecap="round" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    o.append(f'<circle cx="{vx + 1}" cy="{bx + 13}" r="9.5" fill="none" stroke="#e8c35a" stroke-width="2"/>')  # auréola
    o.append(membro(f"M{vx - 34} {bx + 1}Q{vx - 20} {bx + 9} {vx - 6} {bx + 22}", 4.6))  # braço esquerdo
    o.append(membro(f"M{vx + 34} {bx + 1}Q{vx + 20} {bx + 9} {vx + 6} {bx + 22}", 4.6))  # braço direito
    o.append(f'<path d="M{vx - 7} {bx + 21}Q{vx} {bx + 18} {vx + 7} {bx + 21}L{vx + 5} {bx + 58}H{vx - 5}Z" fill="{c}" stroke="{k}" stroke-width="1.2"/>')  # tronco
    o.append(f'<path d="M{vx - 4} {bx + 30}q4 3 8 0M{vx - 3.5} {bx + 38}q3.5 2.5 7 0" fill="none" stroke="{k}" stroke-width=".7" opacity=".6"/>')
    o.append(membro(f"M{vx - 2.5} {bx + 66}Q{vx - 4} {bx + 88} {vx - 1} {bx + 108}", 4.4))  # pernas juntas
    o.append(membro(f"M{vx + 2.5} {bx + 66}Q{vx + 4} {bx + 88} {vx + 1} {bx + 108}", 4.4))
    o.append(f'<path d="M{vx - 8} {bx + 56}H{vx + 8}L{vx + 10} {bx + 70}L{vx + 2} {bx + 67}L{vx - 3} {bx + 72}L{vx - 9} {bx + 68}Z" fill="#fbf6ea" stroke="{k}" stroke-width="1"/>')  # perizônio
    o.append(f'<circle cx="{vx + 2}" cy="{bx + 13}" r="5.6" fill="{c}" stroke="{k}" stroke-width="1.2"/>'
             f'<path d="M{vx - 3} {bx + 10}q5 -4 10 0" fill="none" stroke="#5a3a1c" stroke-width="1.6"/>')  # cabeça inclinada, coroa de espinhos
    for x, y in ((vx - 34, bx + 1), (vx + 34, bx + 1), (vx, bx + 106)):
        o.append(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{k}"/>')  # cravos
    # altar, degraus e castiçais
    o.append(f'<rect x="{vx - 38}" y="{vy - 30}" width="76" height="22" fill="{p["madeira"]}" stroke="{p["pedraLuz"]}" stroke-width="1"/><rect x="{vx - 40}" y="{vy - 32}" width="80" height="4" fill="#efe6d2"/>'
             f'<path d="M{vx - 60} {vy - 8}h120l8 8h-136z" fill="{p["pedraLuz"]}"/>')
    for dx in (-76, -50, 50, 76):
        o.append(f'<path d="M{vx + dx} {vy - 6}v-26" stroke="#c9a54a" stroke-width="2"/><circle cx="{vx + dx}" cy="{vy - 36}" r="6" fill="url(#{uid}chama)"/>')
    # arcadas laterais com colunas e janelinhas
    for lado in (-1, 1):
        for k, s in enumerate((.45, .62, .85, 1.15, 1.6)):
            x = vx + lado * (115 + 230 * (s - .45))
            w = 14 * s
            top = vy - 290 * s
            o.append(f'<rect x="{x - w / 2:.1f}" y="{top:.1f}" width="{w:.1f}" height="{H}" fill="{p["pedra2"]}"/><rect x="{x - w / 2 + w * .6:.1f}" y="{top:.1f}" width="{w * .25:.1f}" height="{H}" fill="{p["pedraLuz"]}" opacity=".6"/>')
            if k < 4:
                s2 = (.62, .85, 1.15, 1.6)[k]
                x2 = vx + lado * (115 + 230 * (s2 - .45))
                yb = vy - 70 * (s + s2) / 2
                o.append(f'<path d="M{x:.1f} {vy - 140 * s:.1f}Q{x:.1f} {vy - 220 * s2:.1f} {(x + x2) / 2:.1f} {vy - 240 * s2:.1f}Q{x2:.1f} {vy - 220 * s2:.1f} {x2:.1f} {vy - 140 * s2:.1f}" fill="none" stroke="{p["pedraLuz"]}" stroke-width="{3 * s:.1f}" opacity=".7"/>')
                # janelinha colorida no alto, entre as colunas
                wx, ww = (x + x2) / 2 - 5 * s, 10 * s
                o.append(f'<rect x="{wx:.1f}" y="{vy - 250 * s2:.1f}" width="{ww:.1f}" height="{60 * s:.1f}" rx="{5 * s:.1f}" fill="{cores[k % len(cores)]}" opacity=".85"/>')
                # arandela acesa
                o.append(f'<circle cx="{x:.1f}" cy="{vy - 20 * s:.1f}" r="{7 * s:.1f}" fill="url(#{uid}chama)"/>')
    # raios de luz do vitral até o chão
    for a, b in ((vx - 40, vx + 70), (vx + 20, vx + 150), (vx - 70, vx - 10)):
        o.append(f'<polygon points="{a},{wt + 40} {a + 22},{wt + 40} {b + 50},{vy + 200} {b - 10},{vy + 200}" fill="url(#{uid}raio)" opacity=".7"/>')
    # piso
    o.append(f'<path d="M0 {vy}H{W}V{H}H0Z" fill="{p["piso"]}"/>')
    # cores do vitral refletidas no corredor central
    for k in range(26):
        t = rnd.random() ** .8
        y = vy + 20 + t * 320
        half = 20 + t * 110
        x = vx + rnd.uniform(-half, half) * .8
        o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{8 + t * 26:.1f}" ry="{3 + t * 9:.1f}" fill="{rnd.choice(cores)}" opacity=".75" filter="url(#{uid}bl)"/>')
    o.append(f'<ellipse cx="{vx}" cy="{vy + 140}" rx="90" ry="60" fill="{p["luz"]}" opacity=".18" filter="url(#{uid}bl2)"/>')
    # bancos dos dois lados, do fundo para a frente
    fileiras = [.08, .14, .21, .29, .38, .49, .62, .78, .97, 1.2]
    for lado in (-1, 1):
        for s in fileiras:
            y = vy + 10 + 330 * s
            ax = vx + lado * (16 + 60 * s)          # ponta do banco no corredor
            bx = vx + lado * (90 + 300 * s)         # ponta junto à parede
            h = 6 + 26 * s
            x1, x2 = min(ax, bx), max(ax, bx)
            o.append(f'<path d="M{x1:.1f} {y - h:.1f}H{x2:.1f}V{y:.1f}H{x1:.1f}Z" fill="{p["madeira"]}"/>'
                     f'<path d="M{x1:.1f} {y - h:.1f}H{x2:.1f}" stroke="{p["madeiraLuz"]}" stroke-width="{1 + 2 * s:.1f}"/>'
                     f'<path d="M{ax:.1f} {y - h * 1.25:.1f}V{y + 4 * s:.1f}" stroke="{p["madeiraLuz"]}" stroke-width="{2 + 5 * s:.1f}"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#{uid}vela)"/></svg>')
    return "".join(o)
