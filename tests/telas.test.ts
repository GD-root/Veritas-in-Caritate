/* O que continua igual à versão 1. */
import { describe, expect, it } from "vitest";
import { lerGabarito } from "./gabarito";
import { janelaCatecismo } from "../src/telas";
import { quando } from "../src/util";

interface Gabarito {
  blocos: Record<string, { partes: string; chips: string; lista: string }>;
  buscas: Record<string, string>;
  modais: Record<string, { cls: string; tit: string; corpo: string }>;
  quando: Record<string, string>;
}
const g = lerGabarito<Gabarito>("telas");

/* As telas foram redesenhadas (tema "dentro da igreja", vistas.test.ts confere o conteúdo de cada ficha).
   Daqui continuam valendo a janela do Catecismo (sem o quadro "Onde fica", que entrou depois) e as datas. */
const semOndeFica = (h: string) => h.replace(/<div class="monde">.*?<\/ol><\/div>/s, "");

describe("janelas e datas iguais à versão 1", () => {
  it("janelas do Catecismo", () => {
    for (const [chave, esperado] of Object.entries(g.modais)) {
      const [ref, cor] = chave.split("|");
      const j = janelaCatecismo(ref, cor)!;
      expect(j.corpo).toContain('<div class="monde">');
      expect({ ...j, corpo: semOndeFica(j.corpo) }).toEqual(esperado);
    }
  });
  it("datas da Tradição", () => {
    for (const [r, esperado] of Object.entries(g.quando)) expect(quando(r)).toBe(esperado);
  });
});
