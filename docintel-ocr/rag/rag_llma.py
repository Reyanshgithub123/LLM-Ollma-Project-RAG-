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

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM


# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load DB
db = FAISS.load_local(
    "db",
    embeddings,
    allow_dangerous_deserialization=True
)


# LLM
llm = OllamaLLM(
    model="llama3.2:3b"
)


def ask(question):

    docs = db.similarity_search(question, k=4)

    if not docs:
        return "No evidence found"


    citations = []
    context_parts = []


    for d in docs:

        page = d.metadata.get("page", "Unknown")
        section = d.metadata.get("section", "Unknown")

        snippet = d.page_content[:200].replace("\n", " ")

        citations.append(
            f"Section {section} (Page {page}): \"{snippet}...\""
        )

        context_parts.append(
            f"[{section} | Page {page}]\n{d.page_content}"
        )


    context = "\n\n".join(context_parts)


    prompt = f"""
You are a regulatory document analyst.

Answer ONLY from context.

Context:
{context}

Question:
{question}

Rules:
- Be precise
- Do not hallucinate
"""

    answer = llm.invoke(prompt)


    citation_block = "\n".join(citations)


    final = f"""
Answer:
{answer}

Evidence:
{citation_block}
"""

    return final


# CLI
while True:

    q = input("Ask> ")

    if q.lower() == "exit":
        break

    print(ask(q))
