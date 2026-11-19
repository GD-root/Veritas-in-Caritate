/* As telas novas: nenhuma ficha perde conteúdo, a navegação aponta para lugares que existem e as lidas aparecem. */
import { describe, expect, it } from "vitest";
import { TEMAS } from "../src/dados";
import { esc } from "../src/util";
import { acharBloco, blocoHTML, buscaHTML, buscar, chave, fichaHTML, inicioHTML, temaHTML, temasHTML } from "../src/vistas";

const nada = new Set<string>();

describe("ficha", () => {
  it("mostra a resposta, todas as referências e o conselho de cada ficha", () => {
    TEMAS.forEach((tm, t) => tm.blocos.forEach((bl, b) => bl.itens.forEach((d, i) => {
      const h = fichaHTML(t, b, i);
      for (const txt of [d.resposta, d.conversa, ...[...d.biblia, ...d.catecismo, ...d.tradicao].flatMap((r) => [r.ref, r.texto])]) expect(h, d.pergunta).toContain(esc(txt));
    })));
  });
  it("anterior e próxima dentro do bloco", () => {
    const h = fichaHTML(0, 0, 0);
    expect(h).not.toContain("Anterior");
    expect(h).toContain('href="#t/0/0/1"');
    expect(fichaHTML(0, 0, TEMAS[0].blocos[0].itens.length - 1)).toContain("Voltar ao bloco");
  });
  it("traz o botão de mandar no WhatsApp", () => {
    expect(fichaHTML(0, 0, 0)).toContain("https://wa.me/?text=");
  });
});

describe("início e temas", () => {
  it("os links do início levam a temas, blocos e fichas que existem", () => {
    const h = inicioHTML(nada);
    const links = [...h.matchAll(/href="#t\/(\d+)(?:\/(\d+))?(?:\/(\d+))?"/g)];
    expect(links.length).toBeGreaterThan(8);
    for (const [, t, b, i] of links) {
      expect(TEMAS[+t]).toBeTruthy();
      if (b !== undefined) expect(TEMAS[+t].blocos[+b]).toBeTruthy();
      if (i !== undefined) expect(TEMAS[+t].blocos[+b].itens[+i]).toBeTruthy();
    }
    expect(h).toContain("O que perguntaram a você hoje?");
    expect(h).toContain("Seguindo a verdade na caridade");
  });
  it("todos os temas e blocos aparecem", () => {
    const h = temasHTML(nada);
    TEMAS.forEach((t, k) => {
      expect(h).toContain(esc(t.nome));
      const ht = temaHTML(k, nada);
      t.blocos.forEach((b) => expect(ht).toContain(esc(b.nome)));
    });
  });
  it("conta as fichas lidas", () => {
    const l = new Set([chave(0, 0, 0), chave(0, 0, 1)]);
    expect(temaHTML(0, l)).toContain("2 de 6 lidas");
    expect(blocoHTML(0, 0, l)).toContain('class="lin lida"');
  });
  it("acha os blocos dos atalhos", () => {
    for (const id of ["maria", "igreja", "imagens", "sacramentos", "solas"]) expect(acharBloco(id), id).not.toBeNull();
  });
});

describe("busca em todos os temas", () => {
  it("acha por palavra sem acento, passagem e número do Catecismo", () => {
    expect(buscar("virgem").length).toBeGreaterThan(0);
    expect(buscar("purgatorio").length).toBeGreaterThan(0);
    expect(buscar("Lc 1").length).toBeGreaterThan(0);
    expect(buscar("CIC 966").length).toBeGreaterThan(0);
    expect(buscar("xyzxyz")).toEqual([]);
  });
  it("mostra a contagem e o aviso quando não acha", () => {
    expect(buscaHTML("virgem", nada)).toMatch(/fichas? encontradas?/);
    expect(buscaHTML("xyzxyz", nada)).toContain("Nenhuma ficha contém esse termo");
  });
});
