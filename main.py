from enum import Enum
from typing import List, Dict, Any, Optional

import openai
import pandas as pd
from docx import Document

from DocUtils import DocUtils
from chatbots import GPT4ChatBot, ChatBot

name: str = "Johnathan Phillips"


def main() -> None:
    u_input: str = input("> ")
    with open("system_prompt_docwriter.txt", 'r') as file:
        docwriter: GPT4ChatBot = GPT4ChatBot(file.read())

    Process.produce_doc(docwriter, u_input, "output2.docx", True)


class Process:
    @staticmethod
    def produce_doc(gpt: ChatBot, prompt: str, output_path: str, verbose: bool = False) -> None:
        response: str = gpt.get_response(prompt)
        df: pd.DataFrame = DocUtils.json_string_to_df(response)
        hours: float = DocUtils.get_total_hours(df)
        if verbose:
            print(response)
            print(f"Hours: {hours}")
        doc: Document = DocUtils.df_to_doc(df)
        doc.save(output_path)


if __name__ == "__main__":
    main()
