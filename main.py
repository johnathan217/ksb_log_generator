from enum import Enum
from typing import List, Dict, Any, Optional

import openai
from test_string import test_string
from DocUtils import DocUtils
from chatbots import GPT4ChatBot, ChatBot


name: str = "Johnathan Phillips"


def main() -> None:
    u_input: str = input("> ")
    with open("system_prompt_docwriter.txt", 'r') as file:
        docwriter: GPT4ChatBot = GPT4ChatBot(file.read())

    Process.produce_doc(docwriter, u_input, "output.docx", True)
    # print(DocUtils.calculate_total_hours(test_string))


class Process:
    @staticmethod
    def produce_doc(gpt: ChatBot, prompt: str, output_path: str, verbose: bool = False) -> None:
        response: str = gpt.get_response(prompt)
        table_string: str = DocUtils.extract_table_content(response)
        hours: float = DocUtils.calculate_total_hours(table_string)
        if verbose:
            print(table_string)
            print(f"Hours: {hours}")
        DocUtils.string_to_doc(table_string, output_path)


if __name__ == "__main__":
    main()
