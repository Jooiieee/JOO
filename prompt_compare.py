# prompt_compare.py
import json
from llm_client import LLMClient

llm = LLMClient()
query = "统计今天各个品类的销售额"

# ① 弱约束：什么都不限定
weak = llm.chat([{"role": "user", "content": f"用户问：{query}。你觉得应该用哪种图？"}])

# ② 强约束：角色 + 指令 + 格式 + JSON Mode
STRONG = """你是图表推荐专家。判断用户问句最适合的图表类型。
可选类型：bar(柱状图)、line(折线图)、pie(饼图)、table(表格)。
只输出 JSON：{{"chart_type": "bar", "confidence": 0.9, "keywords": []}}

用户问句：{query}"""
strong = llm.chat(
    [{"role": "user", "content": STRONG.format(query=query)}], json_mode=True
)

print("弱约束输出：", weak)
print("强约束输出：", strong)
print("可解析为 JSON：", isinstance(json.loads(strong), dict))