import os


class Config:
    testing: bool = False
    name = os.getenv('NAME')
    openai_api_key = os.getenv('OPENAI_API_KEY')
