/* "Conhecer a Igreja": a área que se abre no altar, com perguntas curtas sobre gestos, objetos, vestes,
   canto, história, devoções e as novas comunidades. Funções puras que devolvem o HTML. */
import dados from "./dados/conhecer.json";
import { esc, norm } from "./util";

export type ItemConhecer = { pergunta: string; resposta: string; entenda: string; origem: string; fontes: string[] };
export type CategoriaConhecer = { id: string; nome: string; sobre: string; itens: ItemConhecer[] };
export const CATEGORIAS = dados.categorias as CategoriaConhecer[];

const S = (d: string) => `<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
/** Ícone de cada categoria. */
export const ICONE_CAT: Record<string, string> = {
  gestos: S('<path d="M9 11V5.5a1.5 1.5 0 0 1 3 0V11M12 10V4.5a1.5 1.5 0 0 1 3 0V11M15 10.5V6.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-.5A5.5 5.5 0 0 1 5 16.2L3.6 12.4a1.4 1.4 0 0 1 2.5-1.3L9 15"/>'),
  altar: S('<path d="M3 20h18M5 20v-7h14v7M4 13h16"/><path d="M8 13V8M16 13V8M12 13V4M10 6h4"/><path d="M8 6.5c.6-.6.6-1.4 0-2-.6.6-.6 1.4 0 2zM16 6.5c.6-.6.6-1.4 0-2-.6.6-.6 1.4 0 2z"/>'),
  vestes: S('<path d="M12 3c-1.5 0-2.5.6-3 1.4C5.5 5.5 3.5 9 3 16c2.5 2.5 6 4 9 4s6.5-1.5 9-4c-.5-7-2.5-10.5-6-11.6-.5-.8-1.5-1.4-3-1.4z"/><path d="M12 7v11M9 10.5h6"/>'),
  canto: S('<path d="M4 6h16M4 10h16M4 14h16M4 18h16"/><rect x="7" y="8" width="3" height="3" fill="currentColor"/><rect x="12" y="12" width="3" height="3" fill="currentColor"/><path d="M15 12V6"/>'),
  historia: S('<path d="M7 4h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H7"/><path d="M7 4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2 2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/><path d="M12 8h4M12 12h4M12 16h2"/>'),
  devocoes: S('<circle cx="12" cy="9" r="5.5" stroke-dasharray="1.2 2.1"/><path d="M12 14.5V17M12 17v4M10.2 19h3.6"/>'),
  comunidades: S('<path d="M4 12c3 0 5-1.5 6.5-4l1.5 3 2-5c1 2 3 3.5 6 3-1.5 3.5-4.5 6-8 6.5L10 21l-1-5c-2-.5-4-2-5-4z"/><circle cx="16.2" cy="7.6" r=".5" fill="currentColor"/>'),
};
const CHEV = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';

/** Botão da estante de temas que leva à área, com o balão de aviso nas primeiras vezes. */
export function portaConhecerHTML(mostrarDica: boolean): string {
  return `<a class="porta-igreja" href="#igreja"><span class="selo"><img src="fundos/simbolos/igreja.svg" alt=""></span>` +
    '<span class="txt"><b>Conhecer a Igreja</b></span>' + CHEV +
    (mostrarDica ? '<span class="balao-igreja" aria-hidden="true">Quer conhecer a Igreja por dentro? Toque aqui</span>' : "") + "</a>";
}

/** A entrada da área, diante do altar: as caixas das categorias. */
export function conhecerHTML(): string {
  return '<div class="espaco"></div><section class="painel centro"><p class="sobre-rot">Diante do altar</p><h2>Conhecer a Igreja</h2>' +
    '<p class="sub">Por que fazemos o que fazemos: o sentido dos gestos, dos objetos, das vestes, do canto e da história da Santa Igreja.</p></section>' +
    '<div class="caixas">' + CATEGORIAS.map((c, k) =>
      `<a class="caixa${c.itens.length ? "" : " breve"}" href="#igreja/${k}"><span class="ic">${ICONE_CAT[c.id] || ""}</span><b>${esc(c.nome)}</b><small>${c.itens.length ? `${c.itens.length} ${c.itens.length === 1 ? "pergunta" : "perguntas"}` : "em breve"}</small></a>`).join("") + "</div>";
}

/** Uma categoria: a lista de perguntas. */
export function categoriaConhecerHTML(k: number): string {
  const c = CATEGORIAS[k];
  return '<div class="espaco"></div>' +
    `<section class="painel centro"><span class="ic-grande">${ICONE_CAT[c.id] || ""}</span><h2>${esc(c.nome)}</h2><p class="sub">${esc(c.sobre)}</p></section>` +
    (c.itens.length ? '<div class="painel lista">' + c.itens.map((it, i) =>
      `<a class="lin" href="#igreja/${k}/${i}"><span class="obj">${esc(it.pergunta)}</span>${CHEV}</a>`).join("") + "</div>"
      : '<section class="painel centro"><p class="sub">As perguntas desta parte estão sendo preparadas.</p></section>');
}

/** Uma pergunta: a resposta curta, "entenda melhor", "de onde vem" e as fontes. */
export function itemConhecerHTML(k: number, i: number): string {
  const c = CATEGORIAS[k], it = c.itens[i];
  const ant = i > 0 ? `<a class="bt" href="#igreja/${k}/${i - 1}">‹ Anterior</a>` : "<span></span>";
  const prox = i < c.itens.length - 1 ? `<a class="bt" href="#igreja/${k}/${i + 1}">Próxima ›</a>` : `<a class="bt" href="#igreja/${k}">Voltar</a>`;
  return '<div class="espaco"></div>' +
    `<section class="painel centro"><p class="sobre-rot">${esc(c.nome)}</p><h2 class="reto">${esc(it.pergunta)}</h2></section>` +
    `<section class="painel resposta"><h3>Em poucas palavras</h3><p>${esc(it.resposta)}</p></section>` +
    `<section class="painel texto"><h3>Entenda melhor</h3><p>${esc(it.entenda)}</p></section>` +
    `<section class="painel texto"><h3>De onde vem</h3><p>${esc(it.origem)}</p></section>` +
    `<section class="painel"><h3>Fontes</h3><div class="fontes">${it.fontes.map((f) => `<span class="ref">${esc(f)}</span>`).join("")}</div></section>` +
    `<nav class="passos" aria-label="Outras perguntas">${ant}<small>${i + 1} de ${c.itens.length}</small>${prox}</nav>`;
}

/** Perguntas que contêm o termo (na pergunta, nas respostas ou nas fontes): [parte, pergunta]. */
export function buscarConhecer(q: string): [number, number][] {
  const t = norm(q.trim()), r: [number, number][] = [];
  if (!t) return r;
  CATEGORIAS.forEach((c, k) => c.itens.forEach((it, i) => {
    if (norm([it.pergunta, it.resposta, it.entenda, it.origem, ...it.fontes].join(" ")).includes(t)) r.push([k, i]);
  }));
  return r;
}
/** Linha de uma pergunta nos resultados da busca. */
export function linhaConhecer(k: number, i: number): string {
  const c = CATEGORIAS[k];
  return `<a class="lin" href="#igreja/${k}/${i}"><span class="obj">${esc(c.itens[i].pergunta)}<small>${esc(c.nome)}</small></span>${CHEV}</a>`;
}
