# import json
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings


# # Load OCR JSON
# with open("../structured_ocr.json", "r", encoding="utf-8") as f:
#     data = json.load(f)


# # Convert to text
# texts = []

# for page in data["pages"]:
#     for line in page["lines"]:
#         texts.append(line["text"])

# full_text = "\n".join(texts)


# # Chunk
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=800,
#     chunk_overlap=100
# )

# docs = splitter.create_documents([full_text])


# # Free embeddings
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# # FAISS DB
# db = FAISS.from_documents(docs, embeddings)

# db.save_local("db")

# print("Local vector DB built ✅")

import json
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


# Load OCR JSON
with open("../structured_ocr.json", "r", encoding="utf-8") as f:
    data = json.load(f)


documents = []

current_section = "Introduction"


def detect_section(text):

    # Matches: 5.1 Title, 3.2.4 Something, Phase II
    patterns = [
        r"^\d+\.\d+(\.\d+)?\s+.+",   # 5.1 / 3.2.1
        r"^phase\s+[ivx]+",         # Phase II
        r"^phase\s+\d+"             # Phase 2
    ]

    for p in patterns:
        if re.match(p, text.strip(), re.I):
            return text.strip()

    return None


# Build docs
for page in data["pages"]:

    page_no = page["page_no"]
    buffer = []

    for line in page["lines"]:

        text = line["text"].strip()

        sec = detect_section(text)

        if sec:
            current_section = sec

        buffer.append(text)


    page_text = "\n".join(buffer)

    documents.append({
        "text": page_text,
        "page": page_no,
        "section": current_section
    })


# Chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)


langchain_docs = []

for doc in documents:

    chunks = splitter.split_text(doc["text"])

    for chunk in chunks:

        langchain_docs.append(
            Document(
                page_content=chunk,
                metadata={
                    "page": doc["page"],
                    "section": doc["section"]
                }
            )
        )


# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Build DB
db = FAISS.from_documents(langchain_docs, embeddings)

db.save_local("db")

print("Vector DB with Section + Page built ✅")
