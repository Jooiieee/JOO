import json
from llm_client import chat_json

TEST_GEN_PROMPT = """你是测试工程师。根据下面的功能需求，生成意图识别测试用例。
输出严格JSON数组：[{{"case": "用户问句", "expected": "bar/line/pie/table"}}]
需求：生成5条用户查询语句，用来测试图表类型分类模型。

需求：{requirement}
"""

req = "自然语言查询数据，模型输出bar/line/pie/table四种图表类型"
res = chat_json([{"role":"user","content":TEST_GEN_PROMPT.format(requirement=req)}])
cases = json.loads(res)
for item in cases:
    print(item)