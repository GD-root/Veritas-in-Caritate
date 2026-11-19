/* Veritas in Caritate: navegação entre as telas, o papel de parede de cada tema e os toques. */
import "./estilos.css";
import { TEMAS } from "./dados";
import { janelaCatecismo, textoParaCopiar } from "./telas";
import { FUNDO_TEMA, blocoHTML, botaoSalvar, buscaHTML, chave, fichaHTML, inicioHTML, resultadosHTML, salvasHTML, simbolo, zerarLidas, temaHTML, temasHTML, type Lidas } from "./vistas";

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const app = $("app"), titulo = $("titulo"), subtitulo = $("subtitulo"), esq = $<HTMLAnchorElement>("esq");
const fundoEscuro = $<HTMLSourceElement>("fundo-escuro"), fundoClaro = $<HTMLImageElement>("fundo-claro"), medalhao = $<HTMLImageElement>("medalhao");
const modal = $("modal"), mcaixa = $("mcaixa"), mtit = $("mtit"), mcorpo = $("mcorpo"), mfechar = $("mfechar");
const ICONE_CHAVES = esq.innerHTML;
const ICONE_VOLTAR = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>';

/* Fichas lidas: guardadas só neste aparelho */
const CHAVE_LIDAS = "veritas-lidas";
function lerLidas(): Lidas {
  try { return new Set(JSON.parse(localStorage.getItem(CHAVE_LIDAS) || "[]") as string[]); } catch { return new Set(); }
}
const lidas = lerLidas();
function gravarLidas() {
  try { localStorage.setItem(CHAVE_LIDAS, JSON.stringify([...lidas])); } catch { /* sem espaço ou modo privado */ }
}
function marcarLida(k: string) {
  if (lidas.has(k)) return;
  lidas.add(k);
  gravarLidas();
}

/* Fichas salvas: também só neste aparelho */
const CHAVE_SALVAS = "veritas-salvas";
const salvas: Set<string> = (() => { try { return new Set(JSON.parse(localStorage.getItem(CHAVE_SALVAS) || "[]") as string[]); } catch { return new Set<string>(); } })();
function gravarSalvas() { try { localStorage.setItem(CHAVE_SALVAS, JSON.stringify([...salvas])); } catch { /* sem espaço ou modo privado */ } }

let buscaAtual = "";

function fundo(nome: string, simb = nome) {
  fundoEscuro.srcset = `fundos/${nome}-escuro.svg`;
  fundoClaro.src = `fundos/${nome}-claro.svg`;
  medalhao.src = `fundos/simbolos/${simb}.svg`;
}

function topo(t: string, sub: string, volta: string | null) {
  titulo.textContent = t;
  subtitulo.textContent = sub;
  esq.innerHTML = volta === null ? ICONE_CHAVES : ICONE_VOLTAR;
  esq.href = volta === null ? "#" : volta;
  esq.setAttribute("aria-label", volta === null ? "Início" : "Voltar");
}

