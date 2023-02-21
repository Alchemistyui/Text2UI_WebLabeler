'''
Author: Alchemistyui
Date: 2023-02-20
LastEditTime: 2023-02-21
FilePath: /Text2UI_WebLabeler/server/server.py
Description: 

Copyright (c) 2023, All Rights Reserved. 
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/submit', methods=['POST'])
def submit_form():
    print(request)
    print(request.get_json())
    data = json.dumps(request.get_json())
    with open("/Users/Alchemist/Downloads/Text2UI/web_labeler.jsonl","a") as f:
        f.write(str(data))
        f.write("\n")
        return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
