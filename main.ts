import { copyFileSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

// The grader runs this file as `node /bot/main.ts` from a working
// directory that is not the repository, so a bare "entry.png" would
// throw ENOENT there. Anchor every path to this script's own folder.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(scriptDir, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

// A real PNG opens with this 8-byte signature. Refuse anything else
// here so a corrupt file fails loudly instead of shipping broken.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

const source = readFileSync(sourcePath);
if (
  source.length < PNG_SIGNATURE.length ||
  !source.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)
) {
  throw new Error("entry.png is not a valid PNG (bad signature)");
}
if (source.length === 0 || source.length > 1024 * 1024) {
  throw new Error(`entry.png has an implausible size (${source.length} bytes)`);
}
copyFileSync(sourcePath, join(outputDir, "entry.png"));

// Confirm the copy landed intact before the run ends.
const copied = readFileSync(join(outputDir, "entry.png"));
if (copied.length !== source.length) {
  throw new Error("entry.png copy is incomplete");
}
