import sqlite3

def init_db():
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            usage INTEGER DEAFULT 0,
            plane TEXT DEFAULT 'free'
                   )""")
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("SELECT usage, plan FROM users WHERE user_id = ?",(user_id))
    user = cursor.fetchone()

    conn.close()
    return user

def create_user(user_id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (user_id) VALUES (?)",(user_id))
    conn.commit()
    conn.close()

def update_usage(user_id,usage):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET usage = ? WHERE user_id = ?",(usage, user_id))
    conn.commit()
    conn.close()
    

