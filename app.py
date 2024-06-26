import json
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai
from datetime import datetime
from process import Process as P
from chatbots import GPT4ChatBot
from DocUtils import DocUtils
import concurrent.futures

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


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

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_entry = {executor.submit(P.process_entry, entry): entry for entry in data["entries"]}
        for future in concurrent.futures.as_completed(future_to_entry):
            entry = future_to_entry[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'Entry {entry} generated an exception: {exc}')

    return jsonify({
        "message": "Documents created successfully",
        "results": results
    })


if __name__ == '__main__':
    app.run(debug=True)
