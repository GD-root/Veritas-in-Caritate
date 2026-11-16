"""Testes do gerar_dados.py com um Catecismo de mentira, pequeno. Rode:  python3 -m unittest discover -s ferramentas"""
import unittest

import gerar_dados as g

# O Prólogo vai do § 1 ao 25; os §§ 3 a 24 são preenchidos abaixo para a numeração seguir em ordem.
TEXTO = """ÍNDICE
PRÓLOGO
PRIMEIRA PARTE: A PROFISSÃO DA FÉ
QUARTA PARTE: A ORAÇÃO NA VIDA DA FÉ

PRÓLOGO

I. A vida do homem – conhecer e amar a Deus
1. Deus, infinitamente perfeito, criou o homem.
2. Para que este apelo ressoe, Cristo enviou os apóstolos.
{meio}IV. Estrutura deste catecismo
PRIMEIRA PARTE: A PROFISSÃO DA FÉ
25. Acima de tudo, a caridade.
Notas
1. Cf. Jo 17, 3.
2. CSEL 25,197.
PRIMEIRA PARTE: A PROFISSÃO DA FÉ
PRIMEIRA SECÇÃO: «EU CREIO» – «NÓS CREMOS»
26. Quando professamos a nossa fé, começamos por dizer: «Creio».
CAPÍTULO PRIMEIRO: O HOMEM É «CAPAZ» DE DEUS
27. O desejo de Deus está inscrito no coração do homem
continua na linha de baixo.
ARTIGO 1: «CREIO EM DEUS PAI TODO-PODEROSO CRIADOR DO CÉU
E DA TERRA»
A ALIANÇA COM NOÉ
28. Deus fez aliança com Noé.
""".replace("{meio}", "".join(f"{n}. Parágrafo {n} do Prólogo.\n" for n in range(3, 25)))


class TestEstrutura(unittest.TestCase):
    def setUp(self):
        self.titulos, self.pars = g.ler_catecismo(TEXTO)

    def test_paragrafos_e_notas(self):
        self.assertEqual(sorted(self.pars), list(range(1, 29)))
        self.assertIn("continua na linha de baixo", self.pars[27])
        self.assertNotIn("Jo 17", self.pars[25])  # as notas não entram no texto

    def test_prologo_nao_conta_as_partes_que_descreve(self):
        partes = [t for t in self.titulos if t.nivel == "parte"]
        self.assertEqual([(t.titulo, t.primeiro) for t in partes], [("PRÓLOGO", 1), ("PRIMEIRA PARTE: A PROFISSÃO DA FÉ", 26)])

    def test_titulo_quebrado_em_duas_linhas(self):
        art = next(t for t in self.titulos if t.nivel == "artigo")
        self.assertEqual(art.titulo, "ARTIGO 1: «CREIO EM DEUS PAI TODO-PODEROSO CRIADOR DO CÉU E DA TERRA»")
        assunto = next(t for t in self.titulos if t.nivel == "assunto")
        self.assertEqual(assunto.titulo, "A ALIANÇA COM NOÉ")

    def test_intervalos_e_parte_sem_texto(self):
        divs = g.montar_estrutura(self.titulos, 28, g.indice_do_arquivo(TEXTO))
        por_nome = {d["titulo"]: (d["de"], d["ate"]) for d in divs}
        self.assertEqual(por_nome["Prólogo"], (1, 25))
        self.assertEqual(por_nome["Primeira parte: A profissão da fé"], (26, 28))
        self.assertEqual(por_nome["Capítulo primeiro: O homem é «capaz» de Deus"], (27, 28))
        quarta = next(d for d in divs if d["titulo"].startswith("Quarta"))
        self.assertTrue(quarta["semTexto"])
        self.assertEqual((quarta["de"], quarta["ate"]), (29, 2865))


class TestReferencias(unittest.TestCase):
    def test_numeros_da_ref(self):
        self.assertEqual(g.numeros_da_ref("CIC 75-79"), [75, 76, 77, 78, 79])
        self.assertEqual(g.numeros_da_ref("CIC 484, 487"), [484, 487])
        self.assertEqual(g.numeros_da_ref("CIC 966"), [966])
        self.assertIsNone(g.numeros_da_ref("Catecismo 966"))
        self.assertIsNone(g.numeros_da_ref("CIC 80-75"))

    def test_bonito(self):
        self.assertEqual(g.bonito("ARTIGO 9: «CREIO NA SANTA IGREJA CATÓLICA»"), "Artigo 9: «Creio na santa Igreja Católica»")
        self.assertEqual(g.bonito("CAPÍTULO SEGUNDO: DEUS AO ENCONTRO DO HOMEM"), "Capítulo segundo: Deus ao encontro do homem")


if __name__ == "__main__":
    unittest.main()
