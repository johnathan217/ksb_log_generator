import json
import sys

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from DocUtils import DocUtils
from chatbots import GPT4ChatBot
import openai
from datetime import datetime, timedelta

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

    log_with_timestamp(json.dumps(data, indent=2))

    return jsonify({
        "message": "Document created successfully",
        "filename": "example_document.docx"
    })


def log_with_timestamp(message, file=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day = datetime.now().strftime("%Y-%m-%d")
    log_message = f"[{timestamp}] {message}"

    with open(f'logs/app_{day}.log', 'a') as f:
        f.write(log_message + "\n")


if __name__ == '__main__':
    app.run(debug=True)
