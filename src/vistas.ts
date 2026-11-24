/* As telas do Veritas (tema "dentro da igreja"): início, temas, tema, bloco, ficha e busca.
   Funções puras: recebem o que precisam e devolvem o HTML (por isso dá para testar). */
import { CIC_DET, TEMAS } from "./dados";
import { ICONE } from "./icones";
import { numeroCIC, textoParaCopiar, tituloFicha } from "./telas";
import type { Ficha, Referencia } from "./tipos";
import { esc, norm } from "./util";
import { buscarConhecer, linhaConhecer, portaConhecerHTML } from "./conhecer";

/** Endereço do Praesto Sum, o app irmão sobre a liturgia. */
export const PRAESTO = "https://gd-root.github.io/praesto-summ/";

/** Fichas lidas, guardadas como "tema-bloco-ficha". */
export type Lidas = Set<string>;
export const chave = (t: number, b: number, i: number) => `${t}-${b}-${i}`;

/** Tira das lidas o que o botão de zerar alcança: "tudo", um tema ("2") ou um bloco ("2/1"). */
export function zerarLidas(l: Lidas, alvo: string): void {
  if (alvo === "tudo") { l.clear(); return; }
  const [t, b] = alvo.split("/");
  const prefixo = b === undefined ? `${t}-` : `${t}-${b}-`;
  for (const k of [...l]) if (k.startsWith(prefixo)) l.delete(k);
}

/** Papel de parede de cada tema (public/fundos/<nome>-escuro.svg e -claro.svg). */
export const FUNDO_TEMA = ["defesa", "reforma", "valores", "libertacao"];

/** Símbolo do medalhão do vitral (public/fundos/simbolos/<nome>.svg): o do tema ou o do bloco. */
export function simbolo(t?: number, b?: number): string {
  if (t === undefined) return "veritas";
  if (b === undefined) return FUNDO_TEMA[t] || "veritas";
  const id = TEMAS[t].blocos[b].id;
  return id === "libertacao" ? "libertacao-bloco" : id;
}

/** Breve apresentação de cada tema, mostrada na tela do tema. */
const SOBRE_TEMA: Record<string, string> = {
  "Defesa da fé": "As objeções mais comuns sobre Maria, a Igreja, a Bíblia, os sacramentos e os santos.",
  "Resposta à Reforma": "As cinco solas da Reforma, uma a uma, com a resposta católica.",
  "Valores católicos": "As virtudes e a vida em família, à luz da fé.",
  "Teologia da Libertação": "O que a Igreja ensina, os erros que ela corrigiu e o zelo pela Eucaristia e pela liturgia.",
};
/** Capas dos livros (cores do vitral de cada tema). */
const CAPA = ["#7a1f33,#3d0c18", "#5a2a7a,#2a1040", "#1f5a46,#0c2a20", "#8a5a14,#3a2408"];

/** Atalhos do início: levam direto ao bloco ou à ficha. */
const ATALHOS: [string, string, number?][] = [["Maria", "maria"], ["Papa", "igreja"], ["Imagens", "imagens"], ["Purgatório", "sacramentos", 0], ["Sola Scriptura", "solas", 0]];
/** As objeções que mais aparecem nas conversas. */
const PROCURADAS: [string, number][] = [["imagens", 0], ["maria", 4], ["sacramentos", 1], ["sacramentos", 0]];

const SV = (d: string, w = 20) => `<svg width="${w}" height="${w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
export const IC = {
  chev: SV('<path d="M9 6l6 6-6 6"/>', 16),
  busca: SV('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>', 18),
  salvar: SV('<path d="M6 3h12v18l-6-4-6 4z"/>', 17),
  salva: '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h12v18l-6-4-6 4z"/></svg>',
  copiar: SV('<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16V6a2 2 0 0 1 2-2h10"/>', 17),
  zap: SV('<path d="M4 20l1.5-4A8 8 0 1 1 9 19z"/>', 17),
  ok: SV('<path d="M5 12.5l4.5 4.5L19 7"/>', 13),
};

/** Onde está o bloco com esse id: [tema, bloco], ou null. */
export function acharBloco(id: string): [number, number] | null {
  for (let t = 0; t < TEMAS.length; t++) {
    const b = TEMAS[t].blocos.findIndex((x) => x.id === id);
    if (b >= 0) return [t, b];
  }
  return null;
}

function lidasNo(t: number, b: number, l: Lidas): number {
  return TEMAS[t].blocos[b].itens.filter((_, i) => l.has(chave(t, b, i))).length;
}
function totalTema(t: number) { return TEMAS[t].blocos.reduce((s, b) => s + b.itens.length, 0); }
function lidasTema(t: number, l: Lidas) { return TEMAS[t].blocos.reduce((s, _, b) => s + lidasNo(t, b, l), 0); }
const barra = (f: number, n: number) => `<div class="barra" role="img" aria-label="${f} de ${n} lidas"><i style="width:${n ? Math.round((100 * f) / n) : 0}%"></i></div>`;
/** Contagem de lidas com o botão redondo de zerar (só aparece quando há alguma lida). alvo: "tudo", "t" ou "t/b". */
function contaLidas(f: number, n: number, alvo: string, onde: string): string {
  const bt = f ? `<button class="zerar" data-zerar="${alvo}" aria-label="Zerar as fichas lidas ${onde}" title="Zerar as lidas"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7"/><path d="M4 4v5h5"/></svg></button>` : "";
  return `<div class="conta-lidas"><small class="conta">${f} de ${plural(n, "ficha lida", "fichas lidas")}</small>${bt}</div>`;
}
const plural = (n: number, um: string, varios: string) => n + " " + (n === 1 ? um : varios);

