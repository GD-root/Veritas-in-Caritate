/* Utilidades de texto. */

const ENTIDADES: Record<string, string> = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" };

export const esc = (s: string): string => s.replace(/[&<>"]/g, (c) => ENTIDADES[c]);

/** Minúsculas e sem acentos, para a busca. */
export const norm = (s: string): string => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

/** Data da Tradição por extenso: "c. 110" -> "Cerca de 110 D.C.", "325" -> "325 D.C.". */
export function quando(r: string): string {
  if (/a\.C\./.test(r)) return r.replace("a.C.", "A.C.");
  const m = r.match(/^c\. (\d+)$/);
  if (m) return "Cerca de " + m[1] + " D.C.";
  if (/^\d/.test(r) || /^Séc\./.test(r)) return r + " D.C.";
  return r;
}
