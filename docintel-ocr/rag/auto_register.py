import sys
import sqlite3


DB = "documents.db"


def register(doc):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO documents
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        doc["trial_id"],
        doc["doc_type"],
        doc["version"],
        doc["effective_date"],
        doc["supersedes"],
        doc["status"],
        doc["blob_path"]
    ))

    conn.commit()
    conn.close()


def auto_register(filename):

    # TEMP DEFAULTS (you can improve later)
    doc = {
        "trial_id": "TRIAL_001",
        "doc_type": "protocol",
        "version": "v1.0",
        "effective_date": "2024-01-01",
        "supersedes": None,
        "status": "approved",
        "blob_path": filename
    }

    register(doc)

    print("Registered:", filename)


if __name__ == "__main__":

    fname = sys.argv[1]

    auto_register(fname)
