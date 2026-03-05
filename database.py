import sqlite3
import json
from datetime import datetime

DB_NAME = "resume_analyzer.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            job_description TEXT NOT NULL,
            final_score REAL NOT NULL,
            similarity_score REAL NOT NULL,
            keyword_match_ratio REAL NOT NULL,
            matched_keywords TEXT NOT NULL,
            missing_keywords TEXT NOT NULL,
            suggestions TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_analysis(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analyses (
            filename, job_description, final_score,
            similarity_score, keyword_match_ratio,
            matched_keywords, missing_keywords,
            suggestions, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["filename"],
        data["job_description"],
        data["final_score"],
        data["similarity_score"],
        data["keyword_match_ratio"],
        json.dumps(data["matched_keywords"]),
        json.dumps(data["missing_keywords"]),
        json.dumps(data["suggestions"]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_all_analyses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analyses ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    analyses = []
    for row in rows:
        analyses.append({
            "id": row[0],
            "filename": row[1],
            "job_description": row[2],
            "final_score": row[3],
            "similarity_score": row[4],
            "keyword_match_ratio": row[5],
            "matched_keywords": json.loads(row[6]),
            "missing_keywords": json.loads(row[7]),
            "suggestions": json.loads(row[8]),
            "created_at": row[9]
        })
    return analyses

def get_analysis_by_id(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analyses WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "filename": row[1],
            "job_description": row[2],
            "final_score": row[3],
            "similarity_score": row[4],
            "keyword_match_ratio": row[5],
            "matched_keywords": json.loads(row[6]),
            "missing_keywords": json.loads(row[7]),
            "suggestions": json.loads(row[8]),
            "created_at": row[9],
            "total_jd_keywords": len(json.loads(row[7])) + len(json.loads(row[6])),
            "total_matched": len(json.loads(row[6]))
        }
    return None

def delete_analysis(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (id,))
    conn.commit()
    conn.close()