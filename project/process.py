import json

import pandas as pd
from docx import Document

from chatbots import GPT4ChatBot, ChatBot
from docUtils import DocUtils as Du
from logfile import Logging as l


class Process:
    @staticmethod
    def produce_doc(gpt: ChatBot, plain_text_log: str, verbose: bool = False) -> tuple[Document, float]:
        json_string: str = gpt.get_json_response(plain_text_log)
        if verbose: print(f"\nJSON STRING: {json_string}")
        l.log_with_timestamp(f"\nJSON STRING: {json_string}")
        df: pd.DataFrame = Du.json_string_to_df(json_string)
        if verbose: print(f"\nDF: {df}"), l.log_with_timestamp(f"\nDF: {df}")
        hours: float = Du.get_total_hours(df)
        if verbose: print(f"\nHOURS: {hours}")
        l.log_with_timestamp(f"\nHOURS: {hours}")
        doc: Document = Du.df_to_doc(df)
        return doc, hours

    @staticmethod
    def process_entry(entry: json):
        with open("system_prompt_docwriter.txt", 'r') as file:
            docWriter: ChatBot = GPT4ChatBot(file.read())
        plain_text_log: str = f'The following log refers to the week beginning on Monday {entry["week"]}. {entry["description"]}'
        doc, hours = Process.produce_doc(docWriter, plain_text_log)
        filename = Du.save_doc(doc, entry["week"], hours)
        return {"filename": filename, "hours": hours}