function livros(l: Lidas): string {
  return '<div class="livros">' + TEMAS.map((t, k) =>
    `<a class="livro" href="#t/${k}" style="--capa:linear-gradient(160deg,${CAPA[k]})"><span class="em">${ICONE[t.nome] || ""}</span>` +
    `<span class="nm">${esc(t.nome)}</span><small>${plural(totalTema(k), "ficha", "fichas")}${lidasTema(k, l) ? " · " + lidasTema(k, l) + " lidas" : ""}</small></a>`).join("") + "</div>";
}

function linhaFicha(t: number, b: number, i: number, d: Ficha, l: Lidas, onde = false): string {
  const lida = l.has(chave(t, b, i));
  return `<a class="lin${lida ? " lida" : ""}" href="#t/${t}/${b}/${i}"><span class="obj">${esc(tituloFicha(d))}` +
    (onde ? `<small>${esc(TEMAS[t].blocos[b].nome)}</small>` : "") + "</span>" + (lida ? `<span class="ok" aria-label="lida">${IC.ok}</span>` : "") + IC.chev + "</a>";
}

/* ---------------- Início ---------------- */
export function inicioHTML(l: Lidas): string {
  const atalhos = ATALHOS.map(([nome, id, i]) => {
    const tb = acharBloco(id);
    return tb ? `<a class="atalho" href="#t/${tb[0]}/${tb[1]}${i === undefined ? "" : "/" + i}">${esc(nome)}</a>` : "";
  }).join("");
  const proc = PROCURADAS.map(([id, i]) => {
    const tb = acharBloco(id);
    const d = tb && TEMAS[tb[0]].blocos[tb[1]].itens[i];
    return tb && d ? linhaFicha(tb[0], tb[1], i, d, l) : "";
  }).join("");
  return '<div class="espaco"></div>' +
    `<section class="painel centro"><p class="sobre-rot">Apologética católica</p><h2>O que perguntaram a você hoje?</h2>` +
    `<form class="busca" data-ir-busca><span>${IC.busca}</span><input type="search" name="q" placeholder="Digite a objeção ou a passagem…" aria-label="Buscar objeção ou passagem" autocomplete="off"></form>` +
    `<nav class="atalhos" aria-label="Atalhos">${atalhos}</nav></section>` +
    `<h3 class="rot">Os temas <span>${plural(TEMAS.reduce((s, _, k) => s + totalTema(k), 0), "ficha", "fichas")}</span></h3>${livros(l)}` +
    `<h3 class="rot">Mais procuradas</h3><div class="painel lista">${proc}</div>` +
    /* atalho para o app irmão, o Praesto Sum (o guia da liturgia) */
    `<a class="ponte" href="${PRAESTO}" target="_blank" rel="noopener"><img src="praesto-sum.png" alt="" width="52" height="52"><span class="txt"><b>Quer saber mais sobre a Santa Liturgia?</b><small>Abrir o Praesto Sum</small></span>${IC.chev}</a>` +
    '<section class="painel centro sobre"><p>Para entender a fé, crescer nela e saber explicar com serenidade o que a Igreja crê e por quê: a passagem da Bíblia, o número do Catecismo e a voz dos primeiros cristãos.</p>' +
    "<p>As passagens bíblicas estão resumidas: abra a sua Bíblia na referência para ler o texto. Os números do Catecismo seguem o Catecismo da Igreja Católica. Conhecer a verdade para vivê-la e partilhá-la com caridade: quem pergunta merece respeito, mesmo quando discorda.</p>" +
    '<p class="verso">“Seguindo a verdade na caridade.”<small>Efésios 4,15</small></p></section>';
}

