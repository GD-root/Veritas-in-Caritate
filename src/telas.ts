/* O HTML de cada parte da tela. Funções puras: recebem o estado e devolvem texto (por isso dá para testar). */
import { CIC_DET, PARTES, SITE_CIC, TEMAS } from "./dados";
import { ICONE } from "./icones";
import type { Bloco, Ficha, Referencia } from "./tipos";
import { esc, norm, quando } from "./util";

type TipoLinha = "biblia" | "cic" | "trad";

function linhas(arr: Referencia[], tipo: TipoLinha = "biblia"): string {
  return "<ul>" + arr.map(({ ref, texto }) => {
    if (tipo === "cic" && CIC_DET[ref]) return `<li><button class="ref cicbtn" data-ref="${esc(ref)}" aria-haspopup="dialog">${esc(ref)} <span aria-hidden="true">＋</span></button><span>${esc(texto)}</span></li>`;
    return `<li><span class="ref">${esc(tipo === "trad" ? quando(ref) : ref)}</span><span>${esc(texto)}</span></li>`;
  }).join("") + "</ul>";
}

/** Título da ficha: objeções vêm entre aspas; assuntos ("simples"), sem. */
export function tituloFicha(d: Ficha): string {
  return d.simples ? d.pergunta : "“" + d.pergunta + "”";
}

export function ficha(tema: number, bloco: Bloco, bi: number, d: Ficha, i: number, aberto: boolean, rotulo: boolean): string {
  const id = `r${tema}-${bi}-${i}`;
  const tit = d.simples ? esc(d.pergunta) : "“" + esc(d.pergunta) + "”";
  const temBalao = d.catecismo.some(({ ref }) => CIC_DET[ref]);
  return `<section class="item ${bloco.cor}">
    <button class="q" aria-expanded="${aberto}" aria-controls="${id}">
      <span class="num">${i + 1}</span><span class="qt${d.simples ? " reto" : ""}">${tit}</span><span class="mark" aria-hidden="true">${aberto ? "−" : "+"}</span>
    </button>
    <div class="body" id="${id}" ${aberto ? "" : "hidden"}>
      ${rotulo ? `<p class="onde">${esc(bloco.nome)}</p>` : ""}
      <div class="short"><h3>${esc(d.tituloResposta || (d.simples ? "O que é" : "Resposta curta"))}</h3><p>${esc(d.resposta)}</p></div>
      <div><h3>Na Bíblia</h3>${linhas(d.biblia)}</div>
      <div><h3>No Catecismo</h3>${linhas(d.catecismo, "cic")}${temBalao ? '<p class="dica">Toque nos números com ＋ para ver o que cada parágrafo ensina.</p>' : ""}</div>
      <div><h3>Na Tradição</h3>${linhas(d.tradicao, "trad")}</div>
      <p class="say"><b>${esc(d.rotuloConversa || "Como conversar")}:</b> ${esc(d.conversa)}</p>
      <div class="foot"><button class="copy" data-b="${bi}" data-i="${i}">Copiar referências</button></div>
    </div>
  </section>`;
}

export function partesHTML(tema: number): string {
  return TEMAS.map((t, i) => `<button class="parte" data-t="${i}" ${i === tema ? 'aria-current="true"' : ""}>${ICONE[t.nome] || ""}${esc(t.nome)}</button>`).join("");
}

export function chipsHTML(tema: number, ativo: number): string {
  return TEMAS[tema].blocos.map((b, i) => `<button class="chip ${b.cor}" data-b="${i}" ${i === ativo ? 'aria-current="true"' : ""}>${ICONE[b.nome] || ""}${esc(b.nome)}</button>`).join("");
}

/** Texto em que a busca procura: título, resposta, conselho e todas as referências. */
function textoDaFicha(d: Ficha): string {
  const refs = [...d.biblia, ...d.catecismo, ...d.tradicao].flatMap((r) => [r.ref, r.texto]);
  return norm([d.pergunta, d.resposta, d.conversa, ...refs].join(" "));
}

export function listaHTML(tema: number, ativo: number, busca: string): string {
  const blocos = TEMAS[tema].blocos;
  const t = norm(busca.trim());
  if (t) {
    let html = "";
    blocos.forEach((b, bi) => b.itens.forEach((d, i) => {
      if (textoDaFicha(d).includes(t)) html += ficha(tema, b, bi, d, i, false, true);
    }));
    return html || '<p class="empty">Nenhuma ficha deste tema contém esse termo. Tente outra palavra ou outra passagem.</p>';
  }
  const b = blocos[ativo];
  return b.itens.map((d, i) => ficha(tema, b, ativo, d, i, i === 0, false)).join("");
}

/** Texto copiado pelo botão "Copiar referências". */
export function textoParaCopiar(d: Ficha): string {
  return tituloFicha(d) + "\n\n" + d.resposta + "\n\nBíblia: " + d.biblia.map((x) => x.ref).join("; ") + "\nCatecismo: " + d.catecismo.map((x) => x.ref).join("; ") + "\n\nVeritas in Caritate";
}

/** Janela com a explicação dos parágrafos do Catecismo. */
export function janelaCatecismo(ref: string, cor: string): { cls: string; tit: string; corpo: string } | null {
  const det = CIC_DET[ref];
  if (!det) return null;
  const n = +ref.match(/\d+/)![0];
  const parte = PARTES.find((p) => n >= p[0] && n <= p[1])!;
  return {
    cls: "mcaixa " + cor,
    tit: "Catecismo da Igreja Católica, n. " + ref.replace("CIC ", ""),
    corpo: det.map(({ n: k, texto }) => `<p><b>${esc(k)}</b> ${esc(texto)}</p>`).join("") +
      `<p class="mnota">Explicação com palavras próprias. O texto completo dos parágrafos está no próprio site do Vaticano, na parte que vai do § ${parte[0]} ao § ${parte[1]}.</p>
     <p><a class="mlink" href="${SITE_CIC}" target="_blank" rel="noopener">vatican.va · Catecismo da Igreja Católica</a></p>`,
  };
}
