#!/usr/bin/env python3
"""
Lê o Catecismo da Igreja Católica guardado no Google Drive e gera os dados do Veritas in Caritate.

Entrada (pasta "Catecismo" do Drive, ou uma cópia local dela):
  Catecismo/catecismo-1.txt ... catecismo-N.txt   o texto do Catecismo, em partes, em ordem

Saída:
  src/dados/catecismo-estrutura.json   Partes, Secções, Capítulos, Artigos, Parágrafos e subtítulos, com o
                                       intervalo de números de cada um (só os títulos, sem o texto)
  ferramentas/relatorio-catecismo.md   conferência das referências ao Catecismo usadas nas fichas

O texto dos parágrafos é lido só na memória, para a conferência: não é gravado em lugar nenhum.

Uso:
  python3 ferramentas/gerar_dados.py --pasta ferramentas/entrada      (cópia local)
  python3 ferramentas/gerar_dados.py --drive                         (baixa do Drive)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "src" / "dados"
ULTIMO = 2865  # último número do Catecismo

# --------------------------------------------------------------------------------------------
# Leitura
# --------------------------------------------------------------------------------------------


def numero_no_nome(p: Path) -> int:
    m = re.search(r"(\d+)\D*$", p.stem)
    return int(m.group(1)) if m else 0


def ler_pasta(pasta: Path) -> str:
    sub = next((p for p in pasta.iterdir() if p.is_dir() and p.name.lower() == "catecismo"), None)
    if sub is None:
        sys.exit(f"Não encontrei a pasta 'Catecismo' dentro de {pasta}")
    partes = sorted((p for p in sub.glob("*.txt") if re.fullmatch(r"catecismo-\d+", p.stem, re.I)), key=numero_no_nome)
    if not partes:
        sys.exit(f"Nenhum arquivo catecismo-N.txt em {sub}")
    return "\n".join(p.read_text(encoding="utf-8") for p in partes)


# --------------------------------------------------------------------------------------------
# Estrutura
# --------------------------------------------------------------------------------------------

NIVEIS = ["parte", "secao", "capitulo", "artigo", "paragrafo", "subtitulo", "assunto"]
RE_PARAGRAFO = re.compile(r"^(\d{1,4})\.\s*(\S.*)$")
RE_TITULOS = [
    ("parte", re.compile(r"^(PRÓLOGO|(PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA) PARTE\b.*)$")),
    ("secao", re.compile(r"^(PRIMEIRA|SEGUNDA) SEC[ÇC]ÃO\b.*$")),
    ("capitulo", re.compile(r"^CAP[IÍ]TULO\b.*$")),
    ("artigo", re.compile(r"^ARTIGO\s*\d+.*$")),
    ("paragrafo", re.compile(r"^PARÁGRAFO\s*\d+.*$")),
    ("subtitulo", re.compile(r"^[IVX]+\.\s+\S.*$")),
]


def maiusculas(s: str) -> bool:
    letras = [c for c in s if c.isalpha()]
    return len(letras) >= 4 and sum(c.isupper() for c in letras) / len(letras) > 0.85


def nivel_do_titulo(s: str) -> str | None:
    for nivel, rx in RE_TITULOS:
        if rx.match(s):
            return nivel
    # assuntos: linhas curtas em maiúsculas, sem números (números indicam tabela ou nota)
    if maiusculas(s) and len(s) < 90 and not re.search(r"\d", s):
        return "assunto"
    return None


MAIUSCULAS = {"deus": "Deus", "cristo": "Cristo", "jesus": "Jesus", "espírito": "Espírito", "santo": "Santo",
              "igreja": "Igreja", "pai": "Pai", "filho": "Filho", "maria": "Maria", "senhor": "Senhor", "virgem": "Virgem",
              "credo": "Credo", "eucaristia": "Eucaristia", "trindade": "Trindade", "verbo": "Verbo", "ámen": "Ámen",
              "amen": "Amen", "israel": "Israel", "noé": "Noé", "abraão": "Abraão", "pedro": "Pedro", "adão": "Adão",
              "pôncio": "Pôncio", "pilatos": "Pilatos", "decálogo": "Decálogo", "católica": "Católica"}


def bonito(s: str) -> str:
    """'ARTIGO 9: «CREIO NA SANTA IGREJA CATÓLICA»' -> 'Artigo 9: «Creio na santa Igreja Católica»'"""
    if not maiusculas(s):
        return s
    palavras = []
    for w in s.lower().split():
        nu = re.sub(r"[^\wÀ-ú]", "", w)
        if nu in MAIUSCULAS:
            w = w.replace(nu, MAIUSCULAS[nu])
        elif re.fullmatch(r"[ivx]+", nu) and nu not in ("vi",):
            w = w.replace(nu, nu.upper())
        palavras.append(w)
    r = " ".join(palavras)
    r = re.sub(r"^(\W*)(\w)", lambda m: m.group(1) + m.group(2).upper(), r)
    return re.sub(r":\s*(«?)(\w)", lambda m: ": " + m.group(1) + m.group(2).upper(), r)


@dataclass
class Titulo:
    nivel: str
    titulo: str
    linha: int
    primeiro: int | None = None  # primeiro número de parágrafo depois do título


def ler_catecismo(texto: str) -> tuple[list[Titulo], dict[int, str]]:
    """Devolve os títulos (com o primeiro número de cada um) e o texto de cada parágrafo (só na memória)."""
    linhas = texto.splitlines()
    inicio = next((i for i, l in enumerate(linhas) if re.match(r"^\s*1\.\s+Deus", l)), None)
    if inicio is None:
        sys.exit("Catecismo: não encontrei o parágrafo 1.")
    # volta até o título PRÓLOGO
    inicio = next((i for i in range(inicio, max(0, inicio - 40), -1) if linhas[i].strip() == "PRÓLOGO"), inicio)

    titulos: list[Titulo] = []
    paragrafos: dict[int, list[str]] = {}
    esperado, atual = 1, None
    em_notas = False
    ultimo_foi_titulo = False

    for i in range(inicio, len(linhas)):
        s = linhas[i].strip()
        if not s:
            continue
        if s == "Notas":
            em_notas, atual = True, None
            continue
        m = RE_PARAGRAFO.match(s)
        if m:
            n = int(m.group(1))
            # aceita o número esperado, ou até 3 adiante quando a leitura do texto perdeu algum
            if esperado <= n <= esperado + 3 and not (em_notas and n != esperado):
                em_notas = False
                for t in titulos:
                    if t.primeiro is None:
                        t.primeiro = n
                paragrafos[n] = [m.group(2)]
                atual, esperado = n, n + 1
                ultimo_foi_titulo = False
                continue
            if em_notas:
                continue
        nivel = nivel_do_titulo(s)
        if nivel and (nivel != "assunto" or not em_notas):
            if em_notas and nivel == "assunto":
                continue
            # título que continua na linha de baixo (ARTIGO 1: «CREIO EM DEUS PAI ... / E DA TERRA»):
            # as aspas ficaram abertas, ou a linha começa com "E", "DE", "DO"...
            if ultimo_foi_titulo and nivel == "assunto" and titulos and titulos[-1].primeiro is None:
                ant = titulos[-1].titulo
                if ant.count("«") > ant.count("»") or re.match(r"^(E|DE|DO|DA|DOS|DAS|EM|NA|NO|AO|À)\s", s):
                    titulos[-1].titulo += " " + s
                    continue
            # o Prólogo descreve as quatro partes: antes do § 26 só vale o título "PRÓLOGO" e os subtítulos
            if esperado < 26 and nivel in ("parte", "secao", "capitulo", "artigo", "paragrafo") and s != "PRÓLOGO":
                continue
            em_notas = False
            titulos.append(Titulo(nivel, s, i))
            atual, ultimo_foi_titulo = None, True
            continue
        ultimo_foi_titulo = False
        if em_notas:
            continue
        if atual is not None:
            paragrafos[atual].append(s)

    return titulos, {n: " ".join(v) for n, v in paragrafos.items()}


PARTES_DO_CIC = ["PRIMEIRA PARTE", "SEGUNDA PARTE", "TERCEIRA PARTE", "QUARTA PARTE"]


def montar_estrutura(titulos: list[Titulo], ultimo_lido: int, indice: list[str]) -> list[dict]:
    validos = [t for t in titulos if t.primeiro is not None]
    divisoes = []
    # Partes que estão no índice mas cujo texto não veio no arquivo (o arquivo acaba antes do § 2865)
    achadas = {next((p for p in PARTES_DO_CIC if t.titulo.startswith(p)), "") for t in validos if t.nivel == "parte"}
    faltando = [l for l in indice if any(l.startswith(p) for p in PARTES_DO_CIC) and not any(l.startswith(a) for a in achadas if a)]
    fim_do_texto = ULTIMO + 1 if not faltando else ultimo_lido + 1
    for k, t in enumerate(validos):
        nv = NIVEIS.index(t.nivel)
        # vai até antes do próximo título do mesmo nível ou acima
        prox = next((u.primeiro for u in validos[k + 1:] if NIVEIS.index(u.nivel) <= nv and u.primeiro > t.primeiro), fim_do_texto)
        titulo = t.titulo if t.nivel == "subtitulo" else bonito(t.titulo)
        divisoes.append({"nivel": t.nivel, "titulo": titulo, "de": t.primeiro, "ate": prox - 1})
    for l in faltando:
        divisoes.append({"nivel": "parte", "titulo": bonito(l), "de": ultimo_lido + 1, "ate": ULTIMO, "semTexto": True})
    # dois títulos seguidos sem parágrafo entre eles começam no mesmo número; o de nível menor vem depois
    divisoes.sort(key=lambda d: (d["de"], NIVEIS.index(d["nivel"])))
    return divisoes


def indice_do_arquivo(texto: str) -> list[str]:
    """As linhas do índice no começo do arquivo (antes do texto)."""
    linhas = [l.strip() for l in texto.splitlines()[:1200]]
    i = next((k for k, l in enumerate(linhas) if l == "ÍNDICE"), None)
    return [l for l in linhas[i + 1:] if l] if i is not None else []


# --------------------------------------------------------------------------------------------
# Conferência das referências usadas nas fichas
# --------------------------------------------------------------------------------------------

PALAVRAS_VAZIAS = set("""a o as os um uma uns umas de da do das dos em na no nas nos por pela pelo pelas pelos para com sem
que se e ou nao não mais muito como quando onde qual quais quem cujo seu sua seus suas ele ela eles elas isso este esta
esse essa aquele aquela tambem também ja já so só ser sao são foi era tem têm ter pode podem deve devem todo toda todos
todas cada outro outra outros outras mesmo mesma nos nós vos vós lhe lhes sobre entre ate até ainda assim porque pois
sempre nunca tudo nada aqui ali isto aquilo dele dela deles delas num numa ao aos à às pelo hoje""".split())


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def raizes(texto: str) -> set[str]:
    """Palavras com conteúdo, cortadas nas 5 primeiras letras (graça/graças, salvar/salvação)."""
    ws = re.findall(r"[a-zà-ú]+", texto.lower())
    return {sem_acento(w)[:5] for w in ws if len(w) >= 4 and w not in PALAVRAS_VAZIAS}


def numeros_da_ref(ref: str) -> list[int] | None:
    """'CIC 75-79' -> [75..79]; 'CIC 484, 487' -> [484, 487]. None se não der para ler."""
    m = re.fullmatch(r"CIC\s+(.+)", ref.strip())
    if not m:
        return None
    nums: list[int] = []
    for parte in re.split(r"\s*[,;]\s*|\s+e\s+", m.group(1)):
        r = re.fullmatch(r"(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?", parte)
        if not r:
            return None
        a, b = int(r.group(1)), int(r.group(2) or r.group(1))
        if b < a:
            return None
        nums += list(range(a, b + 1))
    return nums


def onde(divs: list[dict], n: int) -> str:
    caminho = [d for d in divs if d["de"] <= n <= d["ate"] and d["nivel"] not in ("subtitulo", "assunto")]
    return " › ".join(d["titulo"].split(":")[0] if d["nivel"] in ("parte", "secao", "capitulo") else d["titulo"] for d in caminho)


def conferir(divs: list[dict], paragrafos: dict[int, str], ultimo_lido: int, limite: float = 0.2) -> tuple[str, int]:
    temas = json.loads((DADOS / "temas.json").read_text(encoding="utf-8"))
    explic = json.loads((DADOS / "catecismo-explicacoes.json").read_text(encoding="utf-8"))
    partes = json.loads((DADOS / "catecismo-partes.json").read_text(encoding="utf-8"))["partes"]
    ilegiveis, fora, fracas, total = [], [], [], 0

    for t in temas:
        for b in t["blocos"]:
            fichas = json.loads((DADOS / "blocos" / f"{b['id']}.json").read_text(encoding="utf-8"))
            for k, f in enumerate(fichas, 1):
                for r in f["catecismo"]:
                    total += 1
                    nums = numeros_da_ref(r["ref"])
                    if nums is None:
                        ilegiveis.append(f"- {b['nome']}, ficha {k}: `{r['ref']}`")
                        continue
                    if any(n < 1 or n > ULTIMO for n in nums):
                        fora.append(f"- {b['nome']}, ficha {k}: `{r['ref']}` (o Catecismo vai de 1 a {ULTIMO})")
                        continue
                    texto_cic = " ".join(paragrafos[n] for n in nums if n in paragrafos)
                    if not texto_cic:
                        continue
                    alvo = raizes(r["texto"])
                    if len(alvo) < 3:
                        continue
                    nota = len(alvo & raizes(texto_cic)) / len(alvo)
                    if nota < limite:
                        fracas.append((nota, f"- **{r['ref']}** ({b['nome']}, ficha {k}: “{f['pergunta'][:70]}”)  \n"
                                             f"  No app: {r['texto']}  \n  Fica em: {onde(divs, nums[0])}"))

    det_fracas = []
    for ref, itens in explic.items():
        for it in itens:
            nums = numeros_da_ref("CIC " + it["n"])
            if not nums:
                continue
            texto_cic = " ".join(paragrafos[n] for n in nums if n in paragrafos)
            alvo = raizes(it["texto"])
            if texto_cic and len(alvo) >= 3:
                nota = len(alvo & raizes(texto_cic)) / len(alvo)
                if nota < limite:
                    det_fracas.append((nota, f"- **§ {it['n']}** (janela de {ref}): {it['texto']}  \n  Fica em: {onde(divs, nums[0])}"))

    inicios = {d["de"] for d in divs}
    partes_fora = [f"- {a}–{b}" for a, b in partes if a not in inicios and a <= ultimo_lido]

    linhas = [
        "# Conferência das referências ao Catecismo", "",
        f"Gerado em {date.today():%d/%m/%Y} por `ferramentas/gerar_dados.py`, comparando as {total} referências ao Catecismo",
        "das fichas com o texto do Catecismo guardado na pasta Catecismo do Drive.", "",
        "A conferência de assunto compara as palavras do resumo do app com as do parágrafo citado. Nota baixa não quer",
        "dizer erro: o resumo pode usar outras palavras. É uma lista para olhar com calma.", "",
    ]
    if ultimo_lido < ULTIMO:
        linhas += [f"> O arquivo do Drive termina no § {ultimo_lido}. As referências aos §§ {ultimo_lido + 1} a {ULTIMO} (Quarta Parte,",
                   "> a oração) não puderam ser conferidas.", ""]
    problemas = len(ilegiveis) + len(fora)
    linhas += ["## Referências que não dá para ler", ""] + (ilegiveis or ["Nenhuma."]) + [""]
    linhas += ["## Números fora do Catecismo", ""] + (fora or ["Nenhum."]) + [""]
    linhas += [f"## Resumos com poucas palavras em comum com o parágrafo citado ({len(fracas)})", ""]
    linhas += [x for _, x in sorted(fracas)] or ["Nenhum."]
    linhas += ["", f"## Explicações das janelas com poucas palavras em comum ({len(det_fracas)})", ""]
    linhas += [x for _, x in sorted(det_fracas)] or ["Nenhuma."]
    linhas += ["", "## Trechos do site do Vaticano que não começam num título", ""] + (partes_fora or ["Todos começam num título."]) + [""]
    linhas.insert(next(i for i, l in enumerate(linhas) if l.startswith("## ")), f"**{problemas} referências com erro; {len(fracas) + len(det_fracas)} para conferir o assunto.**\n")
    return "\n".join(linhas), problemas


# --------------------------------------------------------------------------------------------
# Principal
# --------------------------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    fonte = ap.add_mutually_exclusive_group(required=True)
    fonte.add_argument("--pasta", type=Path, help="pasta local com a subpasta Catecismo")
    fonte.add_argument("--drive", action="store_true", help="baixar a pasta Catecismo do Google Drive")
    ap.add_argument("--credenciais", type=Path, default=Path(__file__).parent / "credenciais.json")
    args = ap.parse_args()

    if args.drive:
        from drive import baixar_do_drive

        destino = Path(__file__).parent / "entrada"
        baixar_do_drive(args.credenciais, destino, ("Catecismo",))
        args.pasta = destino

    print("Lendo o Catecismo...")
    texto = ler_pasta(args.pasta)
    titulos, paragrafos = ler_catecismo(texto)
    ultimo_lido = max(paragrafos)
    faltam = [n for n in range(1, ultimo_lido + 1) if n not in paragrafos]
    print(f"  {len(paragrafos)} parágrafos lidos, do 1 ao {ultimo_lido}" + (f"; {len(faltam)} não encontrados (erro de leitura do PDF)" if faltam else ""))
    if ultimo_lido < ULTIMO:
        print(f"  Aviso: o arquivo termina no § {ultimo_lido}; o Catecismo vai até o § {ULTIMO}.")
    divs = montar_estrutura(titulos, ultimo_lido, indice_do_arquivo(texto))
    print(f"  {len(divs)} títulos ({', '.join(f'{sum(1 for d in divs if d['nivel'] == n)} {n}' for n in NIVEIS)})")

    saida = DADOS / "catecismo-estrutura.json"
    saida.write_text(json.dumps({
        "fonte": "Títulos e numeração do Catecismo da Igreja Católica (tradução portuguesa). Só os títulos, sem o texto.",
        "gerado": date.today().isoformat(),
        "divisoes": divs,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Gravado: {saida.relative_to(RAIZ)} ({saida.stat().st_size // 1024} KB)")

    relatorio, problemas = conferir(divs, paragrafos, ultimo_lido)
    rel = Path(__file__).parent / "relatorio-catecismo.md"
    rel.write_text(relatorio, encoding="utf-8")
    print(f"Gravado: {rel.relative_to(RAIZ)} ({problemas} referências com erro)")


if __name__ == "__main__":
    main()
