import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR,"user.db")
def init_db():
    conn = sqlite3.connect(DB_PATH,check_same_thread=False,timeout=10)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            usage INTEGER DEFAULT 0,
            plan TEXT DEFAULT 'free'
                   )""")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON users(user_id)")

    conn.commit()
    conn.close()

def get_user(user_id):
    try:
        conn = sqlite3.connect(DB_PATH,check_same_thread=False,timeout=10)
        cursor = conn.cursor()

        cursor.execute("SELECT usage, plan FROM users WHERE user_id = ?",(user_id,))
        user = cursor.fetchone()

        conn.close()
        return user 
    except Exception as e:
        print("DB ERROR",e)
        return e


def create_user(user_id):
    conn = sqlite3.connect(DB_PATH,check_same_thread=False,timeout=10)
    cursor = conn.cursor()

    cursor.execute("""INSERT OR IGNORE INTO users (user_id) VALUES (?)""",(user_id,))
    conn.commit()
    conn.close()

def update_usage(user_id,usage):
    conn = sqlite3.connect(DB_PATH,check_same_thread=False,timeout=10)
    cursor = conn.cursor()

    cursor.execute("""
            UPDATE users SET usage = ?
                   WHERE user_id = ?""", (usage,user_id))
    if cursor.rowcount == 0 :
        cursor.execute("""
             INSERT INTO users (user_id,usage)
                       VALUES(?, ?)""",(user_id,usage))
    conn.commit()
    conn.close()
    

