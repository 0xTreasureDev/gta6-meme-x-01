// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry itself is a post on X; this repository only has to hand in the
// post's address. POST.json at the repository root names it, and the grader
// expects that same file at /output/POST.json. So the whole job here is:
// read POST.json from the bot directory, make sure it is the JSON object the
// gate expects (an object with a string "url"), then copy its bytes verbatim
// into the output directory. Nothing else is written, nothing is printed on
// success, and two runs over the same POST.json produce the same bytes.
//
// Locally:  mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

let raw: Buffer;
try {
  raw = readFileSync(join(botDir, 'POST.json'));
} catch {
  fail(`POST.json is not readable in ${botDir}`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(raw!.toString('utf8'));
} catch {
  fail('POST.json is not valid JSON');
}

const url = (parsed as { url?: unknown } | null)?.url;
if (typeof url !== 'string' || !url.startsWith('https://') || !url.includes('/status/')) {
  fail('POST.json must be an object whose "url" is an X post address');
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'POST.json'), raw!);
