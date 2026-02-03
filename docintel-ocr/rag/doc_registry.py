import sqlite3


DB = "documents.db"


def init_db():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        trial_id TEXT,
        doc_type TEXT,
        version TEXT,

        effective_date TEXT,
        supersedes TEXT,

        status TEXT,

        blob_path TEXT PRIMARY KEY
    )
    """)

    conn.commit()
    conn.close()

    print("Document registry initialized ✅")


if __name__ == "__main__":
    init_db()
