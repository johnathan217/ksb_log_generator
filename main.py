import os
from enum import Enum
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

import openai
import pandas as pd
from docx import Document

from DocUtils import DocUtils
from chatbots import GPT4ChatBot, ChatBot

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
name: str = "Johnathan Phillips"


def main() -> None:
    # u_input: str = input("> ")
    u_input = "on monday 7 june between 0900 and 1300 i had an information technology lecture on how technology solutions inform business processes."
    with open("system_prompt_docwriter.txt", 'r') as file:
        docwriter: GPT4ChatBot = GPT4ChatBot(file.read())

    Process.produce_doc(docwriter, u_input, "output2.docx", True)


class Process:
    @staticmethod
    def produce_doc(gpt: ChatBot, plain_text_log: str, output_path: str, verbose: bool = False) -> None:
        json_string_response: str = gpt.get_response(plain_text_log)
        df: pd.DataFrame = DocUtils.json_string_to_df(json_string_response)
        hours: float = DocUtils.get_total_hours(df)
        if verbose:
            print(json_string_response)
            print(f"Hours: {hours}")
        doc: Document = DocUtils.df_to_doc(df)
        doc.save(output_path)


if __name__ == "__main__":
    main()
