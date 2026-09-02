# hello_llm.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 中的 DEEPSEEK_API_KEY

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个简洁的助手，用一句话回答。"},
        {"role": "user", "content": "你好，请介绍一下你自己。"},
    ],
)
print(resp.choices[0].message.content)