import concurrent.futures
import json
import os

import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from process import Process as p
from logfile import Logging as l
from config import Config

app = Flask(__name__)

load_dotenv()
openai.api_key = Config.openai_api_key

if not os.path.exists('../logs'):
    os.makedirs('../logs')
if not os.path.exists('../outputs'):
    os.makedirs('../outputs')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    l.log_with_timestamp(json.dumps(data, indent=2))

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_entry = {executor.submit(p.process_entry, entry): entry for entry in data["entries"]}
        for future in concurrent.futures.as_completed(future_to_entry):
            entry = future_to_entry[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'Entry {entry} generated an exception: {exc}')

    filenames = [result['filename'] for result in results]
    doc_str: str = "documents" if (len(results) > 1) else "document"
    return jsonify({
        "message": f"{len(results)} {doc_str} created successfully:",
        "filenames": filenames
    })


if __name__ == '__main__':
    app.run(debug=True)
