import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)
MODEL = os.getenv("LLM_MODEL")

def chat(messages, temperature=0.3):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature
    )
    return resp.choices[0].message.content

def chat_json(messages, temperature=0.0):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        response_format={"type":"json_object"}
    )
    return resp.choices[0].message.content


class LLMClient:
    """面向 Demo 的封装：llm.chat(messages, json_mode=True)"""

    def __init__(self, model=None):
        self.model = model or MODEL

    def chat(self, messages, temperature=0.3, json_mode=False):
        if json_mode:
            return chat_json(messages, temperature=temperature)
        return chat(messages, temperature=temperature)

    def chat_json(self, messages, temperature=0.0):
        return chat_json(messages, temperature=temperature)