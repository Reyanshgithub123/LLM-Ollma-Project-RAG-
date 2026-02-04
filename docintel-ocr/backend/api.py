import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import subprocess
import json

from rag.rag_llma import ask


app = FastAPI()


# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# Upload PDF
# -------------------------

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)


    # -------------------------
    # RUN OCR PIPELINE
    # -------------------------

    subprocess.run([
        "node",
        "multi_ocr.js"
    ], check=True)


    # -------------------------
    # REBUILD INDEX
    # -------------------------

    subprocess.run([
        "python",
        "rag/build_index_multi.py"
    ], check=True)


    return {
        "status": "success",
        "file": file.filename,
        "message": "Uploaded, OCR done, indexed"
    }


# -------------------------
# Ask RAG
# -------------------------

@app.post("/ask")
async def ask_question(data: dict):

    question = data["question"]

    result = ask(question)

    return {
        "result": result
    }
