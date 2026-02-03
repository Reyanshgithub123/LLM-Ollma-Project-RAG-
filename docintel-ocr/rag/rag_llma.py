# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.llms import Ollama


# # Load embeddings
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# # Load DB
# db = FAISS.load_local(
#     "db",
#     embeddings,
#     allow_dangerous_deserialization=True
# )


# # Llama Model
# llm = Ollama(model="llama3.1:8b")


# def ask(question):

#     docs = db.similarity_search(question, k=5)

#     if not docs:
#         return "No evidence found"

#     context = "\n\n".join(
#         [d.page_content for d in docs]
#     )

#     prompt = f"""
# You are a clinical document analyst.

# Use ONLY this context.

# Context:
# {context}

# Question:
# {question}

# Rules:
# - Answer only from context
# - If not found say: No evidence found
# """

#     return llm.invoke(prompt)


# # CLI
# while True:

#     q = input("Ask> ")

#     if q.lower() == "exit":
#         break

#     print("\nAnswer:\n", ask(q), "\n")
import os
import json
import uuid
import sqlite3
import re

from datetime import datetime

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM


# ------------------------
# PATH CONFIG (IMPORTANT)
# ------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "documents.db")
DB_DIR = os.path.join(BASE_DIR, "db")
SNAPSHOT_DIR = os.path.join(BASE_DIR, "evidence_snapshots")


# ------------------------
# HELPERS
# ------------------------

def normalize(name):
    """
    Normalize filenames for matching
    """
    return name.lower().replace(" ", "_").replace(".pdf", "")


def get_latest_versions():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT trial_id, doc_type, blob_path, version
        FROM documents
        WHERE status='approved'
    """).fetchall()

    conn.close()


    latest = {}

    for trial, dtype, blob, v in rows:

        key = (trial, dtype)

        try:
            num = float(v.replace("v", ""))
        except:
            num = 0.0


        if key not in latest or num > latest[key][0]:
            latest[key] = (num, blob)


    return latest


# ------------------------
# INIT
# ------------------------

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load Vector DB
db = FAISS.load_local(
    DB_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)


# LLM
llm = OllamaLLM(
    model="llama3.2:3b"
)


# Ensure snapshot folder exists
os.makedirs(SNAPSHOT_DIR, exist_ok=True)


# ------------------------
# MAIN QUERY
# ------------------------

def ask(question):

    # Search wide
    docs_all = db.similarity_search(question, k=15)

    if not docs_all:
        return "No evidence found"


    # Get allowed docs from registry
    latest_map = get_latest_versions()


    allowed = set()

    for (_, blob) in latest_map.values():
        allowed.add(normalize(blob))


    # Filter vectors
    docs = []

    for d in docs_all:

        vec_doc = normalize(d.metadata.get("doc", ""))

        if vec_doc in allowed:

            docs.append(d)

        if len(docs) == 1:
            break


    if not docs:
        return "No evidence found (filtered by registry)"


    # Best doc
    d = docs[0]


    # ------------------------
    # META
    # ------------------------

    answer_id = "A" + uuid.uuid4().hex[:8]

    timestamp = datetime.utcnow().isoformat()


    doc = d.metadata.get("doc", "Unknown") + ".pdf"
    section = d.metadata.get("section", "Unknown")
    page = d.metadata.get("page", "Unknown")
    para = d.metadata.get("para", "Unknown")

    version = "v1.0"


    # ------------------------
    # QUOTE
    # ------------------------

    text = d.page_content.replace("\n", " ").strip()

    sentences = text.split(". ")

    quote = ". ".join(sentences[:2])

    if not quote.endswith("."):
        quote += "."


    # ------------------------
    # SNAPSHOT
    # ------------------------

    snapshot = {
        "answer_id": answer_id,
        "document": doc,
        "version": version,
        "section": section,
        "page": page,
        "paragraph": para,
        "evidence_text": quote,
        "timestamp": timestamp
    }


    file_path = os.path.join(SNAPSHOT_DIR, f"{answer_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)


    # ------------------------
    # LLM
    # ------------------------

    context = d.page_content


    prompt = f"""
You are a regulatory document analyst.

Answer ONLY from context.

Context:
{context}

Question:
{question}

Rules:
- Be precise
- No hallucination
"""


    answer = llm.invoke(prompt)


    # ------------------------
    # OUTPUT
    # ------------------------

    evidence_text = f"""
“{quote}”

According to {doc} → Section {section} → Page {page} → Paragraph {para}
""".strip()


    final = f"""
Answer ID: {answer_id}

Answer:
{answer}

Evidence:
{evidence_text}

Snapshot saved: {file_path}
"""


    return final


# ------------------------
# CLI
# ------------------------

if __name__ == "__main__":

    print("RAG System Ready ✅")
    print("Type 'exit' to quit\n")


    while True:

        q = input("Ask> ")

        if q.lower() == "exit":
            break

        print(ask(q))
