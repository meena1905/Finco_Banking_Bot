import sqlite3
from datetime import datetime


# Initialize the database
def init_db():
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        complaint TEXT,
        category TEXT,
        priority TEXT,
        ticket_id TEXT,
        ai_reply TEXT,
        employee_reply TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()


# Save a new complaint
def save_complaint(name, complaint, category, priority, ticket_id, ai_reply):
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO complaints 
    (name, complaint, category, priority, ticket_id, ai_reply)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, complaint, category, priority, ticket_id, ai_reply))
    
    conn.commit()
    conn.close()


# Get all pending complaints
def get_pending_complaints():
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM complaints WHERE status='Pending'")
    rows = cursor.fetchall()
    conn.close()
    
    complaints = []
    for r in rows:
        complaints.append({
            "id": r[0],
            "name": r[1],
            "complaint": r[2],
            "category": r[3],
            "priority": r[4],
            "ticket_id": r[5],
            "ai_reply": r[6],
            "employee_reply": r[7],
            "status": r[8],
            "created_at": r[9]
        })
    return complaints


# Add employee reply and mark complaint resolved
def add_employee_reply(ticket_id, reply):
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE complaints
    SET employee_reply = ?, status = 'Resolved'
    WHERE ticket_id = ?
    """, (reply, ticket_id))

    conn.commit()
    conn.close()