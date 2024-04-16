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


# Extending from database.py 
db_manager = DatabaseManager('url_database.db')

# Token and user for authentication purposes 
# (note: this will not work in production purposes, only for demo purposes)
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
        short_url_hash = hashlib.md5(original_url.encode('utf-8')).hexdigest()[:6]
        short_url = f'https://short.est/{short_url_hash}'
        db_manager.insert_url_pair(original_url, short_url)
    return jsonify(original_url=original_url, short_url=short_url)

# decode route, returns the original url if found otherwise returns error message
@app.route('/decode', methods=['POST'])
@auth.login_required
def decode():
    short_url = request.json['short_url']
    original_url = db_manager.get_old_url(short_url)
    if original_url:
        return jsonify(original_url=original_url)
    else:
        return jsonify(error="Short URL not found"), 404

if __name__ == '__main__':
    app.run(port=8000, debug=True)

'''
    In order to test for encoding:
        - Via terminal: 
            curl -X POST http://localhost:8000/encode -H "Content-Type: application/json" -H "Authorization: Bearer secret-token-1" -d '{"url":"http://example.com"}'

        - Via Postman:
            Use Post request, enter http://localhost:8000/encode
            In Authorization, put Bearer Token and enter "secret-token-1" as token
            In body enter the url in JSON format
    
    In order to test for Decoding:
        - Via terminal: 
            curl -X POST http://localhost:8000/decode -H "Content-Type: application/json" -H "Authorization: Bearer secret-token-1"  -d '{"short_url":"https://short.est/a9b9f0"}'

        - Via Postman:
            Use Post request, enter http://localhost:8000/decode
            In Authorization, put Bearer Token and enter "secret-token-1" as token
            In body enter the short_url in JSON format

'''