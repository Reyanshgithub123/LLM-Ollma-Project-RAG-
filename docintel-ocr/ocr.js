require("dotenv").config();
const fs = require("fs");
const transform = require("./transform");

const {
  DocumentAnalysisClient,
  AzureKeyCredential
} = require("@azure/ai-form-recognizer");

const endpoint = process.env.AZURE_OCR_ENDPOINT;
const key = process.env.AZURE_OCR_KEY;

const client = new DocumentAnalysisClient(
  endpoint,
  new AzureKeyCredential(key)
);

// 👇 Put your blob file URL here
const fileUrl = "https://stdataeradocinteldev.blob.core.windows.net/raw-documents/Article%20019.pdf?sp=r&st=2026-01-30T15:48:47Z&se=2026-01-31T00:03:47Z&spr=https&sv=2024-11-04&sr=b&sig=jK6kvIKus6udxb6hLnT80A1UHwFzVWJTpHkXShSOr0g%3D";

async function runOCR() {

  console.log("Starting OCR...");

  const poller =
    await client.beginAnalyzeDocumentFromUrl(
      "prebuilt-layout",
      fileUrl
    );

  const result = await poller.pollUntilDone();

  console.log("OCR Done ✅");

  // 1️⃣ Save raw OCR
  fs.writeFileSync(
    "raw_ocr.json",
    JSON.stringify(result, null, 2)
  );

  // 2️⃣ Transform
  const clean = transform(result, "doc_001");

  // 3️⃣ Save structured OCR
  fs.writeFileSync(
    "structured_ocr.json",
    JSON.stringify(clean, null, 2)
  );

  console.log("Saved raw_ocr.json & structured_ocr.json ✅");
}

runOCR();