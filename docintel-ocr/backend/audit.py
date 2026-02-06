import sqlite3
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "audit_logs.db")


def init_db():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        message TEXT,
        user TEXT,
        ip TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_event(event_type, message, user="system", ip="127.0.0.1"):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO audit_logs
    (event_type, message, user, ip, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        event_type,
        message,
        user,
        ip,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def get_logs(limit=50):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    rows = cur.execute("""
    SELECT event_type, message, user, ip, timestamp
    FROM audit_logs
    ORDER BY id DESC
    LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return rows


def get_stats():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    total = cur.execute("SELECT COUNT(*) FROM audit_logs").fetchone()[0]
    docs = cur.execute("SELECT COUNT(*) FROM audit_logs WHERE event_type='upload'").fetchone()[0]
    ai = cur.execute("SELECT COUNT(*) FROM audit_logs WHERE event_type='ai'").fetchone()[0]
    alerts = cur.execute("SELECT COUNT(*) FROM audit_logs WHERE event_type='security'").fetchone()[0]

    conn.close()

    return {
        "total": total,
        "documents": docs,
        "ai": ai,
        "alerts": alerts
    }

def get_recent_uploads(limit=5):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    rows = cur.execute("""
    SELECT message, timestamp
    FROM audit_logs
    WHERE event_type = 'upload'
    ORDER BY id DESC
    LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return rows