/* ---------------- Temas (os quatro livros) ---------------- */
export function temasHTML(l: Lidas, dicaIgreja = false): string {
  const total = TEMAS.reduce((s, _, k) => s + totalTema(k), 0);
  return `<div class="espaco curto"></div><section class="painel centro"><h2>Os temas</h2><p class="sub">Escolha um livro da estante.</p>${contaLidas(l.size, total, "tudo", "de todos os temas")}</section>` + livros(l) +
    '<div class="painel lista">' + TEMAS.map((t, k) =>
      `<a class="lin" href="#t/${k}"><span class="ic">${ICONE[t.nome] || ""}</span><span class="txt"><b>${esc(t.nome)}</b><small>${esc(SOBRE_TEMA[t.nome] || "")}</small>${barra(lidasTema(k, l), totalTema(k))}</span>${IC.chev}</a>`).join("") + "</div>" + portaConhecerHTML(dicaIgreja);
}

/* ---------------- Um tema: os blocos ---------------- */
export function temaHTML(t: number, l: Lidas): string {
  const tm = TEMAS[t];
  const n = totalTema(t), f = lidasTema(t, l);
  return '<div class="espaco"></div>' +
    `<section class="painel centro"><h2>${esc(tm.nome)}</h2><p class="sub">${esc(SOBRE_TEMA[tm.nome] || "")}</p>${barra(f, n)}${contaLidas(f, n, String(t), "deste tema")}</section>` +
    '<h3 class="rot">Os blocos <span>lidas</span></h3><div class="painel lista">' +
    tm.blocos.map((b, k) => {
      const lb = lidasNo(t, k, l);
      return `<a class="lin ${b.cor}" href="#t/${t}/${k}"><span class="ic">${ICONE[b.nome] || ""}</span><span class="txt"><b>${esc(b.nome)}</b><small>${lb} de ${b.itens.length} lidas</small>${barra(lb, b.itens.length)}</span><span class="qt">${b.itens.length}</span>${IC.chev}</a>`;
    }).join("") + "</div>";
}

/* ---------------- Um bloco: as fichas ---------------- */
export function blocoHTML(t: number, b: number, l: Lidas): string {
  const bl = TEMAS[t].blocos[b];
  const f = lidasNo(t, b, l);
  return '<div class="espaco"></div>' +
    `<section class="painel centro ${bl.cor}"><p class="sobre-rot">${esc(TEMAS[t].nome)}</p><h2>${esc(bl.nome)}</h2>${barra(f, bl.itens.length)}${contaLidas(f, bl.itens.length, t + "/" + b, "deste bloco")}</section>` +
    '<div class="painel lista">' + bl.itens.map((d, i) => linhaFicha(t, b, i, d, l)).join("") + "</div>";
}

/* ---------------- A ficha ---------------- */
function refsCatecismo(arr: Referencia[]): string {
  return arr.map(({ ref, texto }) => {
    const r = esc(ref);
    const bt = CIC_DET[ref] ? `<button class="ref cicbtn" data-ref="${r}" aria-haspopup="dialog">${r} <span aria-hidden="true">＋</span></button>`
      : numeroCIC(ref) ? `<button class="ref cicbtn cicloc" data-ref="${r}" aria-haspopup="dialog">${r}</button>` : `<span class="ref">${r}</span>`;
    return `<p>${bt} ${esc(texto)}</p>`;
  }).join("");
}

export function fichaHTML(t: number, b: number, i: number, salva = false): string {
  const bl = TEMAS[t].blocos[b], d = bl.itens[i];
  const ant = i > 0 ? `<a class="bt" href="#t/${t}/${b}/${i - 1}">‹ Anterior</a>` : "<span></span>";
  const prox = i < bl.itens.length - 1 ? `<a class="bt" href="#t/${t}/${b}/${i + 1}">Próxima ›</a>` : `<a class="bt" href="#t/${t}/${b}">Voltar ao bloco</a>`;
  const zap = "https://wa.me/?text=" + encodeURIComponent(textoParaCopiar(d));
  const temBalao = d.catecismo.some(({ ref }) => CIC_DET[ref]);
  return '<div class="espaco"></div>' +
    `<section class="painel centro objecao ${bl.cor}"><p class="sobre-rot">${d.simples ? esc(bl.nome) : "A objeção"}</p><h2 class="${d.simples ? "reto" : "obj"}">${esc(tituloFicha(d))}</h2></section>` +
    `<section class="painel resposta"><h3>${esc(d.tituloResposta || (d.simples ? "O que é" : "Resposta curta"))}</h3><p>${esc(d.resposta)}</p></section>` +
    `<section class="painel"><h3 class="rot dentro">Da Escritura à Tradição <span>${d.biblia.length + d.catecismo.length + d.tradicao.length} fontes</span></h3><div class="tempo">` +
    `<div class="no"><h4>Na Bíblia</h4>${d.biblia.map(({ ref, texto }) => `<p><span class="ref">${esc(ref)}</span> ${esc(texto)}</p>`).join("")}</div>` +
    `<div class="no"><h4>No Catecismo</h4>${refsCatecismo(d.catecismo)}${temBalao ? '<p class="dica">Toque nos números com ＋ para ver o que cada parágrafo ensina.</p>' : ""}</div>` +
    `<div class="no"><h4>${esc(d.rotuloTradicao || "Na Tradição")}</h4>${d.tradicao.map(({ ref, texto }) => `<p><span class="ano">${esc(ref)}</span> ${esc(texto)}</p>`).join("")}</div>` +
    "</div></section>" +
    `<div class="acoes"><button class="bt${salva ? " salva" : ""}" data-salvar aria-pressed="${salva}">${botaoSalvar(salva)}</button><button class="bt" data-copiar>${IC.copiar} Copiar</button><a class="bt zap" href="${zap}" target="_blank" rel="noopener">${IC.zap} WhatsApp</a></div>` +
    `<nav class="passos" aria-label="Outras fichas do bloco">${ant}<small>${i + 1} de ${bl.itens.length}</small>${prox}</nav>`;
}

