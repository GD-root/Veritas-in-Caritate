/* Lê o gabarito gravado a partir da versão 1 (o index.html único, antes da migração para TypeScript). */
import { readFileSync } from "node:fs";
import { gunzipSync } from "node:zlib";
import { fileURLToPath } from "node:url";

export function lerGabarito<T>(nome: string): T {
  const arq = fileURLToPath(new URL("./gabarito/" + nome + ".json.gz", import.meta.url));
  return JSON.parse(gunzipSync(readFileSync(arq)).toString("utf8")) as T;
}
