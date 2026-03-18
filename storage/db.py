import sqlite3
import os
from config.settings import DB_PATH

<<<<<<< HEAD
=======

>>>>>>> 05ab3fa (updated API logic)
def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

<<<<<<< HEAD
=======

>>>>>>> 05ab3fa (updated API logic)
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dns_events (
<<<<<<< HEAD
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ts          TEXT NOT NULL,
            src_ip      TEXT,
            dst_ip      TEXT,
            qname       TEXT,
            qtype       TEXT,
            base_domain TEXT,
            domain_length INTEGER,
            max_label_length INTEGER,
            entropy     REAL,
            score       INTEGER DEFAULT 0
        )
=======
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            ts               TEXT NOT NULL,
            src_ip           TEXT,
            dst_ip           TEXT,
            qname            TEXT,
            qtype            TEXT,
            base_domain      TEXT,
            domain_length    INTEGER,
            max_label_length INTEGER,
            entropy          REAL,
            score            INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
>>>>>>> 05ab3fa (updated API logic)
        CREATE TABLE IF NOT EXISTS alerts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ts          TEXT NOT NULL,
            src_ip      TEXT,
            base_domain TEXT,
            qname       TEXT,
            qtype       TEXT,
            score       INTEGER,
            reasons     TEXT
        )
<<<<<<< HEAD
=======
    """)

    conn.commit()
    conn.close()
>>>>>>> 05ab3fa (updated API logic)
