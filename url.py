'''
Author: Ekansh Gupta
Date Created: 4/15/2024
Date Modified: 4/15/2024
Purpose: Create the encode/decode routes and make sure user is authenticated
Version: 1.0
Change History: Initial
'''

from database import DatabaseManager
from flask import Flask, request, jsonify
import hashlib
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

# Create authentication
auth = HTTPTokenAuth(scheme='Bearer')


# From database.py 
db_manager = DatabaseManager('url_database.db')

# Token and user for authentication purposes 
# (note: this will not work in production purposes only for demo purposes)
tokens = {
    "secret-token-1": "user1"
}

# Verifying to see if token exists and returning user 
@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    return None

# encode route, returns a json with original_url and new short_url
@app.route('/encode', methods=['POST'])
@auth.login_required
def encode():
    original_url = request.json['url']
    short_url = db_manager.get_short_url(original_url)
    if not short_url:
        short_url = hashlib.md5(original_url.encode('utf-8')).hexdigest()[:6]
        db_manager.insert_url_pair(original_url, short_url)
    return jsonify(original_url=original_url, short_url=f'https://short.est/{short_url}')

# decode route, returns the original url if found otherwise returns error message
@app.route('/decode', methods=['POST'])
@auth.login_required
def decode():
    short_url = request.json['short_url'].split('/')[-1]
    original_url = db_manager.get_old_url(short_url)
    if original_url:
        return jsonify(original_url=original_url)
    else:
        return jsonify(error="Short URL not found"), 404

if __name__ == '__main__':
    app.run(port=8000, debug=True)
