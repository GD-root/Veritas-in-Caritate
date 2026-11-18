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

/* Mudanças feitas de propósito depois da versão 1, desfeitas aqui para comparar o resto:
   - números do Catecismo sem explicação própria agora são botões (abrem "onde fica no Catecismo");
   - a janela ganhou o quadro "Onde fica no Catecismo";
   - o quarto tema (Teologia da Libertação) entrou depois, com gabarito próprio em libertacao.test.ts. */
const semBotoesNovos = (h: string) => h.replace(/<button class="ref cicbtn cicloc" data-ref="([^"]*)" aria-haspopup="dialog">([^<]*)<\/button>/g, '<span class="ref">$2</span>');
const semTemaNovo = (h: string) => h.replace(/<button class="parte" data-t="3"[^>]*>.*?<\/button>/s, "");
const semOndeFica = (h: string) => h.replace(/<div class="monde">.*?<\/ol><\/div>/s, "");

describe("telas iguais à versão 1", () => {
  it("tem gabarito de todos os blocos", () => {
    expect(Object.keys(g.blocos).length).toBe(TEMAS.slice(0, 3).reduce((s, t) => s + t.blocos.length, 0));
  });
  for (const [chave, esperado] of Object.entries(g.blocos)) {
    const [t, b] = chave.split("-").map(Number);
    it(`tema ${t}, bloco ${b}: ${TEMAS[t].blocos[b].nome}`, () => {
      expect(semTemaNovo(partesHTML(t))).toBe(esperado.partes);
      expect(chipsHTML(t, b)).toBe(esperado.chips);
      expect(semBotoesNovos(listaHTML(t, b, ""))).toBe(esperado.lista);
    });
  }
  for (const [chave, esperado] of Object.entries(g.buscas)) {
    const i = chave.indexOf(":");
    const t = +chave.slice(0, i), q = chave.slice(i + 1);
    it(`busca "${q}" no tema ${t}`, () => {
      expect(semBotoesNovos(listaHTML(t, 0, q))).toBe(esperado);
    });
  }
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
