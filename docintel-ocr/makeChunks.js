const fs = require("fs");
const makeChunks = require("./chunker");

const data = JSON.parse(
  fs.readFileSync("structured_ocr.json", "utf8")
);

const chunks = makeChunks(data, "doc_019");

fs.writeFileSync(
  "chunks.json",
  JSON.stringify(chunks, null, 2)
);

console.log("Chunks created ✅");
