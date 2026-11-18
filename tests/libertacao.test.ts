/* O tema Teologia da Libertação: fichas completas e telas. */
import { describe, expect, it } from "vitest";
import { TEMAS } from "../src/dados";
import { chipsHTML, listaHTML, partesHTML } from "../src/telas";

const i = TEMAS.findIndex((t) => t.nome === "Teologia da Libertação");
const tema = TEMAS[i];

describe("tema Teologia da Libertação", () => {
  it("é o quarto tema, depois de Valores católicos", () => {
    expect(i).toBe(3);
    expect(TEMAS[2].nome).toBe("Valores católicos");
    expect(partesHTML(0)).toContain('data-t="3"');
  });
  it("tem os três blocos", () => {
    expect(tema.blocos.map((b) => b.id)).toEqual(["libertacao", "desvios", "liturgia"]);
  });
  it("cada ficha tem resposta, Bíblia, Catecismo, Tradição e conselho", () => {
    tema.blocos.forEach((b) => b.itens.forEach((f) => {
      expect(f.resposta.length, f.pergunta).toBeGreaterThan(80);
      expect(f.biblia.length, f.pergunta).toBeGreaterThan(1);
      expect(f.catecismo.length, f.pergunta).toBeGreaterThan(0);
      expect(f.tradicao.length, f.pergunta).toBeGreaterThan(1);
      expect(f.conversa.length, f.pergunta).toBeGreaterThan(20);
    }));
  });
  it("trata dos documentos, do marxismo e da liturgia", () => {
    const tudo = JSON.stringify(tema.blocos);
    for (const t of ["Libertatis Nuntius", "Libertatis Conscientia", "marxista", "Puebla", "Redemptionis Sacramentum", "Sacrosanctum Concilium", "gregoriano"]) expect(tudo).toContain(t);
  });
  it("mostra o título próprio do quadro da Tradição", () => {
    const html = listaHTML(i, 0, "");
    expect(html).toContain("<h3>Na Tradição e no Magistério</h3>");
    expect(chipsHTML(i, 2)).toContain("Eucaristia, ritos e música");
  });
  it("a busca acha as fichas do tema", () => {
    expect(listaHTML(i, 0, "Betânia")).toContain("Santíssimo");
  });
});
