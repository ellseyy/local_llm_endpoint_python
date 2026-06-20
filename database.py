import sqlite3
from config import settings

def init_db():

    conn = sqlite3.connect(settings.sqlite_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            route TEXT,
            status TEXT,
            backend TEXT,
            model TEXT,
            latency_ms_total INTEGER,
            input_chars INTEGER,
            output_chars INTEGER,
            temperature REAL,
            max_tokens INTEGER,
            prompt_preview TEXT,
            response_preview TEXT,
            error_message TEXT
        )
    """)
    
    conn.commit()
    conn.close()