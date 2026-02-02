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

from datetime import datetime

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM


# ------------------------
# CONFIG
# ------------------------

MODEL_NAME = "llama3.2:3b"     # change if needed
SNAPSHOT_DIR = "evidence_snapshots"


# ------------------------
# INIT
# ------------------------

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load Vector DB
db = FAISS.load_local(
    "db",
    embeddings,
    allow_dangerous_deserialization=True
)

# LLM
llm = OllamaLLM(
    model=MODEL_NAME
)

# Ensure snapshot folder exists
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def is_approved(doc_name):

    conn = sqlite3.connect("documents.db")
    cur = conn.cursor()

    res = cur.execute("""
        SELECT status FROM documents
        WHERE blob_path = ?
    """, (doc_name,)).fetchone()

    conn.close()

    if not res:
        return False

    return res[0] == "approved"

# ------------------------
# MAIN QUERY
# ------------------------

def ask(question):

    # Get BEST match only
    # docs = db.similarity_search(question, k=1)
    docs_all = db.similarity_search(question, k=5)

    docs = []

    for d in docs_all:

        docname = d.metadata.get("doc", "") + ".pdf"

        if is_approved(docname):
            docs.append(d)

        if len(docs) == 1:
            break


    if not docs:
        return "No evidence found"


    d = docs[0]   # Top result


    # Unique Answer ID
    answer_id = "A" + uuid.uuid4().hex[:8]

    # Timestamp
    timestamp = datetime.utcnow().isoformat()


    # Metadata
    doc = d.metadata.get("doc", "Unknown") + ".pdf"
    section = d.metadata.get("section", "Unknown")
    page = d.metadata.get("page", "Unknown")
    para = d.metadata.get("para", "Unknown")

    version = "v1.0"   # Optional


    # Clean Text
    text = d.page_content.replace("\n", " ").strip()


    # Take first 2 sentences
    sentences = text.split(". ")

    quote = ". ".join(sentences[:2])

    if not quote.endswith("."):
        quote += "."


    # ------------------------
    # Build Snapshot
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


    file_path = f"{SNAPSHOT_DIR}/{answer_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)


    # ------------------------
    # Build LLM Context
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


    # Generate Answer
    answer = llm.invoke(prompt)


    # ------------------------
    # Final Output
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
