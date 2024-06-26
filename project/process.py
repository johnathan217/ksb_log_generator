import json
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import os
import pandas as pd
from docx import Document
from docUtils import DocUtils as Du
from chatbots import GPT4ChatBot, ChatBot


class Process:
    name = os.getenv('NAME')
    @staticmethod
    def produce_doc(gpt: ChatBot, plain_text_log: str, verbose: bool = False) -> tuple[Document, float]:
        json_string: str = gpt.get_json_response(plain_text_log)
        if verbose: print(f"\nJSON STRING: {json_string}")
        Process.log_with_timestamp(f"\nJSON STRING: {json_string}")
        df: pd.DataFrame = Du.json_string_to_df(json_string)
        if verbose: print(f"\nDF: {df}"), Process.log_with_timestamp(f"\nDF: {df}")
        hours: float = Du.get_total_hours(df)
        if verbose: print(f"\nHOURS: {hours}")
        Process.log_with_timestamp(f"\nHOURS: {hours}")
        doc: Document = Du.df_to_doc(df)
        return doc, hours

    @staticmethod
    def log_with_timestamp(message: str):
        timestamp: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        day: str = datetime.now().strftime("%d-%m-%Y")
        log_message: str = f"[{timestamp}] {message}"

        with open(f'../logs/app_{day}.log', 'a') as f:
            f.write(log_message + "\n")

    @staticmethod
    def process_entry(entry: json):
        with open("system_prompt_docwriter.txt", 'r') as file:
            docWriter: ChatBot = GPT4ChatBot(file.read())
        plain_text_log: str = f'The following log refers to the week {entry["week"]}. {entry["description"]}'
        doc, hours = Process.produce_doc(docWriter, plain_text_log)
        fileName = Du.create_filename(hours, Process.name, entry["week"])
        Du.save_doc(doc, fileName)
        return {"filename": fileName, "hours": hours}
