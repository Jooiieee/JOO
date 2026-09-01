# evaluate_intent.py
import json
from collections import defaultdict
from llm_client import LLMClient

# 构造数据集：每类 10 条（含正样本与易混淆的负样本）
DATASET = [
    # (问句, 期望类型)
    ("统计各品类销售额", "bar"), ("各分类商品数量对比", "bar"),
    ("销量最高的前5个商品", "bar"), ("各省份订单量排行", "bar"),
    ("近30天销售额变化", "line"), ("每日用户活跃度走势", "line"),
    ("订单量增长趋势", "line"), ("复购率随时间变化", "line"),
    ("各品类销售额占比", "pie"), ("订单状态分布", "pie"),
    ("各地区用户比例", "pie"), ("支付方式构成", "pie"),
    ("订单明细", "table"), ("所有商品列表", "table"),
    ("用户基本信息", "table"), ("评价内容列表", "table"),
]

INTENT_PROMPT = """你是图表推荐专家。判断用户问句最适合的图表类型。

可选类型说明：
- bar：柱状图，适合"对比/统计/排行"（如：各品类销售额）
- line：折线图，适合"趋势/变化/走势"（如：近7天每天销售额）
- pie：饼图，适合"占比/比例/分布"（如：各品类销售额占比）
- table：表格，适合"明细/列表"（如：订单明细）

只输出 JSON：{{"chart_type": "bar|line|pie|table", "confidence": 0.0-1.0, "keywords": ["触发词"]}}

用户问句：{query}"""

llm = LLMClient()
matrix = defaultdict(lambda: defaultdict(int))
correct = 0
for query, expected in DATASET:
    raw = llm.chat([{"role": "user", "content": INTENT_PROMPT.format(query=query)}],
                   json_mode=True)
    predicted = json.loads(raw)["chart_type"]
    matrix[expected][predicted] += 1
    correct += (predicted == expected)

print(f"准确率：{correct}/{len(DATASET)} = {correct / len(DATASET):.0%}")
print("\n混淆矩阵（行=期望，列=预测）：")
for row in ["bar", "line", "pie", "table"]:
    print(f"  {row:5s}", {k: v for k, v in matrix[row].items()})