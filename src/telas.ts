/* Peças comuns às telas: referências ao Catecismo, título e texto para copiar de uma ficha, e a janela do Catecismo.
   As telas em si ficam em vistas.ts. */
import { CIC_DET, ESTRUTURA, PARTES, SITE_CIC } from "./dados";
import type { Ficha } from "./tipos";
import { esc } from "./util";

/** Primeiro número de uma referência ao Catecismo ("CIC 75-79" -> 75), ou null. */
export function numeroCIC(ref: string): number | null {
  const m = ref.match(/^CIC\s+(\d{1,4})/);
  return m && +m[1] >= 1 && +m[1] <= 2865 ? +m[1] : null;
}

/** Título da ficha: objeções vêm entre aspas; assuntos ("simples"), sem. */
export function tituloFicha(d: Ficha): string {
  return d.simples ? d.pergunta : "“" + d.pergunta + "”";
}

/** Texto copiado pelo botão "Copiar referências". */
export function textoParaCopiar(d: Ficha): string {
  return tituloFicha(d) + "\n\n" + d.resposta + "\n\nBíblia: " + d.biblia.map((x) => x.ref).join("; ") + "\nCatecismo: " + d.catecismo.map((x) => x.ref).join("; ") + "\n\nVeritas in Caritate";
}

const NIVEIS_CAMINHO = ["parte", "secao", "capitulo", "artigo", "paragrafo", "subtitulo"];

/** Onde um número fica no Catecismo: Parte › Secção › Capítulo › Artigo › Parágrafo › subtítulo. */
export function ondeFica(n: number) {
  return ESTRUTURA.divisoes.filter((d) => d.de <= n && n <= d.ate && NIVEIS_CAMINHO.includes(d.nivel));
}

function ondeFicaHTML(n: number): string {
  const caminho = ondeFica(n);
  if (!caminho.length) return "";
  return '<div class="monde"><h3>Onde fica no Catecismo</h3><ol>' +
    caminho.map((d) => `<li>${esc(d.titulo)} <small>§ ${d.de === d.ate ? d.de : d.de + "–" + d.ate}</small></li>`).join("") + "</ol></div>";
}

/** Janela do Catecismo: a explicação dos parágrafos (quando o app tem) e onde eles ficam no Catecismo. */
export function janelaCatecismo(ref: string, cor: string): { cls: string; tit: string; corpo: string } | null {
  const det = CIC_DET[ref];
  const n = numeroCIC(ref);
  if (!det && n === null) return null;
  const num = n ?? +ref.match(/\d+/)![0];
  const parte = PARTES.find((p) => num >= p[0] && num <= p[1])!;
  const tit = "Catecismo da Igreja Católica, n. " + ref.replace("CIC ", "");
  const link = `<p><a class="mlink" href="${SITE_CIC}" target="_blank" rel="noopener">vatican.va · Catecismo da Igreja Católica</a></p>`;
  if (!det) {
    return {
      cls: "mcaixa " + cor, tit,
      corpo: ondeFicaHTML(num) + `<p class="mnota">O texto completo está no site do Vaticano, na parte que vai do § ${parte[0]} ao § ${parte[1]}.</p>\n     ` + link,
    };
  }
  return {
    cls: "mcaixa " + cor, tit,
    corpo: det.map(({ n: k, texto }) => `<p><b>${esc(k)}</b> ${esc(texto)}</p>`).join("") + ondeFicaHTML(num) +
      `<p class="mnota">Explicação com palavras próprias. O texto completo dos parágrafos está no próprio site do Vaticano, na parte que vai do § ${parte[0]} ao § ${parte[1]}.</p>
     ` + link,
  };
}