function aba(nome: string) {
  document.querySelectorAll<HTMLAnchorElement>(".menu a").forEach((a) => {
    if (a.dataset.aba === nome) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
}

/** Lê o endereço (#t/0/1/2, #temas, #buscar?q=...) e desenha a tela. */
function render() {
  const h = decodeURIComponent(location.hash.replace(/^#/, ""));
  const m = h.match(/^t\/(\d+)(?:\/(\d+))?(?:\/(\d+))?$/);
  if (m && TEMAS[+m[1]] && (m[2] === undefined || TEMAS[+m[1]].blocos[+m[2]]) && (m[3] === undefined || TEMAS[+m[1]].blocos[+m[2]].itens[+m[3]])) {
    const t = +m[1], tm = TEMAS[t];
    fundo(FUNDO_TEMA[t] || "veritas", simbolo(t, m[2] === undefined ? undefined : +m[2]));
    aba("temas");
    if (m[3] !== undefined) {
      const b = +m[2], i = +m[3], bl = tm.blocos[b];
      marcarLida(chave(t, b, i));
      topo(bl.nome, `Ficha ${i + 1} de ${bl.itens.length}`, `#t/${t}/${b}`);
      app.innerHTML = fichaHTML(t, b, i, salvas.has(chave(t, b, i)));
    } else if (m[2] !== undefined) {
      const b = +m[2];
      topo(tm.blocos[b].nome, tm.nome, `#t/${t}`);
      app.innerHTML = blocoHTML(t, b, lidas);
    } else {
      topo(tm.nome, `${tm.blocos.length} ${tm.blocos.length === 1 ? "bloco" : "blocos"}`, "#temas");
      app.innerHTML = temaHTML(t, lidas);
    }
  } else if (h === "temas") {
    fundo("veritas"); aba("temas"); topo("Os temas", "A estante do Veritas", "#");
    app.innerHTML = temasHTML(lidas);
  } else if (h === "salvas") {
    fundo("veritas"); aba("salvas"); topo("Salvas", "Suas fichas guardadas", "#");
    app.innerHTML = salvasHTML(salvas, lidas);
  } else if (h.startsWith("buscar")) {
    buscaAtual = new URLSearchParams(h.split("?")[1] || "").get("q") ?? buscaAtual;
    fundo("veritas"); aba("buscar"); topo("Buscar", "Em todos os temas", "#");
    app.innerHTML = buscaHTML(buscaAtual, lidas);
  } else {
    fundo("veritas"); aba("inicio"); topo("Veritas in Caritate", "A verdade na caridade", null);
    app.innerHTML = inicioHTML(lidas);
  }
}

window.addEventListener("hashchange", () => { render(); window.scrollTo(0, 0); });

/* Busca: no início leva para a tela de busca; na tela de busca a lista muda enquanto se digita */
app.addEventListener("submit", (e) => {
  const f = e.target as HTMLFormElement;
  e.preventDefault();
  const q = (f.querySelector("input") as HTMLInputElement).value;
  if (f.hasAttribute("data-ir-busca")) location.hash = "buscar?q=" + encodeURIComponent(q);
  else (f.querySelector("input") as HTMLInputElement).blur();
});
app.addEventListener("input", (e) => {
  const inp = e.target as HTMLInputElement;
  if (inp.id !== "q") return;
  buscaAtual = inp.value;
  $("resultados").innerHTML = resultadosHTML(buscaAtual, lidas);
});

/* Botão redondo de zerar as lidas (do bloco, do tema ou de tudo), com confirmação */
app.addEventListener("click", (e) => {
  const bt = (e.target as Element).closest<HTMLElement>("[data-zerar]");
  if (!bt) return;
  const alvo = bt.dataset.zerar!;
  const onde = alvo === "tudo" ? "de todos os temas" : alvo.includes("/") ? "deste bloco" : "deste tema";
  if (!confirm(`Zerar as fichas lidas ${onde}? As fichas salvas não mudam.`)) return;
  zerarLidas(lidas, alvo);
  gravarLidas();
  const y = window.scrollY;
  render();
  window.scrollTo(0, y);
});

/* Salvar ou tirar a ficha aberta das salvas */
app.addEventListener("click", (e) => {
  const bt = (e.target as Element).closest<HTMLElement>("[data-salvar]");
  const m = location.hash.match(/^#t\/(\d+)\/(\d+)\/(\d+)$/);
  if (!bt || !m) return;
  const k = chave(+m[1], +m[2], +m[3]);
  if (salvas.has(k)) salvas.delete(k); else salvas.add(k);
  gravarSalvas();
  const on = salvas.has(k);
  bt.innerHTML = botaoSalvar(on);
  bt.classList.toggle("salva", on);
  bt.setAttribute("aria-pressed", String(on));
});

/* Copiar referências da ficha aberta */
app.addEventListener("click", (e) => {
  const c = (e.target as Element).closest<HTMLElement>("[data-copiar]");
  if (!c) return;
  const m = location.hash.match(/^#t\/(\d+)\/(\d+)\/(\d+)$/);
  if (!m) return;
  const d = TEMAS[+m[1]].blocos[+m[2]].itens[+m[3]];
  const rotulo = c.innerHTML;
  const fim = (txt: string) => { c.textContent = txt; setTimeout(() => (c.innerHTML = rotulo), 1800); };
  try { navigator.clipboard.writeText(textoParaCopiar(d)).then(() => fim("Copiado"), () => fim("Não foi possível copiar")); } catch { fim("Não foi possível copiar"); }
});

/* Janela do Catecismo */
let voltar: HTMLElement | null = null;
const CORES = ["tema-mariana", "tema-liturgica", "tema-branca", "tema-roxa", "tema-vermelha"];
function fechar() { modal.hidden = true; voltar?.focus(); }
app.addEventListener("click", (e) => {
  const b = (e.target as Element).closest<HTMLElement>(".cicbtn");
  if (!b) return;
  const obj = app.querySelector(".objecao");
  const j = janelaCatecismo(b.dataset.ref!, CORES.find((t) => obj?.classList.contains(t)) || "");
  if (!j) return;
  mcaixa.className = j.cls; mtit.textContent = j.tit; mcorpo.innerHTML = j.corpo;
  voltar = b; modal.hidden = false; mfechar.focus();
});
modal.addEventListener("click", (e) => { if (e.target === modal || (e.target as Element).closest("#mfechar")) fechar(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !modal.hidden) fechar(); });

render();

/* Funcionamento sem internet */
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch(() => {});
    /* apaga o cache da versão anterior (veritas-v1...), que guardava o index.html inteiro */
    if ("caches" in window) caches.keys().then((ks) => ks.filter((k) => /^veritas-v\d+$/.test(k)).forEach((k) => caches.delete(k))).catch(() => {});
  });
}
