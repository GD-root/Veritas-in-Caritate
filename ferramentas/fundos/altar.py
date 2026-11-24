"""Vista do altar, para a área "Conhecer a Igreja": depois de atravessar a nave, a pessoa chega ao presbitério.
Retábulo dourado com o crucifixo ao centro e a rosácea no alto (onde o app põe o medalhão), o sacrário,
os seis castiçais, o altar com a toalha e o frontal, a lâmpada do Santíssimo, os degraus e a mesa de comunhão."""
import random
from vitral import CHUMBO, mosaico
from igreja import PAL, crucifixo

W, H = 390, 844
OURO = {"escuro": ("#8a6418", "#e6c66f", "#c9a243"), "claro": ("#9a7420", "#f2d98a", "#c9a243")}


def cena_altar(p_nome="escuro", altura_visivel=.6, uid="al"):
    p = PAL[p_nome]
    o1, o2, o3 = OURO[p_nome]
    rnd = random.Random(19)
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMin slice"><defs>',
         f'<linearGradient id="{uid}ouro" x1="0" x2="1"><stop offset="0" stop-color="{o1}"/><stop offset=".5" stop-color="{o2}"/><stop offset="1" stop-color="{o1}"/></linearGradient>',
         f'<linearGradient id="{uid}ouroV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{o2}"/><stop offset="1" stop-color="{o1}"/></linearGradient>',
         f'<radialGradient id="{uid}nicho" cx="50%" cy="30%" r="70%"><stop offset="0" stop-color="#4a1418"/><stop offset="1" stop-color="#1e080a"/></radialGradient>',
         f'<radialGradient id="{uid}chama"><stop offset="0" stop-color="#fff6d0"/><stop offset=".4" stop-color="#ffc54a" stop-opacity=".9"/><stop offset="1" stop-color="#ff9a1f" stop-opacity="0"/></radialGradient>',
         f'<linearGradient id="{uid}raio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["luz"]}" stop-opacity=".4"/><stop offset="1" stop-color="{p["luz"]}" stop-opacity="0"/></linearGradient>',
         f'<linearGradient id="{uid}vela" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["fundo"]}" stop-opacity="0"/><stop offset="{altura_visivel - .2}" stop-color="{p["fundo"]}" stop-opacity="0"/><stop offset="{altura_visivel}" stop-color="{p["fundo"]}" stop-opacity=".9"/><stop offset="{altura_visivel + .08}" stop-color="{p["fundo"]}" stop-opacity="1"/></linearGradient>',
         f'<filter id="{uid}bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>',
         '</defs>']
    # parede da abside, em pedra, com a abóbada em arco
    o.append(f'<rect width="{W}" height="{H}" fill="{p["pedra"]}"/>')
    for k in range(9):
        o.append(f'<path d="M{k * 48 - 10} 0V330" stroke="{p["pedra2"]}" stroke-width="2" opacity=".6"/>')
    o.append(f'<path d="M0 60Q195 -40 390 60" fill="none" stroke="{p["pedraLuz"]}" stroke-width="6" opacity=".5"/>')
    # retábulo dourado: colunas, entablamento e o nicho vermelho do crucifixo
    o.append(f'<path d="M58 330V120Q58 40 195 26Q332 40 332 120V330Z" fill="url(#{uid}ouroV)" stroke="{o1}" stroke-width="2"/>')
    o.append(f'<path d="M96 330V128Q96 70 195 60Q294 70 294 128V330Z" fill="url(#{uid}nicho)" stroke="{o1}" stroke-width="3"/>')
    for x in (70, 84, 306, 320):
        o.append(f'<rect x="{x - 4}" y="110" width="8" height="220" fill="url(#{uid}ouro)" stroke="{o1}" stroke-width=".8"/>'
                 f'<rect x="{x - 6}" y="104" width="12" height="8" fill="{o2}"/><rect x="{x - 6}" y="326" width="12" height="6" fill="{o2}"/>')
    for k in range(10):  # entalhes na moldura
        o.append(f'<circle cx="{110 + k * 19.5:.0f}" cy="{48 + abs(4.5 - k) * 4:.0f}" r="3" fill="{o2}" stroke="{o1}" stroke-width=".6"/>')
    # rosácea no alto: o app põe por cima o medalhão (centro 195, 100; 44 de diâmetro)
    o.append(f'<circle cx="195" cy="100" r="30" fill="{o1}"/><defs><clipPath id="{uid}ros"><circle cx="195" cy="100" r="26"/></clipPath></defs>'
             f'<g clip-path="url(#{uid}ros)"><g transform="translate(169 74)" stroke="{CHUMBO}" stroke-width="1">{mosaico(52, 52, ["#2c5fd0", "#c0392b", "#f2c94c", "#2a9d6a"], 7, passo=10, jit=2)}</g></g>'
             f'<circle cx="195" cy="100" r="22" fill="#f6ecd2" stroke="{CHUMBO}" stroke-width="2.4"/>')
    # crucifixo dentro do nicho
    o.append(f'<g transform="translate(195 134) scale(.56) translate(-195 -136)">{crucifixo(195, 136, 292, p, uid)}</g>')
    # raios de luz descendo sobre o altar
    for a, b in ((150, 120), (210, 260), (180, 190)):
        o.append(f'<polygon points="{a},40 {a + 26},40 {b + 60},360 {b - 20},360" fill="url(#{uid}raio)" opacity=".55"/>')
    # lâmpada do Santíssimo, pendurada à esquerda
    o.append(f'<path d="M36 0V150" stroke="{o1}" stroke-width="1.6"/><path d="M26 150h20l-4 18h-12z" fill="url(#{uid}ouro)"/><ellipse cx="36" cy="160" rx="6" ry="7" fill="#c0281e" opacity=".9"/><circle cx="36" cy="158" r="9" fill="url(#{uid}chama)"/>')
    # piso de mármore e os degraus do presbitério
    o.append(f'<rect y="360" width="{W}" height="{H - 360}" fill="{p["piso"]}"/><g transform="translate(0 30)">')
    for k, (y, w) in enumerate(((330, 300), (344, 330), (358, 360))):
        o.append(f'<path d="M{195 - w / 2} {y}H{195 + w / 2}V{y + 14}H{195 - w / 2}Z" fill="{p["pedraLuz"]}" stroke="{p["pedra2"]}" stroke-width="1"/>')
    # altar: mesa com a toalha branca e o frontal com a cruz
    o.append(f'<rect x="96" y="270" width="198" height="60" fill="{p["madeira"]}" stroke="{o1}" stroke-width="2"/>'
             f'<rect x="112" y="282" width="166" height="44" fill="#7a1018" stroke="{o2}" stroke-width="2"/>'
             f'<path d="M195 288v32M181 300h28" stroke="{o2}" stroke-width="4"/>'
             f'<path d="M90 262H300V272H90Z" fill="#f8f4ea"/><path d="M90 272H300L296 286H94Z" fill="#efe8d8"/>'
             + "".join(f'<path d="M{x} 272l2 10" stroke="#d8cfbc" stroke-width="1"/>' for x in range(98, 300, 10)))
    # sacrário no centro e os seis castiçais
    o.append(f'<path d="M172 262V222Q172 206 195 202Q218 206 218 222V262Z" fill="url(#{uid}ouro)" stroke="{o1}" stroke-width="1.6"/>'
             f'<path d="M181 262V230h28v32" fill="#f6ecd2" stroke="{o1}" stroke-width="1.2"/><path d="M195 236v18M188 243h14" stroke="{o1}" stroke-width="2.4"/>'
             f'<path d="M195 202v-10M190 196h10" stroke="{o2}" stroke-width="2.4"/>')
    for k, dx in enumerate((-86, -62, -38, 38, 62, 86)):
        h = 46 - abs(k - 2.5) * 0 - (3 - min(k, 5 - k)) * 6
        x = 195 + dx
        o.append(f'<path d="M{x - 6} 262h12l-3 -6h-6z" fill="url(#{uid}ouro)"/><rect x="{x - 1.6}" y="{256 - h}" width="3.2" height="{h}" fill="url(#{uid}ouro)"/>'
                 f'<rect x="{x - 3}" y="{246 - h}" width="6" height="12" fill="#f8f4ea"/><circle cx="{x}" cy="{240 - h}" r="7" fill="url(#{uid}chama)"/>')
    # flores dos lados
    for x in (106, 284):
        o.append(f'<path d="M{x - 6} 262h12l-2 -14h-8z" fill="url(#{uid}ouro)"/>' + "".join(
            f'<circle cx="{x + rnd.uniform(-10, 10):.0f}" cy="{240 + rnd.uniform(-8, 6):.0f}" r="{rnd.uniform(3, 5):.1f}" fill="{rnd.choice(["#f8f4ea", "#f2c94c", "#e8e2d0"])}"/>' for _ in range(9)))
    # mesa de comunhão (balaustrada) na frente
    o.append(f'<rect x="0" y="388" width="{W}" height="8" fill="{p["madeiraLuz"]}"/>' + "".join(
        f'<path d="M{x} 396q-5 10 0 18q5 8 0 16" stroke="{p["madeira"]}" stroke-width="7" fill="none"/>' for x in range(14, W, 26)) +
        f'<rect x="0" y="430" width="{W}" height="6" fill="{p["madeira"]}"/>')
    o.append('</g>')
    o.append(f'<ellipse cx="195" cy="320" rx="150" ry="60" fill="{p["luz"]}" opacity=".08" filter="url(#{uid}bl)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#{uid}vela)"/></svg>')
    return "".join(o)
