import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS url_map (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            old_url TEXT NOT NULL,
            short_url TEXT NOT NULL UNIQUE
        );
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_file = 'url_database.db'
    create_connection(db_file)
    create_table(db_file)