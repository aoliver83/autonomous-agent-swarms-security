#!/usr/bin/env node
// Mira — modo offline para um deck JÁ existente (decks criados antes desta versão,
// ou para reparar um deck que voltou a referenciar CDN). Decks NOVOS já nascem
// offline pelo próprio "npx mira-animator new" — esta ferramenta é a rede de seguro.
//
//   node mira-templates/vendor/apply-offline.mjs decks/<deck>
//
// NÃO baixa nada — só copia o que já está em mira-templates/vendor/. Idempotente.

import { existsSync, statSync } from 'fs';
import { join, dirname, resolve, basename } from 'path';
import { fileURLToPath } from 'url';
import { applyOffline } from './offline-core.mjs';

const VENDOR_SRC = dirname(fileURLToPath(import.meta.url));
const deckArg = process.argv[2];

if (!deckArg) {
  console.error('Uso: node mira-templates/vendor/apply-offline.mjs <pasta-do-deck>');
  process.exit(1);
}
const deckDir = resolve(process.cwd(), deckArg);
if (!existsSync(deckDir) || !statSync(deckDir).isDirectory()) {
  console.error(`Pasta do deck nao encontrada: ${deckDir}`);
  process.exit(1);
}

const { copied, reports, warnings, htmlCount } = applyOffline(deckDir, VENDOR_SRC);

console.log(`\nMira offline — deck: ${basename(deckDir)}`);
console.log(`Bundle copiado para assets/vendor/ (${copied} arquivos).`);
console.log(`HTMLs processados (${htmlCount}):`);
reports.forEach(r => console.log('  ' + r));
if (warnings.length) {
  console.log(`\nAtencao (${warnings.length}):`);
  warnings.forEach(w => console.log('  - ' + w));
} else {
  console.log(`\nOK: nenhuma dependencia externa remanescente nos HTMLs conhecidos.`);
}
console.log('');
