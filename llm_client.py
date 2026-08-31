# llm_client.py
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class LLMClient:
    """轻量 LLM 客户端：支持重试、超时、JSON 模式。"""

    def __init__(self, model="deepseek-chat", max_retries=2):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
            timeout=60,
        )
        self.model = model
        self.max_retries = max_retries

    def chat(self, messages, json_mode=False, temperature=0.7):
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    response_format={"type": "json_object"} if json_mode else None,
                )
                return resp.choices[0].message.content
            except Exception as e:
                print(f"第 {attempt + 1} 次调用失败: {e}")
                if attempt == self.max_retries:
                    raise
                time.sleep(2 ** attempt)  # 指数退避


if __name__ == "__main__":
    llm = LLMClient()
    print(llm.chat([{"role": "user", "content": "用JSON格式返回一句话说'你好'"}], json_mode=True))