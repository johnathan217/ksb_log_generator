import os


class Config:
    testing: bool = True
    name = os.getenv('NAME')
    openai_api_key = os.getenv('OPENAI_API_KEY')
