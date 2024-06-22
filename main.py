import os
from enum import Enum
from typing import List, Dict, Any, Optional

import openai
import pandas as pd
from docx import Document
from dotenv import load_dotenv

from DocUtils import DocUtils
from chatbots import GPT4ChatBot, ChatBot

load_dotenv()
name: str = "Johnathan Phillips"
openai.api_key = os.getenv('OPENAI_API_KEY')


def main() -> None:
    # u_input: str = input("> ")
    u_input = "on friday 7 june between 0900 and 1300 i had an information technology lecture on how technology solutions inform business processes."
    with open("system_prompt_docwriter.txt", 'r') as file:
        docwriter: GPT4ChatBot = GPT4ChatBot(file.read())

    Process.produce_doc(docwriter, u_input, "output2.docx", True)


class Process:
    @staticmethod
    def produce_doc(gpt: ChatBot, plain_text_log: str, output_path: str, verbose: bool = False) -> None:
        json_string: str = gpt.get_json_response(plain_text_log)
        if verbose: print(f"\nJSON STRING: {json_string}")
        df: pd.DataFrame = DocUtils.json_string_to_df(json_string)
        if verbose: print(f"\nDF: {df}")
        hours: float = DocUtils.get_total_hours(df)
        if verbose: print(f"\nHOURS: {hours}")
        doc: Document = DocUtils.df_to_doc(df)
        doc.save(output_path)


if __name__ == "__main__":
    main()
