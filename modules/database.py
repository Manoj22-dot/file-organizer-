"""
modules/database.py
Database initialization, models, and all DB operations using SQLite.
"""

import sqlite3
import os
from datetime import datetime
from flask import g


def get_db(app):
    """Get database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """Create all tables if they don't exist."""
    db_path = app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Files table - stores every processed file
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            original_name   TEXT NOT NULL,
            original_path   TEXT,
            organized_path  TEXT,
            file_size   INTEGER DEFAULT 0,
            file_type   TEXT,
            category    TEXT,
            mime_type   TEXT,
            checksum    TEXT,
            status      TEXT DEFAULT 'pending',
            created_at  TEXT DEFAULT (datetime('now')),
            updated_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    # History table - full audit trail of every action
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            action      TEXT NOT NULL,
            file_id     INTEGER,
            file_name   TEXT,
            source_path TEXT,
            dest_path   TEXT,
            category    TEXT,
            details     TEXT,
            status      TEXT DEFAULT 'success',
            timestamp   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (file_id) REFERENCES files(id)
        )
    """)

    # Stats table - aggregated statistics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            date            TEXT DEFAULT (date('now')),
            files_organized INTEGER DEFAULT 0,
            files_failed    INTEGER DEFAULT 0,
            bytes_processed INTEGER DEFAULT 0,
            categories_used TEXT
        )
    """)

    # Settings table - user preferences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key     TEXT PRIMARY KEY,
            value   TEXT,
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Insert default settings
    defaults = [
        ('duplicate_handling', 'rename'),
        ('organize_by', 'type'),
        ('auto_organize', 'false'),
        ('watch_folder', ''),
    ]
    for key, value in defaults:
        cursor.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {db_path}")


# ── CRUD helpers ──────────────────────────────────────────────────────────────

def insert_file(db_path, original_name, original_path, file_size, file_type,
                category, mime_type, checksum):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO files (original_name, original_path, file_size, file_type,
                           category, mime_type, checksum, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'processing')
    """, (original_name, original_path, file_size, file_type, category,
          mime_type, checksum))
    file_id = cur.lastrowid
    conn.commit()
    conn.close()
    return file_id


def update_file_organized(db_path, file_id, organized_path, status='organized'):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        UPDATE files SET organized_path=?, status=?, updated_at=datetime('now')
        WHERE id=?
    """, (organized_path, status, file_id))
    conn.commit()
    conn.close()


def insert_history(db_path, action, file_id, file_name, source_path,
                   dest_path, category, details, status='success'):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO history (action, file_id, file_name, source_path,
                             dest_path, category, details, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (action, file_id, file_name, source_path, dest_path,
          category, details, status))
    conn.commit()
    conn.close()


def get_all_files(db_path, limit=100, offset=0, category=None, status=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = "SELECT * FROM files WHERE 1=1"
    params = []
    if category:
        query += " AND category=?"
        params.append(category)
    if status:
        query += " AND status=?"
        params.append(status)
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params += [limit, offset]
    rows = cur.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_history(db_path, limit=200):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM history ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dashboard_stats(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    total = cur.execute("SELECT COUNT(*) as c FROM files").fetchone()['c']
    organized = cur.execute(
        "SELECT COUNT(*) as c FROM files WHERE status='organized'"
    ).fetchone()['c']
    total_size = cur.execute(
        "SELECT COALESCE(SUM(file_size),0) as s FROM files"
    ).fetchone()['s']
    categories = cur.execute(
        "SELECT category, COUNT(*) as cnt FROM files GROUP BY category ORDER BY cnt DESC"
    ).fetchall()
    recent = cur.execute(
        "SELECT * FROM history ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()

    conn.close()
    return {
        'total_files': total,
        'organized_files': organized,
        'total_size_bytes': total_size,
        'categories': [dict(r) for r in categories],
        'recent_activity': [dict(r) for r in recent],
    }


def get_setting(db_path, key, default=None):
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT value FROM settings WHERE key=?", (key,)
    ).fetchone()
    conn.close()
    return row[0] if row else default


def set_setting(db_path, key, value):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, datetime('now'))",
        (key, value)
    )
    conn.commit()
    conn.close()