/** Rótulo do botão de salvar a ficha. */
export function botaoSalvar(salva: boolean): string {
  return salva ? IC.salva + " Salva" : IC.salvar + " Salvar";
}

/* ---------------- Salvas ---------------- */
export function salvasHTML(salvas: Set<string>, l: Lidas): string {
  let grupos = "";
  TEMAS.forEach((tm, t) => {
    const linhas = tm.blocos.flatMap((bl, b) => bl.itens.map((d, i) => (salvas.has(chave(t, b, i)) ? linhaFicha(t, b, i, d, l, true) : ""))).join("");
    if (linhas) grupos += `<h3 class="rot">${esc(tm.nome)}</h3><div class="painel lista">${linhas}</div>`;
  });
  return '<div class="espaco curto"></div>' +
    `<section class="painel centro"><h2>Para ter à mão na próxima conversa</h2><p class="sub">${salvas.size ? plural(salvas.size, "ficha salva", "fichas salvas") + " neste aparelho." : "Nenhuma ficha salva ainda."}</p></section>` +
    (grupos || `<p class="vazio painel">Abra uma ficha e toque em <b>Salvar</b>. Ela aparece aqui, pronta para mostrar ou mandar no WhatsApp.</p>`);
}

/* ---------------- Busca em todos os temas ---------------- */
function textoDaFicha(d: Ficha): string {
  const refs = [...d.biblia, ...d.catecismo, ...d.tradicao].flatMap((r) => [r.ref, r.texto]);
  return norm([d.pergunta, d.resposta, ...refs].join(" "));
}

/** Fichas que contêm o termo (sem acentos), de todos os temas. */
export function buscar(q: string): [number, number, number][] {
  const t = norm(q.trim());
  const r: [number, number, number][] = [];
  if (!t) return r;
  TEMAS.forEach((tm, ti) => tm.blocos.forEach((b, bi) => b.itens.forEach((d, i) => { if (textoDaFicha(d).includes(t)) r.push([ti, bi, i]); })));
  return r;
}

/** Resultados da busca (a lista muda enquanto se digita, sem redesenhar o campo). */
export function resultadosHTML(q: string, l: Lidas): string {
  const r = buscar(q), rc = buscarConhecer(q), n = r.length + rc.length;
  const conta = q.trim() ? `<small class="conta">${plural(n, "ficha encontrada", "fichas encontradas")}</small>` : "";
  return conta + (!q.trim() ? '<p class="vazio">Digite uma palavra, uma objeção, uma passagem (Lc 1) ou um número do Catecismo (495).</p>'
    : n ? (r.length ? '<div class="painel lista">' + r.map(([t, b, i]) => linhaFicha(t, b, i, TEMAS[t].blocos[b].itens[i], l, true)).join("") + "</div>" : "") +
      (rc.length ? '<h3 class="rot">Conhecer a Igreja</h3><div class="painel lista">' + rc.map(([k, i]) => linhaConhecer(k, i)).join("") + "</div>" : "")
      : '<p class="vazio">Nenhuma ficha contém esse termo. Tente outra palavra ou outra passagem.</p>');
}

export function buscaHTML(q: string, l: Lidas): string {
  return '<div class="espaco curto"></div>' +
    `<section class="painel centro"><h2>Buscar</h2><form class="busca" data-busca><span>${IC.busca}</span><input id="q" type="search" name="q" value="${esc(q)}" placeholder="Ex.: irmãos, Lc 1, virgem, 495" aria-label="Buscar em todos os temas" autocomplete="off"></form></section>` +
    `<div id="resultados">${resultadosHTML(q, l)}</div>`;
}
