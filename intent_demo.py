# intent_demo.py
import json
from llm_client import LLMClient

INTENT_PROMPT = """你是图表推荐专家。判断用户问句最适合的图表类型。

可选类型说明：
- bar：柱状图，适合"对比/统计/排行"（如：各品类销售额）
- line：折线图，适合"趋势/变化/走势"（如：近7天每天销售额）
- pie：饼图，适合"占比/比例/分布"（如：各品类销售额占比）
- table：表格，适合"明细/列表"（如：订单明细）

只输出 JSON：{{"chart_type": "bar|line|pie|table", "confidence": 0.0-1.0, "keywords": ["触发词"]}}

用户问句：{query}"""

TEST_CASES = [
    ("统计今天各个品类的销售额", "bar"),
    ("近7天每天的订单总额趋势", "line"),
    ("各分类商品销售额占比", "pie"),
    ("订单明细列表", "table"),
    ("哪个商品卖得最好", "bar"),
    ("用户增长趋势", "line"),
    ("各区域订单占比", "pie"),
    ("所有用户信息", "table"),
]

llm = LLMClient()
correct = 0
for query, expected in TEST_CASES:
    raw = llm.chat([{"role": "user", "content": INTENT_PROMPT.format(query=query)}],
                   json_mode=True)
    data = json.loads(raw)
    hit = data["chart_type"] == expected
    correct += hit
    print(f"{'✓' if hit else '✗'} 预测={data['chart_type']:5s} 期望={expected:5s} "
          f"置信度={data['confidence']} | {query}")

print(f"\n意图识别准确率：{correct}/{len(TEST_CASES)}")