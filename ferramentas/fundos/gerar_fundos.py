"""Gera os papéis de parede do Veritas (interior de igreja com o vitral de cada tema), em public/fundos/.
Uso: python3 ferramentas/fundos/gerar_fundos.py"""
import pathlib, sys
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from igreja import cena  # noqa

SAIDA = AQUI.parent.parent / "public" / "fundos"
TEMAS = ["veritas", "defesa", "reforma", "valores", "libertacao"]

def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    for t in TEMAS:
        for modo in ("escuro", "claro"):
            svg = cena(modo, t, .6, uid=f"{t[:3]}{modo[0]}")
            (SAIDA / f"{t}-{modo}.svg").write_text(svg, encoding="utf-8")
    print("ok:", len(TEMAS) * 2, "fundos em", SAIDA)

if __name__ == "__main__":
    main()
