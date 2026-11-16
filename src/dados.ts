/* Junta os temas com as fichas de cada bloco. Para acrescentar um bloco: crie src/dados/blocos/<id>.json,
   importe aqui e ponha o bloco em src/dados/temas.json. */
import temasInfo from "./dados/temas.json";
import explicacoes from "./dados/catecismo-explicacoes.json";
import partes from "./dados/catecismo-partes.json";
import estrutura from "./dados/catecismo-estrutura.json";
import maria from "./dados/blocos/maria.json";
import igreja from "./dados/blocos/igreja.json";
import escritura from "./dados/blocos/escritura.json";
import sacramentos from "./dados/blocos/sacramentos.json";
import cristo from "./dados/blocos/cristo.json";
import imagens from "./dados/blocos/imagens.json";
import solas from "./dados/blocos/solas.json";
import teologais from "./dados/blocos/teologais.json";
import cardeais from "./dados/blocos/cardeais.json";
import vida from "./dados/blocos/vida.json";
import type { EstruturaCatecismo, Explicacao, Ficha, Tema, TemaInfo } from "./tipos";

const FICHAS: Record<string, Ficha[]> = { maria, igreja, escritura, sacramentos, cristo, imagens, solas, teologais, cardeais, vida };

export const TEMAS: Tema[] = (temasInfo as TemaInfo[]).map((t) => ({
  nome: t.nome,
  blocos: t.blocos.map((b) => {
    const itens = FICHAS[b.id];
    if (!itens) throw new Error("Bloco sem arquivo de fichas: " + b.id);
    return { ...b, itens };
  }),
}));

/** Explicações dos parágrafos do Catecismo, pela referência ("CIC 75-79"). */
export const CIC_DET = explicacoes as Record<string, Explicacao[]>;

/** Trechos do Catecismo como divididos no site do Vaticano. */
export const PARTES = partes.partes as [number, number][];
export const SITE_CIC = partes.site;

/** Títulos e numeração do Catecismo (gerado do Drive por ferramentas/gerar_dados.py). */
export const ESTRUTURA = estrutura as EstruturaCatecismo;
