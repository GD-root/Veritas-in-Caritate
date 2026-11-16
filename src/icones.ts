/* Ícones dos temas e blocos (desenhos em SVG). */
const SV = (d: string): string => `<svg class="sym" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;
export const ICONE: Record<string, string> = {
 "Defesa da fé": SV('<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M12 8v8M9 11h6"/>'),
 "Resposta à Reforma": SV('<rect x="6" y="3" width="12" height="18" rx="1"/><path d="M9 7h6M9 10h6M9 13h4"/><circle cx="15.5" cy="16.5" r=".8" fill="currentColor"/>'),
 "Valores católicos": SV('<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'),
 "Santíssima Virgem Maria": SV('<path d="M5 19V8l7 7 7-7v11"/><path d="M12 3v6M9.5 5.5h5"/>'),
 "Igreja, Pedro e o Papa": SV('<circle cx="6.5" cy="6.5" r="2.5"/><path d="M8.3 8.3L19 19M16 19h3v-3"/><circle cx="17.5" cy="6.5" r="2.5"/><path d="M15.7 8.3L5 19M8 19H5v-3"/>'),
 "Bíblia e Tradição": SV('<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/><path d="M12 6.5v5M10 8.5h4"/>'),
 "Sacramentos e salvação": SV('<path d="M7 4h10c0 5-2 8-5 8s-5-3-5-8z"/><path d="M12 12v6M8 20h8"/>'),
 "Cristo, mandamentos e domingo": SV('<path d="M12 3v18M7 8h10"/>'),
 "Imagens, santos e relíquias": SV('<path d="M9 10h6v11H9z"/><path d="M12 10V8"/><path d="M12 3c1.5 1.6 1.5 3.4 0 5-1.5-1.6-1.5-3.4 0-5z"/>'),
 "As cinco solas": SV('<path d="M7 3h8l3 3v15H7z"/><path d="M15 3v3h3"/><path d="M10 11h5M10 14h5M10 17h3"/>'),
 "Virtudes teologais": SV('<path d="M12 21v-6"/><path d="M8 15h8"/><path d="M12 4c2.5 2.5 3.5 5 0 9-3.5-4-2.5-6.5 0-9z"/>'),
 "Virtudes cardeais": SV('<circle cx="12" cy="12" r="8"/><path d="M12 6l1.8 4.2L18 12l-4.2 1.8L12 18l-1.8-4.2L6 12l4.2-1.8z"/>'),
 "Vida, matrimônio e família": SV('<path d="M4 11l8-6 8 6"/><path d="M6 10v10h12V10"/><path d="M12 18s-3-1.8-3-4a1.5 1.5 0 0 1 3-.8 1.5 1.5 0 0 1 3 .8c0 2.2-3 4-3 4z"/>')
};
