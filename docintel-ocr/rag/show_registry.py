import sqlite3


DB = "documents.db"


conn = sqlite3.connect(DB)
cur = conn.cursor()

rows = cur.execute("""
SELECT trial_id, doc_type, version, status, blob_path
FROM documents
ORDER BY trial_id, doc_type, version
""").fetchall()


print("\nDOCUMENT REGISTRY\n")

for r in rows:
    print(r)

conn.close()
