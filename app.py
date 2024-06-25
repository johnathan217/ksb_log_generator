import json
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai
from datetime import datetime, timedelta
from process import Process as P
from chatbots import ChatBot, GPT4ChatBot
from DocUtils import DocUtils

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
name = "Johnathan Phillips"

if not os.path.exists('logs'):
    os.makedirs('logs')
if not os.path.exists('outputs'):
    os.makedirs('outputs')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    P.log_with_timestamp(json.dumps(data, indent=2))
    with open("system_prompt_docwriter.txt", 'r') as file:
        docWriter: GPT4ChatBot = GPT4ChatBot(file.read())

    doc, hours = P.produce_doc(docWriter, data["entries"][0]["description"])
    fileName = DocUtils.create_filename(hours, name, data["entries"][0]["week"])
    DocUtils.save_doc(doc, fileName)

    return jsonify({
        "message": "Document created successfully",
        "filename": f"{fileName}"
    })


if __name__ == '__main__':
    app.run(debug=True)
