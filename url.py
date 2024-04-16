from flask import Flask, request, jsonify
#from flask_cors import CORS
import sqlite3
import hashlib

app = Flask(__name__)
#CORS(app)

DATABASE = 'url_database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_url_pair(old_url, short_url):
    conn = get_db_connection()
    conn.execute('INSERT INTO url_map (old_url, short_url) VALUES (?, ?)', (old_url, short_url))
    conn.commit()
    conn.close()

def get_old_url(short_url):
    conn = get_db_connection()
    url_data = conn.execute('SELECT old_url FROM url_map WHERE short_url = ?', (short_url,)).fetchone()
    conn.close()
    return url_data

def get_short_url(old_url):
    conn = get_db_connection()
    url_data = conn.execute('SELECT short_url FROM url_map WHERE old_url = ?', (old_url,)).fetchone()
    conn.close()
    return url_data

def generate_short_url(url):
    hasher = hashlib.md5()
    hasher.update(url.encode('utf-8'))
    return hasher.hexdigest()[:6]

@app.route('/encode', methods=['POST'])
def encode():
    original_url = request.json['url']
    existing_short_url = get_short_url(original_url)
    if existing_short_url:
        short_url = existing_short_url['short_url']
    else:
        short_url = generate_short_url(original_url)
        insert_url_pair(original_url, short_url)
    return jsonify(original_url=original_url, short_url=f'https://short.est/{short_url}')

@app.route('/decode', methods=['POST'])
def decode():
    short_url = request.json['short_url'].split('/')[-1]
    url_data = get_old_url(short_url)
    if url_data:
        return jsonify(original_url=url_data['old_url'])
    else:
        return jsonify(error="Short URL not found"), 404

if __name__ == '__main__':
    app.run(port=8000, debug=True)
