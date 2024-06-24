import json
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai
from datetime import datetime, timedelta
from process import Process as P

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
name = "Johnathan Phillips"

if not os.path.exists('logs'):
    os.makedirs('logs')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    P.log_with_timestamp(json.dumps(data, indent=2))

    return jsonify({
        "message": "Document created successfully",
        "filename": "example_document.docx"
    })




if __name__ == '__main__':
    app.run(debug=True)
