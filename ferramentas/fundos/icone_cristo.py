"""Ícone do Cristo Ressuscitado e Rei (estandarte atrás do altar da igreja moderna), desenhado numa caixa
200 × 430 e depois reduzido para o tamanho da cena.

Cristo de pé, de frente: coroa e auréola com a cruz vermelha, cabelo longo e barba, gola bordada a ouro,
túnica branca com faixa na cintura e a estola branca caindo do ombro, manto vermelho-alaranjado manchado
com flores douradas e forro mais claro, a mão direita erguida segurando a cruz-estandarte e a esquerda
no peito, pés descalços dando um passo. Fundo de nuvens cor de pêssego, ramos de folhinhas vermelhas e
verdes, dois anjos com rolos no alto, dois anjinhos de asas douradas com IC e XC e o chão ocre."""
import random

BW, BH = 200, 430
PELE, PELE2, PELE3 = "#e6b98e", "#c98e62", "#9a6440"
CONT = "#4a1e0e"
OURO, OURO2 = "#e8bd4a", "#a8741e"


def _folhas(rnd, n, xs, ys, cores, r=(2.2, 4.2)):
    out = []
    for _ in range(n):
        x, y = rnd.uniform(*xs), rnd.uniform(*ys)
        rx = rnd.uniform(*r)
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{rx * rnd.uniform(.65, .9):.1f}" transform="rotate({rnd.randint(0, 180)} {x:.1f} {y:.1f})" fill="{rnd.choice(cores)}" opacity="{rnd.uniform(.75, 1):.2f}"/>')
    return "".join(out)


def _anjo_rolo(x, y, lado, uid):
    """Anjo branco deitado no ar, segurando um rolo, no alto do ícone."""
    s = lado
    return (f'<g transform="translate({x} {y}) scale({s} 1)">'
            f'<path d="M-18 4Q-6 -10 14 -6Q22 -4 26 2Q14 4 6 10Q-6 14 -18 4Z" fill="#f4efe6" stroke="#b9a68a" stroke-width=".7"/>'
            f'<path d="M-4 -4Q-14 -20 -30 -18Q-22 -10 -10 0Z" fill="#ece4d6" stroke="#b9a68a" stroke-width=".6"/>'
            f'<path d="M-2 -2Q4 -16 -4 -24Q8 -18 6 -4Z" fill="#e4dacb" stroke="#b9a68a" stroke-width=".6"/>'
            f'<circle cx="22" cy="-2" r="4" fill="{PELE}" stroke="#b07a52" stroke-width=".5"/><path d="M19 -5q3 -3 6 0" stroke="#7a4a24" stroke-width="1.6" fill="none"/>'
            f'<path d="M26 4l10 -2v8l-10 2z" fill="#f8f2e4" stroke="#b9a68a" stroke-width=".6"/><path d="M36 2q3 4 0 8" stroke="#b9a68a" stroke-width=".6" fill="none"/></g>')


def _anjinho(x, y, letras, lado):
    """Anjinho de asas douradas segurando o medalhão com IC ou XC."""
    s = lado
    return (f'<g transform="translate({x} {y})">'
            f'<path d="M{-4 * s} -2Q{-20 * s} -14 {-26 * s} -2Q{-18 * s} 0 {-14 * s} 6Q{-20 * s} 8 {-22 * s} 14Q{-10 * s} 12 {-2 * s} 4Z" fill="{OURO}" stroke="{OURO2}" stroke-width=".6"/>'
            f'<path d="M{-10 * s} -4l{-8 * s} 2M{-12 * s} 2l{-8 * s} 4" stroke="{OURO2}" stroke-width=".5"/>'
            f'<circle cx="{2 * s}" cy="-6" r="3.4" fill="{PELE}"/><path d="M{-1 * s} -2q{3 * s} 8 {8 * s} 10" stroke="#f0e6d6" stroke-width="5" stroke-linecap="round" fill="none"/>'
            f'<circle cx="0" cy="8" r="6.5" fill="#f6ead2" stroke="{OURO2}" stroke-width=".7"/>'
            f'<text x="0" y="10.6" text-anchor="middle" font-family="serif" font-size="7" font-weight="700" fill="#a3192e">{letras}</text></g>')


