# Ferramentas: o Catecismo do Drive para o app

O script `gerar_dados.py` lê a pasta **Catecismo** do seu Google Drive e gera:

| Arquivo | O que tem |
|---|---|
| `src/dados/catecismo-estrutura.json` | Partes, Secções, Capítulos, Artigos, Parágrafos e subtítulos do Catecismo, com o intervalo de números de cada um. Só os títulos. É o que o app usa para mostrar "Onde fica no Catecismo" |
| `ferramentas/relatorio-catecismo.md` | Conferência das referências ao Catecismo usadas nas fichas: números que não existem e resumos que não parecem bater com o parágrafo citado |

**O texto do Catecismo não vai para o app.** Ele é lido só na memória, para a conferência. O app continua explicando
com palavras próprias e mandando para o texto oficial no site do Vaticano.

> O arquivo atual do Drive é uma cópia de e-book que termina no § 2557: a Quarta Parte (a oração, §§ 2558–2865)
> não está nele. O script avisa isso, e o app mostra só "Quarta parte" para esses números. Se você puser no Drive
> um texto que vá até o § 2865, basta rodar o script de novo.

## O que precisa estar no Drive

```
Catecismo/
  catecismo-1.txt ... catecismo-N.txt    o Catecismo em partes, em ordem
```

## Rodar com uma cópia local

Baixe a pasta para `ferramentas/entrada/Catecismo/` (fica fora do GitHub) e rode:

```
python3 ferramentas/gerar_dados.py --pasta ferramentas/entrada
npm test
```

Só usa a biblioteca padrão do Python 3.10 ou mais novo.

## Rodar direto do Drive

```
pip install -r ferramentas/requirements.txt
python3 ferramentas/gerar_dados.py --drive
```

O acesso ao Drive é igual ao do Praesto Sum (só leitura): um cliente OAuth "App para computador" salvo como
`ferramentas/credenciais.json`, ou uma conta de serviço com a pasta **Catecismo** compartilhada com ela. Para o GitHub
atualizar sozinho, guarde o JSON da conta de serviço no segredo `GOOGLE_CREDENCIAIS` e rode
*Actions › Atualizar dados do Drive*. Os dados novos vão para a branch `dados-do-drive`, já testados.

## Testes

```
python3 -m unittest discover -s ferramentas
```
