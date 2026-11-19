// main.ts — entrypoint for the gta6-meme-x-01 bounty ("Post a GTA 6 meme on X").
//
// The post on X is the entry itself; this program only hands the house the
// file that names it. It copies POST.json from the repository into the
// output directory the house reads.
//
// Environment:
//   MAKEFUN_BOT_DIR     — where the repository lives (default /bot)
//   MAKEFUN_OUTPUT_DIR  — where POST.json must land (default /output)

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

try {
  mkdirSync(outDir, { recursive: true });
  const from = join(botDir, "POST.json");
  const to = join(outDir, "POST.json");
  copyFileSync(from, to);
  console.log(`POST.json copied to ${to}`);
} catch (err) {
  // A missing or unreadable POST.json is fatal: without it the house cannot
  // find the post, so fail loudly instead of writing a partial output.
  const reason = err instanceof Error ? err.message : String(err);
  console.error(`failed to copy POST.json from ${botDir}: ${reason}`);
  process.exit(1);
}
