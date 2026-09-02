# zero_vs_few.py
import json
from llm_client import LLMClient

llm = LLMClient()

# ---------- Zero-Shot：一个示例都不给 ----------
ZERO_SHOT = """你是图表推荐专家。判断用户问句最适合的图表类型。
可选类型：bar(柱状图)、line(折线图)、pie(饼图)、table(表格)。
只输出 JSON：{{"chart_type": "bar", "confidence": 0.9}}

用户问句：{query}"""

# ---------- Few-Shot：每类给 1 个示例 ----------
FEW_SHOT = """你是图表推荐专家。判断用户问句最适合的图表类型。

示例：
"统计各品类销售额" → {{"chart_type": "bar", "confidence": 0.95}}
"近7天销售趋势"   → {{"chart_type": "line", "confidence": 0.95}}
"各品类销售额占比" → {{"chart_type": "pie", "confidence": 0.95}}
"订单明细列表"     → {{"chart_type": "table", "confidence": 0.95}}

现在判断下面的问句，只输出 JSON：{{"chart_type": "...", "confidence": 0.95}}
用户问句：{query}"""

TEST_QUERIES = [
    "各个分类的商品数量对比",
    "过去一个月每天的下单量变化",
    "不同支付方式的使用占比",
    "全部商品的基本信息",
]

def run(prompt_template):
    results = []
    for q in TEST_QUERIES:
        raw = llm.chat([{"role": "user", "content": prompt_template.format(query=q)}],
                       json_mode=True)
        results.append((q, json.loads(raw)["chart_type"]))
    return results

zero = run(ZERO_SHOT)
few = run(FEW_SHOT)

print(f"{'问句':<24} {'Zero-Shot':<10} {'Few-Shot':<10}")
for (q, z), (_, f) in zip(zero, few):
    print(f"{q:<24} {z:<10} {f:<10} {'✓ 一致' if z == f else '✗ 不一致'}")