/* Estrutura do Catecismo gerada do Drive e a janela "onde fica". */
import { describe, expect, it } from "vitest";
import { ESTRUTURA, TEMAS } from "../src/dados";
import { janelaCatecismo, numeroCIC, ondeFica } from "../src/telas";

describe("estrutura do Catecismo", () => {
  const partes = ESTRUTURA.divisoes.filter((d) => d.nivel === "parte");
  it("Prólogo e as quatro partes, nos intervalos certos", () => {
    expect(partes.map((p) => [p.de, p.ate])).toEqual([[1, 25], [26, 1065], [1066, 1690], [1691, 2557], [2558, 2865]]);
  });
  it("cada divisão tem início antes do fim e dentro do Catecismo", () => {
    ESTRUTURA.divisoes.forEach((d) => {
      expect(d.de).toBeGreaterThanOrEqual(1);
      expect(d.ate).toBeLessThanOrEqual(2865);
      expect(d.de).toBeLessThanOrEqual(d.ate);
    });
  });
  it("acha o artigo do Credo sobre a Igreja", () => {
    const art = ondeFica(882).find((d) => d.nivel === "artigo")!;
    expect(art.titulo).toMatch(/Igreja/);
    expect([art.de, art.ate]).toEqual([748, 975]);
  });
});

describe("referências das fichas", () => {
  const refs = TEMAS.flatMap((t) => t.blocos.flatMap((b) => b.itens.flatMap((f) => f.catecismo.map((r) => r.ref))));
  it("todas são números válidos do Catecismo", () => {
    refs.forEach((r) => expect(numeroCIC(r), r).not.toBeNull());
  });
  it("toda referência abre a janela, com o lugar no Catecismo", () => {
    refs.forEach((r) => {
      const j = janelaCatecismo(r, "");
      expect(j, r).not.toBeNull();
      expect(j!.corpo).toContain("Onde fica no Catecismo");
    });
  });
});
