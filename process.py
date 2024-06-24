import datetime
from enum import Enum
from typing import List, Dict, Any, Optional

import pandas as pd
from docx import Document
from DocUtils import DocUtils as Du
from chatbots import GPT4ChatBot, ChatBot


class Process:
    @staticmethod
    def produce_doc(gpt: ChatBot, plain_text_log: str, output_path: str, verbose: bool = False) -> None:
        json_string: str = gpt.get_json_response(plain_text_log)
        if verbose: print(f"\nJSON STRING: {json_string}")
        Process.log_with_timestamp(f"\nJSON STRING: {json_string}")
        df: pd.DataFrame = Du.json_string_to_df(json_string)
        if verbose: print(f"\nDF: {df}"), Process.log_with_timestamp(f"\nDF: {df}")
        hours: float = Du.get_total_hours(df)
        if verbose: print(f"\nHOURS: {hours}")
        Process.log_with_timestamp(f"\nHOURS: {hours}")
        doc: Document = Du.df_to_doc(df)
        doc.save(output_path)

    @staticmethod
    def process_submit(json, ):
        for entries in json["entries"]:
            Du.create_filename()

    @staticmethod
    def log_with_timestamp(message, file=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day = datetime.now().strftime("%Y-%m-%d")
        log_message = f"[{timestamp}] {message}"

        with open(f'logs/app_{day}.log', 'a') as f:
            f.write(log_message + "\n")


