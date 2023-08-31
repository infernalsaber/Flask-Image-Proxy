from flask import Flask, jsonify, request, Response
# from PIL import Image
# import numpy as np
# import cv2
# import io
import requests

import base64

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
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            headers = {'Content-Type': response.headers['Content-Type']}
            return Response(response.iter_content(chunk_size=8192), headers=headers)
        else:
            return "Image not found", 404
    except Exception as e:
        return str(e), 500

@app.route("/image/transform")
def transform_img():
    ...

if __name__ == "__main__":
    app.run()