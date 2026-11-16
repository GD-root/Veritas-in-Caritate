/* Veritas in Caritate: liga as telas à página e cuida dos toques. */
import "./estilos.css";
import { TEMAS } from "./dados";
import { chipsHTML, janelaCatecismo, listaHTML, partesHTML, textoParaCopiar } from "./telas";

let tema = 0, ativo = 0;

const lista = document.getElementById("lista")!;
const nav = document.getElementById("blocos")!;
const pnav = document.getElementById("partes")!;
const busca = document.getElementById("busca") as HTMLInputElement;
const modal = document.getElementById("modal")!;
const mcaixa = document.getElementById("mcaixa")!;
const mtit = document.getElementById("mtit")!;
const mcorpo = document.getElementById("mcorpo")!;
const mfechar = document.getElementById("mfechar")!;

const temas = () => { pnav.innerHTML = partesHTML(tema); };
const chips = () => { nav.innerHTML = chipsHTML(tema, ativo); };
const render = () => { lista.innerHTML = listaHTML(tema, ativo, busca.value); };

pnav.addEventListener("click", (e) => {
  const c = (e.target as Element).closest<HTMLElement>(".parte");
  if (!c) return;
  tema = +c.dataset.t!; ativo = 0; busca.value = "";
  temas(); chips(); render();
});
nav.addEventListener("click", (e) => {
  const c = (e.target as Element).closest<HTMLElement>(".chip");
  if (!c) return;
  ativo = +c.dataset.b!; busca.value = "";
  chips(); render();
});

/* Abrir e fechar fichas; copiar referências */
lista.addEventListener("click", (e) => {
  const alvo = e.target as Element;
  const q = alvo.closest<HTMLElement>(".q");
  if (q) {
    const body = document.getElementById(q.getAttribute("aria-controls")!)!;
    const abrir = body.hidden;
    body.hidden = !abrir;
    q.setAttribute("aria-expanded", String(abrir));
    q.querySelector(".mark")!.textContent = abrir ? "−" : "+";
    return;
  }
  const c = alvo.closest<HTMLElement>(".copy");
  if (c) {
    const d = TEMAS[tema].blocos[+c.dataset.b!].itens[+c.dataset.i!];
    const ok = () => { c.textContent = "Copiado"; setTimeout(() => (c.textContent = "Copiar referências"), 1600); };
    const falha = () => { c.textContent = "Não foi possível copiar"; setTimeout(() => (c.textContent = "Copiar referências"), 2200); };
    try { navigator.clipboard.writeText(textoParaCopiar(d)).then(ok, falha); } catch { falha(); }
  }
});

/* Janela do Catecismo */
let voltar: HTMLElement | null = null;
const CORES = ["tema-mariana", "tema-liturgica", "tema-branca", "tema-roxa", "tema-vermelha"];
function fechar() { modal.hidden = true; voltar?.focus(); }
lista.addEventListener("click", (e) => {
  const b = (e.target as Element).closest<HTMLElement>(".cicbtn");
  if (!b) return;
  const item = b.closest(".item")!;
  const j = janelaCatecismo(b.dataset.ref!, CORES.find((t) => item.classList.contains(t)) || "");
  if (!j) return;
  mcaixa.className = j.cls; mtit.textContent = j.tit; mcorpo.innerHTML = j.corpo;
  voltar = b; modal.hidden = false; mfechar.focus();
});
modal.addEventListener("click", (e) => { if (e.target === modal || (e.target as Element).closest("#mfechar")) fechar(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !modal.hidden) fechar(); });

busca.addEventListener("input", render);
temas(); chips(); render();

/* Funcionamento sem internet */
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch(() => {});
    /* apaga o cache da versão anterior (veritas-v1...), que guardava o index.html inteiro */
    if ("caches" in window) caches.keys().then((ks) => ks.filter((k) => /^veritas-v\d+$/.test(k)).forEach((k) => caches.delete(k))).catch(() => {});
  });
}
