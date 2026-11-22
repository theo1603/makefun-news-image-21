// News-image entry for make.fun's "Sum up 21 November's world news in one
// image" bounty. The image is the entry.png beside this file: a one-page
// newspaper poster drawn from the day's reported stories (see
// draw_poster.py, which generated it). The program just copies it to the
// grader's output directory, so both runs write byte-identical output.
// Node 22, standard library only; no network.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
if (!existsSync(source)) {
  throw new Error("entry.png missing next to main.ts; run draw_poster.py first");
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
