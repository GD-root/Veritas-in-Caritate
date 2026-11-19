"""Nave com bancos: grande vitral gótico ao fundo com o crucifixo na frente, raios de luz, arcadas laterais,
bancos de madeira dos dois lados e as cores do vitral refletidas no piso do corredor central."""
import math, random
from vitral import SIMB, CHUMBO, mosaico

W, H = 390, 844
V = (195, 318)  # ponto de fuga: base do altar
PAL = {
 "escuro": dict(fundo="#100c0b", pedra="#1c1714", pedra2="#2a221d", pedraLuz="#4a3c32", madeira="#2e1a10", madeiraLuz="#6a4226", piso="#120e0c", luz="#ffe2a8", cruz="#3a2414", cruzLuz="#7a5432", corpo="#efdcc0", corpoSombra="#c9a882", contorno="#1a0f08"),
 "claro": dict(fundo="#f6f1e7", pedra="#b8a58a", pedra2="#cdbb9e", pedraLuz="#e8dcc6", madeira="#6a4228", madeiraLuz="#a8724a", piso="#d8cbb4", luz="#fff6dc", cruz="#4a2e1a", cruzLuz="#7a5432", corpo="#efdcc0", corpoSombra="#c9a882", contorno="#2a1a0e"),
}
VIDRO = {"veritas": ["#2c5fd0", "#e08a1a", "#c0392b", "#f2c94c", "#2a9d6a", "#7a3cc0", "#4ab0e0"],
         "defesa": ["#c0392b", "#2c5fd0", "#f2c94c", "#a3192e", "#4ab0e0", "#e08a1a"],
         "reforma": ["#7a3cc0", "#2c5fd0", "#c43a7a", "#4ab0e0", "#f2c94c"],
         "valores": ["#2a9d6a", "#f2c94c", "#e08a1a", "#1d7a4c", "#4ab0e0"],
         "libertacao": ["#f2c94c", "#e08a1a", "#c0392b", "#a3192e", "#2c5fd0"],
         "maria": ["#2c5fd0", "#4ab0e0", "#9ab8ea", "#f3e6c4", "#1c3a9a", "#f2c94c"]}

