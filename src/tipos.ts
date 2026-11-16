/* Formato dos dados do Veritas in Caritate (src/dados). O TypeScript avisa se algum campo faltar. */

/** Uma linha de referência: "Lc 1,28" + o que a passagem diz, resumido. */
export interface Referencia {
  ref: string;
  texto: string;
}

/** Uma ficha: a objeção (ou o assunto) e a resposta com Bíblia, Catecismo e Tradição. */
export interface Ficha {
  /** true quando o título é um assunto ("O que é a fé") e não uma objeção entre aspas */
  simples?: boolean;
  pergunta: string;
  /** título do quadro da resposta; padrão "Resposta curta" (ou "O que é", nas fichas simples) */
  tituloResposta?: string;
  resposta: string;
  biblia: Referencia[];
  catecismo: Referencia[];
  tradicao: Referencia[];
  /** rótulo do conselho final; padrão "Como conversar" */
  rotuloConversa?: string;
  conversa: string;
}

/** Cores de cada bloco (classes do CSS). */
export type CorBloco = "" | "tema-mariana" | "tema-liturgica" | "tema-branca" | "tema-roxa" | "tema-vermelha";

export interface BlocoInfo {
  /** nome do arquivo em src/dados/blocos */
  id: string;
  nome: string;
  cor: CorBloco;
}
export interface TemaInfo {
  nome: string;
  blocos: BlocoInfo[];
}
export interface Bloco extends BlocoInfo {
  itens: Ficha[];
}
export interface Tema {
  nome: string;
  blocos: Bloco[];
}

/** Explicação, com palavras próprias, de um parágrafo do Catecismo ("75" ou "109-110"). */
export interface Explicacao {
  n: string;
  texto: string;
}

/* ---------- Estrutura do Catecismo (gerada a partir do Drive por ferramentas/gerar_dados.py) ---------- */
export interface DivisaoCatecismo {
  /** "parte", "secao", "capitulo", "artigo" ou "paragrafo" */
  nivel: string;
  titulo: string;
  de: number;
  ate: number;
}
export interface EstruturaCatecismo {
  fonte: string;
  gerado: string;
  divisoes: DivisaoCatecismo[];
}
