from enum import Enum
from typing import List, Dict, Any, Optional
from openai.types.chat import ChatCompletion
import openai


class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class OpenAIChatModels(Enum):
    GPT4o = "gpt-4o"
    GPT4TURBO = "gpt-4-turbo"
    GPT4 = "gpt-4"
    GPT35TURBO = "gpt-3.5-turbo"


class ChatBot:
    def __init__(self, model: OpenAIChatModels, system_prompt: str) -> None:
        self.model: OpenAIChatModels = model
        self.system_prompt: str = system_prompt
        self.conversation_history: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    def get_response(self, prompt: str) -> str:
        self.append_message(prompt, MessageType.USER)
        response: ChatCompletion = openai.chat.completions.create(
            model=self.model.value,
            messages=self.conversation_history
        )
        reply: Optional[str] = response.choices[0].message.content
        if reply is None:
            raise ValueError("Received empty response from OpenAI API")
        return reply

    def get_json_response(self, prompt: str) -> str:
        self.append_message(prompt, MessageType.USER)
        response: ChatCompletion = openai.chat.completions.create(
            model=self.model.value,
            response_format={"type": "json_object"},
            messages=self.conversation_history
        )
        reply: Optional[str] = response.choices[0].message.content
        if reply is None:
            raise ValueError("Received empty response from OpenAI API")
        return reply

    def append_message(self, content: str, message_type: MessageType) -> None:
        self.conversation_history.append({"role": message_type.value, "content": content})


class GPT4ChatBot(ChatBot):
    def __init__(self, system_prompt: str) -> None:
        super().__init__(OpenAIChatModels.GPT4TURBO, system_prompt)
