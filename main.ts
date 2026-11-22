import { copyFileSync, readFileSync } from "node:fs";

// A valid PNG always starts with this 8-byte signature. Verify it before
// copying so a corrupt or non-PNG entry.png fails loudly here instead of
// silently shipping a broken image to the grader.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

const source = readFileSync("entry.png");
if (
  source.length < PNG_SIGNATURE.length ||
  !source.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)
) {
  throw new Error("entry.png is not a valid PNG (bad signature)");
}
copyFileSync("entry.png", "/output/entry.png");
