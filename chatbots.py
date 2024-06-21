from enum import Enum
from typing import List, Dict, Any, Optional
from openai.types.chat import ChatCompletion
import openai


class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatBot:
    def __init__(self, model: str, system_prompt: str) -> None:
        self.model: str = model
        self.system_prompt: str = system_prompt
        self.conversation_history: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    def get_response(self, prompt: str) -> str:
        self.append_message(prompt, MessageType.USER)
        response: ChatCompletion = openai.chat.completions.create(
            model=self.model,
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
        super().__init__("gpt-4", system_prompt)