def crucifixo(x, topo, pe, p, uid):
    """Crucifixo no estilo barroco: Cristo já morto, cabeça caída sobre o ombro e o cabelo cobrindo o rosto,
    corpo em curva com os joelhos dobrados de lado, braços em V presos com cordas e cravos, perizônio amarrado
    de lado, pés cruzados com um cravo, as chagas, madeira rústica e a placa nas três línguas."""
    k = p["contorno"]
    tb = topo + 32                          # altura da trave
    sangue = "#7a0f0f"
    g = [f'<defs><linearGradient id="{uid}mad" x1="0" x2="1"><stop offset="0" stop-color="{p["cruz"]}"/><stop offset=".5" stop-color="{p["cruzLuz"]}"/><stop offset="1" stop-color="{p["cruz"]}"/></linearGradient>'
         f'<linearGradient id="{uid}madH" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["cruzLuz"]}"/><stop offset="1" stop-color="{p["cruz"]}"/></linearGradient>'
         f'<linearGradient id="{uid}pele" x1="0" x2="1"><stop offset="0" stop-color="#8a5a36"/><stop offset=".35" stop-color="#d8ad7c"/><stop offset=".65" stop-color="#e2bc8c"/><stop offset="1" stop-color="#8a5a36"/></linearGradient>'
         f'<linearGradient id="{uid}braco" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2bc8c"/><stop offset="1" stop-color="#9a6a42"/></linearGradient>'
         f'<linearGradient id="{uid}pano" x1="0" x2="1"><stop offset="0" stop-color="#f6efe2"/><stop offset=".6" stop-color="#e2d6c2"/><stop offset="1" stop-color="#a8987e"/></linearGradient></defs>']
    # cruz de madeira rústica, com veios
    g.append(f'<rect x="{x - 6.5}" y="{topo}" width="13" height="{pe - topo}" fill="url(#{uid}mad)" stroke="{k}" stroke-width="1"/>'
             f'<rect x="{x - 54}" y="{tb - 6.5}" width="108" height="13" fill="url(#{uid}madH)" stroke="{k}" stroke-width="1"/>'
             f'<path d="M{x - 2} {topo + 3}V{pe - 3}M{x + 3} {topo + 20}V{pe - 30}M{x - 50} {tb - 2}H{x + 50}M{x - 30} {tb + 3}H{x + 40}" stroke="{k}" stroke-width=".6" opacity=".45"/>')
    # placa nas três línguas (hebraico, grego e latim)
    g.append(f'<path d="M{x - 24} {topo + 1}h48l-2 19h-44z" fill="#efe6d0" stroke="{k}" stroke-width=".9"/>'
             f'<text x="{x}" y="{topo + 6.6}" text-anchor="middle" font-family="serif" font-size="4.2" textLength="38" lengthAdjust="spacingAndGlyphs" fill="#3a2414">ישוע הנוצרי מלך היהודים</text>'
             f'<text x="{x}" y="{topo + 11.8}" text-anchor="middle" font-family="serif" font-size="3.6" textLength="40" lengthAdjust="spacingAndGlyphs" fill="#3a2414">ΙΗΣΟΥΣ Ο ΝΑΖΩΡΑΙΟΣ Ο ΒΑΣΙΛΕΥΣ</text>'
             f'<text x="{x}" y="{topo + 17}" text-anchor="middle" font-family="serif" font-size="3.8" font-weight="700" textLength="40" lengthAdjust="spacingAndGlyphs" fill="#3a2414">IESVS NAZARENVS REX IVDÆORVM</text>')
    # braços em V, presos com cordas e cravos
    for lado, (sx, sy) in ((-1, (x - 9, tb + 21)), (1, (x + 10, tb + 23))):
        mx, my = x + lado * 48, tb - 1
        g.append(f'<path d="M{mx} {my - 3}Q{x + lado * 30} {tb + 1} {sx + lado * 1} {sy - 4}Q{sx + lado * 4} {sy + 2} {sx} {sy + 6}Q{x + lado * 28} {tb + 13} {mx} {my + 3}Z" fill="url(#{uid}braco)" stroke="{k}" stroke-width=".9"/>'
                 f'<path d="M{x + lado * 30} {tb + 5}q{lado * -3} 2 {lado * -6} 2" fill="none" stroke="#8a5a36" stroke-width=".8"/>'
                 f'<path d="M{mx - lado * 1} {my - 3}q{lado * 5} -1 {lado * 7} 2q{lado * -1} 3 {lado * -6} 4z" fill="#c99868" stroke="{k}" stroke-width=".7"/>'
                 f'<path d="M{mx - lado * 8} {my - 4}l{lado * 2} 9M{mx - lado * 10.5} {my - 3.5}l{lado * 2} 9" stroke="#c9b48a" stroke-width="1.6"/>'
                 f'<circle cx="{mx + lado * 1}" cy="{my}" r="1.7" fill="#1a120c"/><path d="M{mx + lado * 1} {my + 1.5}q{lado * -1} 4 0 7" fill="none" stroke="{sangue}" stroke-width="1"/>')
    # tronco em curva: os ombros caídos e o quadril deslocado para a direita de quem olha
    g.append(f'<path d="M{x - 10} {tb + 18}Q{x + 1} {tb + 14} {x + 11} {tb + 20}Q{x + 15} {tb + 36} {x + 13} {tb + 56}L{x - 4} {tb + 57}Q{x - 9} {tb + 44} {x - 12} {tb + 32}Q{x - 13} {tb + 24} {x - 10} {tb + 18}Z" fill="url(#{uid}pele)" stroke="{k}" stroke-width="1"/>'
             f'<path d="M{x - 8} {tb + 26}q5 3.5 9 0q4 3 9 .5M{x - 8} {tb + 33}q3 1.6 6 .4M{x + 3} {tb + 33}q3 1.6 7 0M{x - 7.5} {tb + 38}q2.6 1.4 5 .2M{x + 3.5} {tb + 38}q2.8 1.4 6 0M{x + 2} {tb + 41}q.6 6 1 13M{x - 3} {tb + 45}q2 1 4 0M{x + 4} {tb + 45}q2 1 4 0M{x - 2.5} {tb + 50}q2 1 4 0M{x + 4.5} {tb + 50}q2 1 4 0" fill="none" stroke="#8a5a36" stroke-width=".8"/>'
             f'<path d="M{x + 11} {tb + 33}q2 2 1 5q-1 6 1 10" fill="none" stroke="{sangue}" stroke-width="1.3"/>')
    # pernas (desenhadas antes do perizônio, que cobre o alto das coxas): quadril inteiro, joelhos dobrados
    # para a direita de quem olha, pés cruzados com um cravo
    g.append(f'<path d="M{x - 9} {tb + 54}H{x + 14}Q{x + 17} {tb + 70} {x + 15} {tb + 84}L{x - 4} {tb + 82}Q{x - 10} {tb + 70} {x - 9} {tb + 54}Z" fill="url(#{uid}pele)" stroke="{k}" stroke-width=".9"/>'
             f'<path d="M{x - 8} {tb + 70}Q{x - 3} {tb + 82} {x + 8} {tb + 89}Q{x + 7} {tb + 104} {x + 3} {tb + 120}L{x - 2} {tb + 120}Q{x} {tb + 104} {x + 2} {tb + 93}Q{x - 9} {tb + 86} {x - 9} {tb + 72}Z" fill="url(#{uid}pele)" stroke="{k}" stroke-width=".9"/>'
             f'<path d="M{x + 2} {tb + 70}Q{x + 9} {tb + 78} {x + 15.5} {tb + 86}Q{x + 12} {tb + 104} {x + 6} {tb + 120}L{x + 1} {tb + 120}Q{x + 6} {tb + 104} {x + 8.5} {tb + 93}Q{x + 2} {tb + 86} {x} {tb + 76}Z" fill="url(#{uid}pele)" stroke="{k}" stroke-width=".9"/>'
             f'<path d="M{x + 9} {tb + 87}q3 1.5 5 -1M{x + 3.5} {tb + 90}q2 1 4 -.5M{x + 5} {tb + 98}q-1 8 -3 14M{x + 11} {tb + 98}q-2 8 -4 14" fill="none" stroke="#8a5a36" stroke-width=".8"/>'
             f'<path d="M{x + 12} {tb + 89}q-1 6 -3 12M{x + 6} {tb + 93}q-1 5 -2 9" fill="none" stroke="{sangue}" stroke-width="1"/>'
             f'<path d="M{x - 3} {tb + 118}l-2 9 7 1 3 -9zM{x + 2} {tb + 117}l1 11 6 -2 -2 -9z" fill="#c99868" stroke="{k}" stroke-width=".8"/>'
             f'<circle cx="{x + 2}" cy="{tb + 122}" r="1.8" fill="#1a120c"/><path d="M{x + 2} {tb + 124}q-1 4 0 8M{x - 1} {tb + 126}v4" fill="none" stroke="{sangue}" stroke-width="1"/>')
    # perizônio por cima: cobre do ventre até o meio das coxas, com dobras, a barra lisa e o nó de lado
    g.append(f'<path d="M{x - 10} {tb + 52}Q{x + 3} {tb + 47} {x + 16} {tb + 53}L{x + 18} {tb + 76}Q{x + 11} {tb + 81} {x + 4} {tb + 78}Q{x - 3} {tb + 82} {x - 10} {tb + 75}Q{x - 12} {tb + 63} {x - 10} {tb + 52}Z" fill="url(#{uid}pano)" stroke="{k}" stroke-width=".9"/>'
             f'<path d="M{x - 7} {tb + 55}Q{x - 2} {tb + 64} {x - 4} {tb + 77}M{x - 1} {tb + 54}Q{x + 4} {tb + 64} {x + 3} {tb + 77}M{x + 5} {tb + 53}Q{x + 10} {tb + 63} {x + 10} {tb + 78}M{x - 9} {tb + 58}Q{x + 2} {tb + 55} {x + 15} {tb + 58}" fill="none" stroke="#a8987e" stroke-width=".8"/>'
             f'<path d="M{x + 14} {tb + 52}q5 -1 6 4q-2 3 -6 2z" fill="#e2d6c2" stroke="{k}" stroke-width=".8"/>'
             f'<path d="M{x + 18} {tb + 57}q4 6 2 14q2 6 5 9q-5 0 -7 -5q-2 3 -4 2q2 -6 1 -12z" fill="url(#{uid}pano)" stroke="{k}" stroke-width=".8"/>')
    # cabeça caída sobre o ombro, o cabelo escuro cobrindo o rosto, coroa de espinhos
    hx, hy = x - 9, tb + 22
    g.append(f'<path d="M{hx + 4} {hy - 9}Q{hx + 10} {hy - 4} {hx + 7} {hy + 4}Q{hx + 4} {hy + 9} {hx - 1} {hy + 10}Q{hx - 6} {hy + 8} {hx - 7} {hy + 2}Q{hx - 6} {hy - 7} {hx + 4} {hy - 9}Z" fill="#c99868" stroke="{k}" stroke-width=".9"/>'
             f'<path d="M{hx + 5} {hy - 11}Q{hx - 6} {hy - 12} {hx - 9} {hy - 2}Q{hx - 11} {hy + 10} {hx - 7} {hy + 22}Q{hx - 4} {hy + 14} {hx - 3} {hy + 8}Q{hx - 1} {hy + 16} {hx + 1} {hy + 20}Q{hx + 2} {hy + 10} {hx + 3} {hy + 4}Q{hx + 6} {hy + 8} {hx + 7} {hy + 14}Q{hx + 9} {hy + 4} {hx + 8} {hy - 4}Q{hx + 9} {hy - 9} {hx + 5} {hy - 11}Z" fill="#2a1a10" stroke="{k}" stroke-width=".7"/>'
             f'<path d="M{hx - 6} {hy - 3}q3 6 2 14M{hx} {hy - 4}q1 8 0 16M{hx + 5} {hy - 5}q2 6 1 12" fill="none" stroke="#4a3020" stroke-width=".7"/>'
             f'<path d="M{hx - 7} {hy - 7}Q{hx} {hy - 14} {hx + 8} {hy - 8}" fill="none" stroke="#3a2a14" stroke-width="2.6"/>'
             + "".join(f'<path d="M{hx - 6 + j * 2.6:.1f} {hy - 8.5 - (3 if 1 < j < 5 else 1.5):.1f}l{(-1) ** j * 1.8:.1f} -2.6" stroke="#3a2a14" stroke-width=".9"/>' for j in range(6))
             + f'<path d="M{hx + 6} {hy - 6}q1 4 -1 8M{hx + 2} {hy + 9}q1 3 0 6" fill="none" stroke="{sangue}" stroke-width="1"/>')
    return "".join(g)

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
    # grande crucifixo diante do vitral: Cristo crucificado (ver crucifixo())
    o.append(crucifixo(vx, 112, vy - 18, p, uid))
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
