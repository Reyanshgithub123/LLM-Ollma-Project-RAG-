# import os
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from backend.audit import init_db, log_event, get_logs, get_stats

# import subprocess
# import json

# from rag.rag_llma import ask


# app = FastAPI()
# init_db()


# # Allow frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # -------------------------
# # Upload PDF
# # -------------------------

# @app.post("/upload")
# async def upload(file: UploadFile = File(...)):

#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     # Save file
#     with open(file_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)


#     # -------------------------
#     # RUN OCR PIPELINE
#     # -------------------------

#     subprocess.run([
#         "node",
#         "multi_ocr.js"
#     ], check=True)


#     # -------------------------
#     # REBUILD INDEX
#     # -------------------------

#     subprocess.run([
#         "python",
#         "rag/build_index_multi.py"
#     ], check=True)


#     return {
#         "status": "success",
#         "file": file.filename,
#         "message": "Uploaded, OCR done, indexed"
#     }


# # -------------------------
# # Ask RAG
# # -------------------------

# @app.post("/ask")
# async def ask_question(data: dict):

#     question = data["question"]

#     result = ask(question)

#     return {
#         "result": result
#     }

import os
import shutil
import subprocess

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.audit import (
    init_db,
    log_event,
    get_logs,
    get_stats
)

from rag.rag_llma import ask


# -------------------------
# APP INIT
# -------------------------

app = FastAPI()

# Init audit DB
init_db()


# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# PATHS
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "../uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# HELPERS
# -------------------------

def get_client_ip(request: Request):

    if request.client:
        return request.client.host

    return "unknown"


# -------------------------
# UPLOAD PDF
# -------------------------

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    print("Saved upload:", file_path)


    # -------------------------
    # RUN OCR (ONLY THIS FILE)
    # -------------------------

    subprocess.run([
        "node",
        "multi_ocr.js",
        file_path
    ], check=True)


    # -------------------------
    # REBUILD INDEX
    # -------------------------

    subprocess.run([
        "python",
        "rag/build_index_multi.py"
    ], check=True)


    # -------------------------
    # AUDIT
    # -------------------------

    log_event(
        "upload",
        f"Uploaded {file.filename}"
    )


    return {
        "status": "success",
        "file": file.filename,
        "message": "Uploaded + OCR + Indexed"
    }




# -------------------------
# ASK RAG
# -------------------------

@app.post("/ask")
async def ask_question(
    request: Request,
    data: dict
):

    question = data.get("question", "").strip()

    if not question:

        return {
            "result": "No question provided"
        }


    # Log AI query
    log_event(
        event_type="ai",
        message=f"Question asked: {question[:80]}",
        user="demo_user",
        ip=get_client_ip(request)
    )


    try:

        result = ask(question)

        return {
            "result": result
        }


    except Exception as e:

        log_event(
            event_type="security",
            message=f"AI failure: {str(e)}",
            user="system",
            ip=get_client_ip(request)
        )

        return {
            "result": "AI processing failed",
            "detail": str(e)
        }


# -------------------------
# AUDIT LOGS
# -------------------------

@app.get("/audit/logs")
def fetch_logs():

    rows = get_logs()

    data = []

    for event, msg, user, ip, ts in rows:

        data.append({
            "event": event,
            "message": msg,
            "user": user,
            "ip": ip,
            "time": ts
        })

    return data


# -------------------------
# AUDIT STATS
# -------------------------

@app.get("/audit/stats")
def fetch_stats():

    return get_stats()
