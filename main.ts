// News-image entry for 19 November 2026 (Node 22, standard library only).
// The entry image lives beside this file as entry.png; this program writes
// exactly those bytes to /output/entry.png (or MAKEFUN_OUTPUT_DIR when set
// for a local run), so both grader runs produce identical output.
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, "entry.png"));
if (bytes.length === 0 || bytes.length > 1048576) {
  throw new Error("entry.png must be a non-empty file under 1 MiB");
}
writeFileSync(target, bytes);
