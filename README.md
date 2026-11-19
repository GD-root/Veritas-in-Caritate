# Veritas in Caritate

Apologética católica para o celular: para cada objeção, a resposta curta, as passagens da Bíblia, os números do
Catecismo e a voz dos primeiros cristãos. Abre sem internet depois da primeira visita.

## Como está organizado

```
index.html                    a página (só a estrutura)
public/                       ícones, manifest e fundos/ (o interior da igreja com o vitral de cada tema)
src/
  main.ts                     navegação (#t/tema/bloco/ficha, #temas, #buscar), fundo de cada tema e toques
  vistas.ts                   o HTML de cada tela: início, temas, tema, bloco, ficha e busca (funções testáveis)
  telas.ts                    peças comuns: referências ao Catecismo, texto para copiar e a janela do Catecismo
  dados.ts                    junta os temas com as fichas
  tipos.ts                    o formato de cada arquivo de dados
  dados/
    temas.json                  temas e blocos (nome, cor, arquivo das fichas)
    blocos/*.json               as fichas de cada bloco: maria, igreja, escritura, sacramentos, cristo,
                                imagens, solas, teologais, cardeais, vida,
                                libertacao, desvios, liturgia (Teologia da Libertação)
    catecismo-explicacoes.json  explicação, com palavras próprias, dos parágrafos citados
    catecismo-partes.json       trechos do Catecismo como divididos no site do Vaticano
    catecismo-estrutura.json    ← gerado do Drive: Partes, Secções, Capítulos, Artigos e subtítulos
tests/                        testes automáticos
ferramentas/                  o script em Python que lê o Catecismo do Drive (veja ferramentas/LEIAME.md)
                              e fundos/gerar_fundos.py, que desenha os papéis de parede de public/fundos
                              e os símbolos dos vitrais de cada tema e bloco (fundos/simbolos.py)
```

### Acrescentar ou corrigir uma ficha

Edite o arquivo do bloco em `src/dados/blocos/`. Cada ficha tem:

| Campo | O que é |
|---|---|
| `pergunta` | a objeção (aparece entre aspas) ou, com `"simples": true`, o assunto |
| `resposta` | a resposta curta |
| `biblia`, `catecismo`, `tradicao` | listas de `{ "ref": "...", "texto": "..." }`; no Catecismo, use `"CIC 966"` ou `"CIC 75-79"` |
| `conversa` | o conselho de como conversar (guardado, mas não aparece no app por enquanto) |
| `tituloResposta`, `rotuloConversa`, `rotuloTradicao` | opcionais, para trocar os títulos padrão |

Para um bloco novo: crie o arquivo em `src/dados/blocos/`, importe em `src/dados.ts` e ponha em `src/dados/temas.json`.

## Comandos

Precisa do [Node.js](https://nodejs.org) 22 ou mais novo.

```
npm install        uma vez
npm run dev        abre o app para testar (atualiza sozinho)
npm test           roda os testes
npm run build      monta a versão final em dist/
```

## Testes

- `tests/telas.test.ts` confere que cada bloco, as buscas e as 224 janelas do Catecismo produzem o mesmo HTML da
  versão 1 (o `index.html` antigo, de arquivo único), descontadas só as mudanças feitas de propósito.
- `tests/catecismo.test.ts` confere a estrutura gerada do Drive e que toda referência das fichas abre a janela.
- `ferramentas/test_gerar_dados.py` testa o script em Python.

## Publicação

A cada envio para a `main`, o fluxo `.github/workflows/publicar.yml` roda os testes, monta e publica no GitHub Pages.
**Uma vez só:** *Settings › Pages › Build and deployment › Source* = **GitHub Actions**.
Não é mais preciso trocar o número de versão no `sw.js`: ele é gerado a cada publicação.

## Instalar no celular

- **iPhone:** Safari › Compartilhar › "Adicionar à Tela de Início".
- **Android:** Chrome › menu (três pontos) › "Instalar app".

As passagens bíblicas estão resumidas; o texto completo do Catecismo está no site do Vaticano (os links precisam de internet).
