/* Cada parte da tela precisa produzir o mesmo HTML da versão 1. */
import { describe, expect, it } from "vitest";
import { lerGabarito } from "./gabarito";
import { TEMAS } from "../src/dados";
import { chipsHTML, janelaCatecismo, listaHTML, partesHTML } from "../src/telas";
import { quando } from "../src/util";

interface Gabarito {
  blocos: Record<string, { partes: string; chips: string; lista: string }>;
  buscas: Record<string, string>;
  modais: Record<string, { cls: string; tit: string; corpo: string }>;
  quando: Record<string, string>;
}
const g = lerGabarito<Gabarito>("telas");

describe("telas iguais à versão 1", () => {
  it("tem gabarito de todos os blocos", () => {
    expect(Object.keys(g.blocos).length).toBe(TEMAS.reduce((s, t) => s + t.blocos.length, 0));
  });
  for (const [chave, esperado] of Object.entries(g.blocos)) {
    const [t, b] = chave.split("-").map(Number);
    it(`tema ${t}, bloco ${b}: ${TEMAS[t].blocos[b].nome}`, () => {
      expect(partesHTML(t)).toBe(esperado.partes);
      expect(chipsHTML(t, b)).toBe(esperado.chips);
      expect(listaHTML(t, b, "")).toBe(esperado.lista);
    });
  }
  for (const [chave, esperado] of Object.entries(g.buscas)) {
    const i = chave.indexOf(":");
    const t = +chave.slice(0, i), q = chave.slice(i + 1);
    it(`busca "${q}" no tema ${t}`, () => {
      expect(listaHTML(t, 0, q)).toBe(esperado);
    });
  }
  it("janelas do Catecismo", () => {
    for (const [chave, esperado] of Object.entries(g.modais)) {
      const [ref, cor] = chave.split("|");
      expect(janelaCatecismo(ref, cor)).toEqual(esperado);
    }
  });
  it("datas da Tradição", () => {
    for (const [r, esperado] of Object.entries(g.quando)) expect(quando(r)).toBe(esperado);
  });
});