def _desenho(uid):
    rnd = random.Random(42)
    cx = 100
    g = [f'<defs>'
         f'<linearGradient id="{uid}fd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf0dc"/><stop offset=".45" stop-color="#f7dcb4"/><stop offset=".8" stop-color="#f0bf84"/><stop offset="1" stop-color="#d98a42"/></linearGradient>'
         f'<radialGradient id="{uid}nv"><stop offset="0" stop-color="#fffaf0" stop-opacity=".9"/><stop offset="1" stop-color="#fffaf0" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="{uid}nl"><stop offset="0" stop-color="#ef9a52" stop-opacity=".55"/><stop offset="1" stop-color="#ef9a52" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="{uid}mt" x1="0" x2="1"><stop offset="0" stop-color="#a8200e"/><stop offset=".25" stop-color="#e2461a"/><stop offset=".5" stop-color="#f26a24"/><stop offset=".75" stop-color="#e04416"/><stop offset="1" stop-color="#9a1c0c"/></linearGradient>'
         f'<linearGradient id="{uid}fo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8a24a"/><stop offset="1" stop-color="#e8762a"/></linearGradient>'
         f'<linearGradient id="{uid}tn" x1="0" x2="1"><stop offset="0" stop-color="#e6dccd"/><stop offset=".45" stop-color="#fffbf4"/><stop offset=".7" stop-color="#f6efe4"/><stop offset="1" stop-color="#d8cbb8"/></linearGradient>'
         f'<linearGradient id="{uid}rs" x1="0" x2="1"><stop offset="0" stop-color="{PELE2}"/><stop offset=".35" stop-color="{PELE}"/><stop offset=".7" stop-color="#ecc49c"/><stop offset="1" stop-color="{PELE2}"/></linearGradient>'
         f'<radialGradient id="{uid}au" cx="50%" cy="45%"><stop offset=".55" stop-color="#fff6dc"/><stop offset=".9" stop-color="#f6dfa2"/><stop offset="1" stop-color="#d9a640"/></radialGradient>'
         f'<filter id="{uid}bf" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'
         f'<clipPath id="{uid}bx"><rect width="{BW}" height="{BH}"/></clipPath></defs>'
         f'<g clip-path="url(#{uid}bx)"><rect width="{BW}" height="{BH}" fill="url(#{uid}fd)"/>']
    # nuvens e manchas de luz do fundo
    for _ in range(14):
        x, y, r = rnd.uniform(0, BW), rnd.uniform(0, 300), rnd.uniform(14, 34)
        g.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * .6:.0f}" fill="url(#{uid}nv)"/>')
    for _ in range(10):
        x, y, r = rnd.choice((rnd.uniform(0, 50), rnd.uniform(150, 200))), rnd.uniform(40, 360), rnd.uniform(12, 26)
        g.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * .7:.0f}" fill="url(#{uid}nl)"/>')
    g.append(f'<path d="M100 40q-6 20 4 40q8 20 -2 40" fill="none" stroke="#fffaf0" stroke-width="6" opacity=".6" filter="url(#{uid}bf)"/>')
    # ramos de folhinhas vermelhas descendo dos dois lados e folhas verdes no meio e embaixo
    verm = ["#e0602a", "#f08a3a", "#c8401c", "#e8a040", "#d4502a"]
    verde = ["#5a6a3a", "#3e4a2a", "#7a8a4a", "#8a5a3a", "#2e3a2a"]
    for lado in (-1, 1):
        for j in range(26):
            t = j / 26
            x = cx + lado * (34 + 14 * (t * 3 % 1) + rnd.uniform(-6, 6))
            y = 10 + t * 190
            g.append(_folhas(rnd, 2, (x - 3, x + 3), (y - 3, y + 3), verm, (2.4, 4.4)))
        g.append(_folhas(rnd, 26, (cx + lado * 30, cx + lado * 98) if lado > 0 else (cx - 98, cx - 30), (190, 232), verde + verm[:2], (2.6, 4.6)))
        g.append(_folhas(rnd, 22, (cx + lado * 64, cx + lado * 100) if lado > 0 else (cx - 100, cx - 64), (250, 300), verde + verm, (2.6, 4.4)))
        g.append(_folhas(rnd, 22, (cx + lado * 50, cx + lado * 100) if lado > 0 else (cx - 100, cx - 50), (330, 380), verde + verm, (2.8, 4.8)))
    # anjos com os rolos no alto
    g.append(_anjo_rolo(46, 66, 1, uid) + _anjo_rolo(154, 66, -1, uid))
    # chão ocre
    g.append(f'<path d="M0 372Q100 360 200 372V430H0Z" fill="#c07a36"/><path d="M0 384Q100 374 200 384" fill="none" stroke="#a8622a" stroke-width="1.2"/>'
             + _folhas(rnd, 30, (4, 196), (378, 426), ["#8a4a1e", "#6a3a18", "#d08a3a", "#5a6a3a"], (2.4, 4)))
    # cruz-estandarte (a haste passa por trás da mão)
    sx = 58
    g.append(f'<path d="M{sx} 24V404" stroke="#8a5a1a" stroke-width="3.6"/><path d="M{sx} 24V404" stroke="{OURO}" stroke-width="1.6"/>'
             f'<path d="M{sx - 22} 50H{sx + 22}M{sx} 16V30" stroke="#8a5a1a" stroke-width="4"/><path d="M{sx - 22} 50H{sx + 22}" stroke="{OURO}" stroke-width="1.8"/>'
             f'<path d="M{sx - 25} 46l3 4 -3 4M{sx + 25} 46l-3 4 3 4M{sx - 4} 13l4 -4 4 4" fill="none" stroke="#8a5a1a" stroke-width="1.6"/>')
    # manto: as costas, abrindo-se dos ombros até a barra que ondula; o forro claro aparece nas bordas
    g.append(f'<path d="M78 146Q60 150 52 176Q40 230 30 290Q22 330 26 352Q40 360 56 352Q66 360 76 350L82 190L122 190L130 354Q142 364 156 358Q170 366 182 356Q182 320 172 280Q162 220 152 178Q144 150 124 146Z" fill="url(#{uid}mt)" stroke="{CONT}" stroke-width=".9"/>'
             f'<path d="M26 352Q40 360 56 352Q66 360 76 350L74 340Q62 350 52 342Q40 350 30 342Z" fill="url(#{uid}fo)"/>'
             f'<path d="M130 354Q142 364 156 358Q170 366 182 356L180 344Q168 354 156 346Q142 352 132 342Z" fill="url(#{uid}fo)"/>')
    # aba da frente do manto à esquerda de quem olha, caindo do ombro e dobrando sobre o braço
    g.append(f'<path d="M80 150Q70 160 66 190Q60 250 54 300Q50 330 62 346Q72 340 80 344Q84 300 84 250Q86 200 90 160Z" fill="url(#{uid}mt)" stroke="{CONT}" stroke-width=".8"/>'
             f'<path d="M66 196Q62 250 58 300M74 180Q72 240 70 330M82 190Q80 250 78 336" fill="none" stroke="#8a1a0a" stroke-width="1" opacity=".55"/>'
             f'<path d="M58 300q-4 6 -2 14M54 260q-3 4 -1 10" fill="none" stroke="#fbd39a" stroke-width=".9" opacity=".8"/>')
    # textura manchada e florzinhas douradas no manto
    for _ in range(70):
        lado = rnd.choice((-1, 1))
        x = cx + lado * rnd.uniform(26, 76)
        y = rnd.uniform(170, 350)
        if lado < 0 and x < 30 + (y - 170) * -.05:
            continue
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1, 2.6):.1f}" fill="{rnd.choice(["#b8240e", "#f5823a", "#c8300f"])}" opacity=".7"/>')
    for _ in range(26):
        lado = rnd.choice((-1, 1))
        x, y = cx + lado * rnd.uniform(30, 70), rnd.uniform(190, 340)
        g.append(f'<path d="M{x:.1f} {y - 1.6:.1f}l1 1.6 -1 1.6 -1 -1.6zM{x - 1.6:.1f} {y:.1f}h3.2" stroke="#fbd890" stroke-width=".6" fill="#fbd890" opacity=".85"/>')
    g.append(f'<path d="M44 250q-8 -10 2 -16q8 -2 6 6q-2 4 -6 2" fill="none" stroke="#fff3dc" stroke-width=".9" opacity=".8"/>'
             f'<path d="M40 268q-6 8 0 14" fill="none" stroke="#fff3dc" stroke-width=".8" opacity=".7"/>'
             f'<path d="M150 210Q160 260 170 330M140 200Q146 260 150 344M160 250q4 30 12 70" fill="none" stroke="#8a1a0a" stroke-width="1" opacity=".55"/>')
    # túnica branca: do pescoço aos pés, com pregas, a faixa da cintura e a barra
    g.append(f'<path d="M86 146Q100 150 116 146L124 190Q130 260 130 330Q134 360 128 380Q112 386 100 382Q86 386 74 380Q70 350 74 320Q76 250 82 190Z" fill="url(#{uid}tn)" stroke="{CONT}" stroke-width=".8"/>'
             f'<path d="M90 236Q88 300 84 376M100 240Q100 310 98 380M112 236Q114 300 116 378M84 300Q80 340 80 378" fill="none" stroke="#cbbca6" stroke-width="1"/>'
             f'<path d="M80 212Q100 220 124 212L125 226Q100 234 79 226Z" fill="#f8f2e8" stroke="#b9a88e" stroke-width=".8"/>'
             f'<path d="M82 218Q100 225 123 218M86 230q-2 8 -6 14M114 230q2 8 6 12" fill="none" stroke="#c9b9a2" stroke-width=".8"/>')
    # estola branca caindo do ombro esquerdo de Cristo (à direita de quem olha) até os joelhos
    g.append(f'<path d="M118 150L128 152L140 330L130 334Z" fill="#fffaf2" stroke="#b9a88e" stroke-width=".8"/>'
             f'<path d="M126 166v8M122.5 170h7" stroke="{OURO}" stroke-width="1.4"/><path d="M132 320l6 -1" stroke="{OURO}" stroke-width="1.2"/>')
    # braço direito erguido com a manga branca e o punho dourado, a mão fechada na haste
    g.append(f'<path d="M84 150Q70 150 64 138L54 112L66 108L74 128Q80 138 92 144Z" fill="url(#{uid}tn)" stroke="{CONT}" stroke-width=".8"/>'
             f'<path d="M70 136q-4 -10 -8 -18M78 140q-6 -6 -10 -16" fill="none" stroke="#cbbca6" stroke-width=".8"/>'
             f'<path d="M53 112L66 107L64 101L52 106Z" fill="{OURO}" stroke="{OURO2}" stroke-width=".6"/>'
             f'<path d="M52 104Q50 96 54 90Q60 86 64 90Q66 96 64 102Z" fill="url(#{uid}rs)" stroke="{CONT}" stroke-width=".7"/>'
             f'<path d="M54 92h8M53.5 95.5h9M53.5 99h9" stroke="{PELE3}" stroke-width=".6"/><path d="M52 94q-3 2 -1 6" fill="none" stroke="{CONT}" stroke-width=".6"/>')
    # gola larga bordada a ouro
    g.append(f'<path d="M80 144Q100 132 120 144Q122 154 116 158Q100 164 84 158Q78 154 80 144Z" fill="{OURO}" stroke="{OURO2}" stroke-width=".8"/>'
             + "".join(f'<circle cx="{100 + 17 * c:.1f}" cy="{150 + 5 * (1 - c * c) ** .5:.1f}" r="1.2" fill="#a3192e"/>' for c in (-.9, -.6, -.3, 0, .3, .6, .9))
             + f'<path d="M84 150Q100 158 116 150" fill="none" stroke="#fff1c4" stroke-width=".8"/>')
    # mão esquerda no peito, com a manga e o punho dourado
    g.append(f'<path d="M124 152Q134 164 132 178L120 184Q114 176 116 168Z" fill="url(#{uid}tn)" stroke="{CONT}" stroke-width=".7"/>'
             f'<path d="M121 184L132 178L131 172L119 178Z" fill="{OURO}" stroke="{OURO2}" stroke-width=".5"/>'
             f'<path d="M120 178Q112 180 104 176Q98 172 100 168Q106 168 112 170Q116 168 120 172Z" fill="url(#{uid}rs)" stroke="{CONT}" stroke-width=".6"/>'
             f'<path d="M102 169q4 2 8 2M101 172q5 2 10 2M103 175q4 1.5 8 1.5" fill="none" stroke="{PELE3}" stroke-width=".55"/>')
    # pés descalços: o direito à frente, mais baixo; o esquerdo atrás
    g.append(f'<path d="M86 380Q84 392 82 402Q86 408 96 408Q100 404 98 396Q96 388 96 382Z" fill="url(#{uid}rs)" stroke="{CONT}" stroke-width=".7"/>'
             f'<path d="M84 404q2 3 4 3M88 405q1 2.5 3 2.5M92 405q1 2.5 3 2.5" fill="none" stroke="{PELE3}" stroke-width=".55"/>'
             f'<path d="M110 376Q112 386 116 392Q122 394 126 390Q124 382 120 376Z" fill="url(#{uid}rs)" stroke="{CONT}" stroke-width=".7"/>'
             f'<path d="M117 390q2 1.5 4 1M121 389q1.5 1.2 3 .6" fill="none" stroke="{PELE3}" stroke-width=".5"/>')
    # auréola com a cruz vermelha
    hx, hy = cx, 114
    g.append(f'<circle cx="{hx}" cy="{hy - 4}" r="30" fill="url(#{uid}au)" stroke="#c9922c" stroke-width="1.2"/>'
             f'<circle cx="{hx}" cy="{hy - 4}" r="27.5" fill="none" stroke="#e8c27a" stroke-width=".6"/>'
             f'<path d="M{hx} {hy - 34}V{hy - 24}M{hx - 30} {hy - 4}H{hx - 18}M{hx + 30} {hy - 4}H{hx + 18}" stroke="#c0281a" stroke-width="3"/>')
    # cabelo longo (por trás do rosto), caindo sobre os ombros
    g.append(f'<path d="M{hx - 14} {hy - 16}Q{hx} {hy - 26} {hx + 14} {hy - 16}Q{hx + 19} {hy - 2} {hx + 17} {hy + 14}Q{hx + 20} {hy + 26} {hx + 14} {hy + 34}Q{hx + 10} {hy + 24} {hx + 10} {hy + 12}L{hx - 10} {hy + 12}Q{hx - 10} {hy + 24} {hx - 14} {hy + 34}Q{hx - 20} {hy + 26} {hx - 17} {hy + 14}Q{hx - 19} {hy - 2} {hx - 14} {hy - 16}Z" fill="#4a2814" stroke="#2a160a" stroke-width=".7"/>'
             f'<path d="M{hx - 15} {hy}q-2 14 0 30M{hx + 15} {hy}q2 14 0 30M{hx - 12} {hy + 4}q-1 12 -1 24M{hx + 12} {hy + 4}q1 12 1 24" fill="none" stroke="#6a3e20" stroke-width=".8"/>')
    # pescoço e rosto, no estilo dos ícones: olhos amendoados, sobrancelhas arqueadas, nariz longo e fino
    g.append(f'<path d="M{hx - 5} {hy + 14}h10v12h-10z" fill="{PELE2}"/>'
             f'<path d="M{hx - 11} {hy - 8}Q{hx - 12} {hy + 8} {hx - 7} {hy + 16}Q{hx} {hy + 22} {hx + 7} {hy + 16}Q{hx + 12} {hy + 8} {hx + 11} {hy - 8}Q{hx} {hy - 16} {hx - 11} {hy - 8}Z" fill="url(#{uid}rs)" stroke="{CONT}" stroke-width=".7"/>'
             f'<path d="M{hx - 9} {hy - 3}Q{hx - 5.5} {hy - 6} {hx - 2} {hy - 3.4}M{hx + 2} {hy - 3.4}Q{hx + 5.5} {hy - 6} {hx + 9} {hy - 3}" fill="none" stroke="#3a1e0e" stroke-width="1"/>'
             f'<path d="M{hx - 8.4} {hy + .4}Q{hx - 5.4} {hy - 2} {hx - 2.4} {hy + .4}Q{hx - 5.4} {hy + 2} {hx - 8.4} {hy + .4}ZM{hx + 2.4} {hy + .4}Q{hx + 5.4} {hy - 2} {hx + 8.4} {hy + .4}Q{hx + 5.4} {hy + 2} {hx + 2.4} {hy + .4}Z" fill="#fbf4e8" stroke="#3a1e0e" stroke-width=".6"/>'
             f'<circle cx="{hx - 5.2}" cy="{hy + .3}" r="1.2" fill="#2a160a"/><circle cx="{hx + 5.2}" cy="{hy + .3}" r="1.2" fill="#2a160a"/>'
             f'<path d="M{hx - 1.4} {hy - 2}Q{hx - 1.6} {hy + 5} {hx - 2.4} {hy + 7.4}Q{hx} {hy + 8.6} {hx + 2.2} {hy + 7.4}" fill="none" stroke="{PELE3}" stroke-width=".8"/>'
             f'<path d="M{hx - 7} {hy + 4}q1 3 3 4M{hx + 7} {hy + 4}q-1 3 -3 4" fill="none" stroke="#c98a5e" stroke-width=".6" opacity=".7"/>')
    # bigode e barba bipartida
    g.append(f'<path d="M{hx - 8} {hy + 9}Q{hx - 4} {hy + 8} {hx} {hy + 9.6}Q{hx + 4} {hy + 8} {hx + 8} {hy + 9}Q{hx + 9} {hy + 16} {hx + 5} {hy + 22}Q{hx + 2} {hy + 20} {hx} {hy + 23}Q{hx - 2} {hy + 20} {hx - 5} {hy + 22}Q{hx - 9} {hy + 16} {hx - 8} {hy + 9}Z" fill="#5a3218" stroke="#2a160a" stroke-width=".5"/>'
             f'<path d="M{hx - 3} {hy + 12.4}Q{hx} {hy + 13.6} {hx + 3} {hy + 12.4}" fill="none" stroke="#8a3a2a" stroke-width="1.1"/>'
             f'<path d="M{hx - 4} {hy + 16}q1 3 0 5M{hx + 4} {hy + 16}q-1 3 0 5" fill="none" stroke="#7a4a28" stroke-width=".6"/>')
    # coroa de ouro com pedras e o cabelo repartido ao meio por baixo
    g.append(f'<path d="M{hx - 11} {hy - 8}Q{hx} {hy - 13} {hx + 11} {hy - 8}" fill="none" stroke="#4a2814" stroke-width="3"/>'
             f'<path d="M{hx - 13} {hy - 9}L{hx - 14} {hy - 20}L{hx - 9} {hy - 15}L{hx - 5} {hy - 23}L{hx} {hy - 16}L{hx + 5} {hy - 23}L{hx + 9} {hy - 15}L{hx + 14} {hy - 20}L{hx + 13} {hy - 9}Q{hx} {hy - 14} {hx - 13} {hy - 9}Z" fill="{OURO}" stroke="{OURO2}" stroke-width=".8"/>'
             f'<path d="M{hx - 13} {hy - 11.5}Q{hx} {hy - 16.5} {hx + 13} {hy - 11.5}" fill="none" stroke="{OURO2}" stroke-width=".7"/>'
             f'<circle cx="{hx}" cy="{hy - 13}" r="1.6" fill="#a3192e"/><circle cx="{hx - 7}" cy="{hy - 12.4}" r="1.3" fill="#1f6fd0"/><circle cx="{hx + 7}" cy="{hy - 12.4}" r="1.3" fill="#1f6fd0"/>'
             f'<circle cx="{hx - 14}" cy="{hy - 20}" r="1.3" fill="#fff4cc"/><circle cx="{hx - 5}" cy="{hy - 23}" r="1.3" fill="#fff4cc"/><circle cx="{hx + 5}" cy="{hy - 23}" r="1.3" fill="#fff4cc"/><circle cx="{hx + 14}" cy="{hy - 20}" r="1.3" fill="#fff4cc"/>')
    # anjinhos com IC e XC ao lado da auréola, e dois anjinhos menores embaixo nas laterais
    g.append(_anjinho(34, 150, "IC", -1) + _anjinho(166, 150, "XC", 1))
    for x, lado in ((22, -1), (178, 1)):
        g.append(f'<g transform="translate({x} 300)"><path d="M0 0q{8 * lado} -10 {14 * lado} -4q{-4 * lado} 4 {-6 * lado} 10z" fill="{OURO}" opacity=".85"/><circle cx="0" cy="-3" r="3" fill="{PELE}"/><path d="M0 0v10" stroke="#f0e6d6" stroke-width="5" stroke-linecap="round"/></g>')
    g.append(f'</g><rect width="{BW}" height="{BH}" fill="none" stroke="#a8742e" stroke-width="1.4"/>')
    return "".join(g)


def icone(x0, y0, w, uid):
    """O ícone na cena, com largura w (a altura segue a proporção 200 × 430)."""
    s = w / BW
    return f'<g transform="translate({x0} {y0}) scale({s:.4f})">{_desenho(uid)}</g>'


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(f'<svg viewBox="0 0 {BW} {BH}" xmlns="http://www.w3.org/2000/svg" width="{BW * 3}" height="{BH * 3}">{_desenho("z")}</svg>')
