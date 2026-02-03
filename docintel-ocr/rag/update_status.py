import sqlite3
import sys


DB = "documents.db"


def update_status(blob, status, version=None, supersedes=None):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    if version:
        cur.execute("""
        UPDATE documents
        SET status=?, version=?, supersedes=?
        WHERE blob_path=?
        """, (status, version, supersedes, blob))

    else:
        cur.execute("""
        UPDATE documents
        SET status=?
        WHERE blob_path=?
        """, (status, blob))


    conn.commit()
    conn.close()

    print("Updated:", blob, "→", status)


if __name__ == "__main__":

    # Usage:
    # python update_status.py "Article 019.pdf" approved v2.0 v1.0

    blob = sys.argv[1]
    status = sys.argv[2]

    version = None
    supersedes = None

    if len(sys.argv) > 3:
        version = sys.argv[3]

    if len(sys.argv) > 4:
        supersedes = sys.argv[4]


    update_status(blob, status, version, supersedes)
