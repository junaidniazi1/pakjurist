import sqlite3
from datetime import datetime
import json
import os

class Database:
    """Handles all database operations for chat sessions"""
    
    DB_NAME = "chat_sessions.db"
    
    def __init__(self):
        """Initialize database and create tables"""
        self.create_tables()
    
    def get_connection(self):
        """Create and return a database connection"""
        return sqlite3.connect(self.DB_NAME)
    
    def create_tables(self):
        """Create Sessions and Messages tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Sessions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TIMESTAMP,
                    last_activity TIMESTAMP
                )
            """)
            
            # Messages Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT CHECK(role IN ('user', 'assistant')),
                    content TEXT,
                    timestamp TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)
            
            conn.commit()
    
    def create_session_if_not_exists(self, session_id: str):
        """Create a new session if it doesn't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                INSERT OR IGNORE INTO sessions (session_id, created_at, last_activity)
                VALUES (?, ?, ?)
            """, (session_id, now, now))
            
            conn.commit()
    
    def save_message(self, session_id: str, role: str, content: str, metadata: dict = None):
        """Save a message to the database"""
        # Ensure session exists first
        self.create_session_if_not_exists(session_id)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            metadata_json = json.dumps(metadata) if metadata else None
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Insert message
            cursor.execute("""
                INSERT INTO messages (session_id, role, content, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, role, content, now, metadata_json))
            
            # Update session last activity
            cursor.execute("""
                UPDATE sessions 
                SET last_activity = ? 
                WHERE session_id = ?
            """, (now, session_id))
            
            conn.commit()
    
    def get_conversation_history(self, session_id: str, limit: int = 50):
        """Get conversation history for a session"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT role, content, timestamp 
                FROM messages 
                WHERE session_id = ? 
                ORDER BY timestamp ASC 
                LIMIT ?
            """, (session_id, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def clear_session(self, session_id: str):
        """Clear all messages for a session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            conn.commit()
    
    def delete_session(self, session_id: str):
        """Delete a session and all its messages"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Delete messages first
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            
            # Delete session
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            
            conn.commit()
    
    def get_session_stats(self, session_id: str):
        """Get statistics for a session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN role = 'user' THEN 1 ELSE 0 END) as user_count,
                    SUM(CASE WHEN role = 'assistant' THEN 1 ELSE 0 END) as assistant_count
                FROM messages 
                WHERE session_id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            
            if row and row[0] > 0:
                return {
                    'total_messages': row[0],
                    'user_messages': row[1],
                    'assistant_messages': row[2]
                }
            
            return {
                'total_messages': 0,
                'user_messages': 0,
                'assistant_messages': 0
            }
    
    def get_all_sessions(self, limit: int = 10):
        """Get all sessions ordered by last activity"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, created_at, last_activity
                FROM sessions
                ORDER BY last_activity DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_message_count(self, session_id: str):
        """Get total message count for a session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM messages 
                WHERE session_id = ?
            """, (session_id,))
            
            return cursor.fetchone()[0]
    
    def search_messages(self, session_id: str, search_term: str):
        """Search messages in a session"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT role, content, timestamp
                FROM messages
                WHERE session_id = ? AND content LIKE ?
                ORDER BY timestamp ASC
            """, (session_id, f'%{search_term}%'))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

# Initialize database when module is imported
if __name__ == "__main__":
    db = Database()
    print("✅ Database initialized successfully.")
    print(f"📊 Database location: {os.path.abspath(Database.DB_NAME)}")