import json
import os
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


# ------------------------
# PATHS (FIXED)
# ------------------------

BASE = os.path.dirname(os.path.abspath(__file__))

OCR_DIR = os.path.abspath(
    os.path.join(BASE, "..", "ocr_outputs")
)

DB_DIR = os.path.join(BASE, "db")


# ------------------------
# HELPERS
# ------------------------

def detect_section(text):

    patterns = [
        r"^\d+\.\d+(\.\d+)?\s+.+",
        r"^phase\s+[ivx]+",
        r"^phase\s+\d+"
    ]

    for p in patterns:
        if re.match(p, text.strip(), re.I):
            return text.strip()

    return None


# ------------------------
# INIT
# ------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Ensure DB folder exists
os.makedirs(DB_DIR, exist_ok=True)


all_docs = []


# ------------------------
# LOAD OCR FILES
# ------------------------

if not os.path.exists(OCR_DIR):
    raise Exception(f"OCR folder not found: {OCR_DIR}")


for file in os.listdir(OCR_DIR):

    if not file.endswith(".json"):
        continue


    doc_id = file.replace(".json", "")

    path = os.path.join(OCR_DIR, file)


    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)


    current_section = "Introduction"


    for page in data["pages"]:

        page_no = page["page_no"]

        para_no = 1
        buffer = []


        for line in page["lines"]:

            text = line["text"].strip()


            sec = detect_section(text)

            if sec:
                current_section = sec


            if text == "":
                para_no += 1
                continue


            buffer.append(text)


        page_text = "\n".join(buffer)

        chunks = splitter.split_text(page_text)


        for chunk in chunks:

            all_docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "doc": doc_id,
                        "page": page_no,
                        "section": current_section,
                        "para": para_no
                    }
                )
            )


# ------------------------
# BUILD VECTOR DB
# ------------------------

if not all_docs:
    raise Exception("No OCR data found to index")


db = FAISS.from_documents(all_docs, embeddings)

db.save_local(DB_DIR)

print("Vector DB built at:", DB_DIR, "✅")
