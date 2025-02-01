from flask import Flask, jsonify, request, Response
from curl_cffi import requests
import random

import base64


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
]



app = Flask(__name__)

@app.route("/")
def check():
    return jsonify({"status": "I am on"})

@app.route("/ping")
def ping():
    return jsonify({"ping": "pong"})


@app.route("/proxy")
def proxy():
    image_url = request.args.get('url')
    
    if not image_url:
        return "Image URL parameter missing", 400
    
    try:
        # Randomly select a user agent
        headers = {
            'User-Agent': random.choice(user_agents)
        }
        response = requests.get(image_url, stream=True, headers=headers)
        if response.status_code == 200:
            headers = {'Content-Type': response.headers['Content-Type']}
            return Response(response.iter_content(chunk_size=8192), headers=headers)
        else:
            return "Can't fetch", response.status_code
    except Exception as e:
        return str(e), 500

@app.route("/image/transform")
def transform_img():
    ...

if __name__ == "__main__":
    app.run()