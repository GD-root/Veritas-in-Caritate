/* "Conhecer a Igreja": toda pergunta tem resposta, explicação, origem e fontes; as telas montam sem erro. */
import { describe, expect, it } from "vitest";
import { CATEGORIAS, ICONE_CAT, categoriaConhecerHTML, conhecerHTML, itemConhecerHTML, portaConhecerHTML } from "../src/conhecer";
import { inicioHTML, PRAESTO, resultadosHTML } from "../src/vistas";

describe("Conhecer a Igreja", () => {
  it("tem as 7 partes, cada uma com ícone e pelo menos 5 perguntas", () => {
    expect(CATEGORIAS.map((c) => c.id)).toEqual(["gestos", "altar", "vestes", "canto", "historia", "devocoes", "comunidades"]);
    CATEGORIAS.forEach((c) => { expect(ICONE_CAT[c.id], c.id).toBeTruthy(); expect(c.itens.length, c.id).toBeGreaterThanOrEqual(5); });
  });
  it("toda pergunta tem resposta curta, explicação, origem e fontes", () => {
    CATEGORIAS.forEach((c) => c.itens.forEach((it) => {
      expect(it.pergunta.endsWith("?"), it.pergunta).toBe(true);
      expect(it.resposta.length, it.pergunta).toBeGreaterThan(60);
      expect(it.entenda.length, it.pergunta).toBeGreaterThan(150);
      expect(it.origem.length, it.pergunta).toBeGreaterThan(80);
      expect(it.fontes.length, it.pergunta).toBeGreaterThan(0);
    }));
  });
  it("as comunidades incluem a Renovação, as novas comunidades, a Opus Dei e as tradicionais", () => {
    const p = CATEGORIAS.find((c) => c.id === "comunidades")!.itens.map((i) => i.pergunta).join(" | ");
    for (const nome of ["Renovação Carismática", "novas comunidades", "Opus Dei", "Canção Nova", "Shalom", "tradicionais"]) expect(p).toContain(nome);
  });
  it("as telas montam: entrada, cada parte e cada pergunta", () => {
    expect(conhecerHTML()).toContain('href="#igreja/6"');
    CATEGORIAS.forEach((c, k) => {
      expect(categoriaConhecerHTML(k)).toContain(c.nome);
      c.itens.forEach((_, i) => expect(itemConhecerHTML(k, i)).toContain("Em poucas palavras"));
    });
  });
  it("o botão da estante mostra o balão só quando pedido", () => {
    expect(portaConhecerHTML(true)).toContain("Toque aqui");
    expect(portaConhecerHTML(false)).not.toContain("Toque aqui");
  });
  it("a tela inicial tem o atalho para o Praesto Sum", () => {
    expect(inicioHTML(new Set())).toContain(PRAESTO);
  });
  it("a busca do alto encontra as perguntas", () => {
    expect(resultadosHTML("escapulário", new Set())).toContain('href="#igreja/5/1"');
    expect(resultadosHTML("Opus Dei", new Set())).toContain("Conhecer a Igreja");
  });
});
