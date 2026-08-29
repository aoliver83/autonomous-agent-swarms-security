// Mira — núcleo do modo offline (sem dependências externas, só fs).
// Compartilhado por:
//   - lib/commands/new.js        -> todo deck novo já nasce offline
//   - templates/vendor/apply-offline.mjs -> localiza um deck já existente
//
// applyOffline(deckDir, vendorSrc) copia as libs vendoradas para
// <deckDir>/assets/vendor/ e reescreve TODOS os HTMLs do deck para caminhos
// relativos locais. NÃO baixa nada — só copia o que já está em vendorSrc.

import {
  existsSync, mkdirSync, copyFileSync, readdirSync,
  readFileSync, writeFileSync, cpSync,
} from 'fs';
import { join, basename } from 'path';

// Arquivos comuns, copiados em TODO deck.
export const BUNDLE = ['tailwind.js', 'aos.css', 'aos.js', 'lucide.js', 'd3.v7.min.js', 'inter.css'];

const V = 'assets/vendor/';

// CDN (bloqueável) -> caminho local relativo. Os HTMLs do deck vivem na raiz da
// pasta do deck, então o prefixo é sempre 'assets/vendor/'.
const RULES = [
  [/https?:\/\/cdn\.tailwindcss\.com[^\s"'>]*/g, V + 'tailwind.js'],
  [/https?:\/\/unpkg\.com\/aos@[^/]+\/dist\/aos\.css[^\s"'>]*/g, V + 'aos.css'],
  [/https?:\/\/unpkg\.com\/aos@[^/]+\/dist\/aos\.js[^\s"'>]*/g, V + 'aos.js'],
  [/https?:\/\/unpkg\.com\/lucide@[^\s"'>]*/g, V + 'lucide.js'],
  [/https?:\/\/d3js\.org\/d3\.v7\.min\.js[^\s"'>]*/g, V + 'd3.v7.min.js'],
  [/https?:\/\/fonts\.googleapis\.com\/css2\?family=Inter[^\s"'>]*/g, V + 'inter.css'],
  // Three.js (mira-3d): importmap -> local. Os addons preservam seus imports bare
  // ('three', 'three/addons/...'), resolvidos pelo próprio importmap local.
  [/https?:\/\/unpkg\.com\/three@[^/]+\/build\/three\.module\.js[^\s"'>]*/g, V + 'three/three.module.js'],
  [/https?:\/\/unpkg\.com\/three@[^/]+\/examples\/jsm\//g, V + 'three/addons/'],
];

function listHtml(deckDir) {
  return readdirSync(deckDir)
    .filter(f => f.toLowerCase().endsWith('.html'))
    .map(f => join(deckDir, f));
}

/**
 * @param {string} deckDir   pasta do deck (contém os .html)
 * @param {string} vendorSrc pasta com as libs vendoradas (BUNDLE + fonts/ + three/)
 * @returns {{copied:number, reports:string[], warnings:string[], htmlCount:number}}
 */
export function applyOffline(deckDir, vendorSrc) {
  const assetsVendor = join(deckDir, 'assets', 'vendor');
  mkdirSync(join(assetsVendor, 'fonts'), { recursive: true });

  // 1. Copiar o bundle comum.
  let copied = 0;
  for (const f of BUNDLE) {
    const src = join(vendorSrc, f);
    if (existsSync(src)) { copyFileSync(src, join(assetsVendor, f)); copied++; }
  }
  const fontsSrc = join(vendorSrc, 'fonts');
  if (existsSync(fontsSrc)) {
    for (const f of readdirSync(fontsSrc)) { copyFileSync(join(fontsSrc, f), join(assetsVendor, 'fonts', f)); copied++; }
  }

  // 2. Three.js só se algum HTML usar (é pesado, ~1,4 MB).
  const htmlFiles = listHtml(deckDir);
  const usesThree = htmlFiles.some(f => /unpkg\.com\/three@|"three"\s*:/.test(readFileSync(f, 'utf8')));
  let threeCopied = false;
  if (usesThree && existsSync(join(vendorSrc, 'three'))) {
    cpSync(join(vendorSrc, 'three'), join(assetsVendor, 'three'), { recursive: true, force: true });
    threeCopied = true;
  }

  // 3. Reescrever cada HTML.
  const reports = [];
  const warnings = [];
  for (const file of htmlFiles) {
    let html = readFileSync(file, 'utf8');
    const before = html;
    const hits = [];
    for (const [re, local] of RULES) {
      if (re.test(html)) { hits.push(local); html = html.replace(re, local); }
      re.lastIndex = 0;
    }
    // preconnect de fonts: externo e inútil offline.
    html = html.replace(/\s*<link[^>]*rel=["']preconnect["'][^>]*fonts\.(googleapis|gstatic)\.com[^>]*>/g, '');

    if (/three\/three\.module\.js/.test(html) && threeCopied) {
      hits.push(V + 'three/');
    } else if (/unpkg\.com\/three@/.test(html) || /"three"\s*:/.test(html)) {
      warnings.push(`${basename(file)}: usa Three.js mas o bundle não tem three/ ` +
        `(instalação antiga?). Rode "npx mira-animator update".`);
    }
    const leftover = [...html.matchAll(/(?:src|href)=["'](https?:\/\/[^"']+)["']/g)]
      .map(m => m[1]).filter(u => !/fonts\.(googleapis|gstatic)\.com/.test(u));
    if (leftover.length) warnings.push(`${basename(file)}: ainda referencia externo: ${[...new Set(leftover)].join(', ')}`);

    if (html !== before) {
      writeFileSync(file, html, 'utf8');
      reports.push(`${basename(file)}: ${[...new Set(hits)].length} recurso(s) localizado(s)`);
    } else {
      reports.push(`${basename(file)}: nada a localizar (já offline ou sem CDN conhecida)`);
    }
  }

  return { copied, reports, warnings, htmlCount: htmlFiles.length };
}
