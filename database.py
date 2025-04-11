
import sqlite3
import os

DB_NAME = "records.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_name TEXT,
            interview_date TEXT,
            assessment_process TEXT,
            lessons_learned TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_record(school, date, process, lesson):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO records (school_name, interview_date, assessment_process, lessons_learned) VALUES (?, ?, ?, ?)',
              (school, date, process, lesson))
    record_id = c.lastrowid
    conn.commit()
    conn.close()
    return record_id

def get_all_records():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM records ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(id=row[0], school_name=row[1], interview_date=row[2], assessment_process=row[3], lessons_learned=row[4]) for row in rows]
