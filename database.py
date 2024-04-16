'''
Author: Ekansh Gupta
Date Created: 4/15/2024
Date Modified: 4/15/2024
Purpose: Create a database to store the old_url and short_url
Version: 1.0
Change History: Initial
'''

import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    # Creating url_map table if it does not exist 
    def init_db(self):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS url_map (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        old_url TEXT NOT NULL,
                        short_url TEXT NOT NULL UNIQUE
                    );
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    # Inserting a new old_url and short_url pair into database
    def insert_url_pair(self, old_url, short_url):
        try:
            with self.get_connection() as conn:
                conn.execute('INSERT INTO url_map (old_url, short_url) VALUES (?, ?)', (old_url, short_url))
                conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    # Retreiving the old_url from the short_url
    def get_old_url(self, short_url):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT old_url FROM url_map WHERE short_url = ?', (short_url,))
                result = cursor.fetchone()
                if result:
                    return result['old_url'] 
                else:
                    return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # Retreiving short_url from old_url
    def get_short_url(self, old_url):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT short_url FROM url_map WHERE old_url = ?', (old_url,))
                result = cursor.fetchone()
                if result:
                    return result['short_url'] 
                else:
                    return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
