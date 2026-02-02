require("dotenv").config();

const fs = require("fs");
const path = require("path");

const transform = require("./transform");

const {
  DocumentAnalysisClient,
  AzureKeyCredential
} = require("@azure/ai-form-recognizer");

const {
  BlobServiceClient
} = require("@azure/storage-blob");


// ENV
const endpoint = process.env.AZURE_OCR_ENDPOINT;
const key = process.env.AZURE_OCR_KEY;

const AZURE_STORAGE_CONNECTION =
  process.env.AZURE_STORAGE_CONNECTION_STRING;


// Clients
const ocrClient = new DocumentAnalysisClient(
  endpoint,
  new AzureKeyCredential(key)
);

const blobClient = BlobServiceClient.fromConnectionString(
  AZURE_STORAGE_CONNECTION
);


// CONFIG
const CONTAINER = "raw-documents";
const OUTPUT_DIR = "./ocr_outputs";


// Create output folder
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR);
}


// Get all PDFs from blob
async function listPDFFiles() {

  const container =
    blobClient.getContainerClient(CONTAINER);

  const files = [];

  for await (const blob of container.listBlobsFlat()) {

    if (blob.name.endsWith(".pdf")) {
      files.push(blob.name);
    }
  }

  return files;
}


// OCR One File
async function processFile(fileName) {

  console.log(`\nProcessing: ${fileName}`);

  const container =
    blobClient.getContainerClient(CONTAINER);

  const blob =
    container.getBlockBlobClient(fileName);


  // Generate SAS URL (valid for 1 hour)
  const sasUrl = await blob.generateSasUrl({
    permissions: "r",
    expiresOn: new Date(Date.now() + 60 * 60 * 1000)
  });


  const poller =
    await ocrClient.beginAnalyzeDocumentFromUrl(
      "prebuilt-layout",
      sasUrl
    );

  const result = await poller.pollUntilDone();


  // Transform
  const docId = fileName
    .replace(".pdf", "")
    .replace(/\s+/g, "_");

  const clean = transform(result, docId);


  // Save
  fs.writeFileSync(
    `${OUTPUT_DIR}/${docId}.json`,
    JSON.stringify(clean, null, 2)
  );


  console.log(`Saved → ${docId}.json ✅`);
}


// MAIN
async function runBatchOCR() {

  console.log("Fetching PDF list...");

  const files = await listPDFFiles();

  console.log(`Found ${files.length} PDFs`);

  for (const file of files) {

    try {
      await processFile(file);
    }
    catch (err) {
      console.error("Error:", file, err.message);
    }
  }

  console.log("\nBatch OCR Done 🔥");
}


runBatchOCR();
