require("dotenv").config();

console.log("🔥 SINGLE FILE OCR MODE 🔥");

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const transform = require("./transform");

const {
  DocumentAnalysisClient,
  AzureKeyCredential
} = require("@azure/ai-form-recognizer");


// --------------------
// ENV
// --------------------

const endpoint = process.env.AZURE_OCR_ENDPOINT;
const key = process.env.AZURE_OCR_KEY;


// --------------------
// CLIENT
// --------------------

const ocrClient = new DocumentAnalysisClient(
  endpoint,
  new AzureKeyCredential(key)
);


// --------------------
// CONFIG
// --------------------

const INPUT_FILE = process.argv[2];
const OUTPUT_DIR = "./ocr_outputs";


// --------------------
// VALIDATION
// --------------------

if (!INPUT_FILE) {
  console.error("❌ No file provided");
  process.exit(1);
}

if (!fs.existsSync(INPUT_FILE)) {
  console.error("❌ File not found:", INPUT_FILE);
  process.exit(1);
}


// --------------------
// OUTPUT DIR
// --------------------

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}


// --------------------
// MAIN
// --------------------

async function run() {

  const fileName = path.basename(INPUT_FILE);

  console.log("Processing:", fileName);


  // --------------------
  // Register
  // --------------------

  try {
    execSync(`python rag/auto_register.py "${fileName}"`);
    console.log("Registered ✅");
  }
  catch {
    console.log("Registration skipped ⚠️");
  }


  // --------------------
  // Read file
  // --------------------

  const buffer = fs.readFileSync(INPUT_FILE);


  // --------------------
  // OCR
  // --------------------

  console.log("Running OCR...");

  const poller =
    await ocrClient.beginAnalyzeDocument(
      "prebuilt-layout",
      buffer
    );

  const result = await poller.pollUntilDone();

  console.log("OCR done ✅");


  // --------------------
  // Transform
  // --------------------

  const docId = fileName
    .replace(".pdf", "")
    .replace(/\s+/g, "_");


  const clean = transform(result, docId);


  // --------------------
  // Save
  // --------------------

  const outPath =
    path.join(OUTPUT_DIR, `${docId}.json`);

  fs.writeFileSync(
    outPath,
    JSON.stringify(clean, null, 2)
  );

  console.log("Saved →", outPath, "✅");

  console.log("\nPIPELINE COMPLETE 🔥");
}


run().catch(err => {
  console.error("❌ OCR Failed:", err);
  process.exit(1);
});
