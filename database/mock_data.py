# mock_data.py
import sqlite3, random, datetime

random.seed(42)  # 固定种子，保证每次数据一致（利于调试）
conn = sqlite3.connect("ecommerce.db")
cur = conn.cursor()

CATEGORIES = ["手机", "电脑", "家电", "配件"]
PRODUCTS = [("iPhone 15", 1, 5999.00, "128G"), ("小米14", 1, 3999.00, "256G"),
            ("MacBook Air", 2, 7999.00, "8G+256G"), ("联想小新", 2, 4999.00, "16G+512G"),
            ("海尔冰箱", 3, 2899.00, "双门"), ("戴森吸尘器", 3, 3299.00, "V12"),
            ("充电宝", 4, 99.00, "20000mAh"), ("蓝牙耳机", 4, 199.00, "降噪")]

PAYMENTS = ["微信", "支付宝", "银行卡"]

# 分类
for name in CATEGORIES:
    cur.execute("INSERT INTO categories(name) VALUES (?)", (name,))
# 商品
for name, cid, price, spec in PRODUCTS:
    cur.execute("INSERT INTO products(name, category_id, price, spec) VALUES (?,?,?,?)",
                (name, cid, price, spec))
# 用户
for i in range(1, 11):
    cur.execute("INSERT INTO users(username, email) VALUES (?,?)",
                (f"user{i:02d}", f"user{i:02d}@test.com"))
# 订单 + 明细（总额 = 明细求和，保证业务一致）
for i in range(1, 101):  # 100 个订单
    user_id = random.randint(1, 10)
    day = datetime.date(2026, 8, 1) + datetime.timedelta(days=random.randint(0, 29))
    cur.execute(
        "INSERT INTO orders(order_no, user_id, total_amount, status, payment_method, created_at) VALUES (?,?,0,?,?,?)",
        (f"SO{i:06d}", user_id, random.choice(["completed", "pending", "cancelled"]),
         random.choice(PAYMENTS), f"{day} 10:30:00"))
    order_id = cur.lastrowid
    # 每个订单 1~3 件商品
    total = 0
    for _ in range(random.randint(1, 3)):
        pid = random.randint(1, len(PRODUCTS))
        price = random.choice([x[2] for x in PRODUCTS])
        qty = random.randint(1, 3)
        cur.execute("INSERT INTO order_items(order_id, product_id, quantity, price) VALUES (?,?,?,?)",
                    (order_id, pid, qty, price))
        total += qty * price
    cur.execute("UPDATE orders SET total_amount=? WHERE id=?", (total, order_id))

conn.commit()
print("Mock 数据插入完成：4 分类 / 8 商品 / 10 用户 / 100 订单")
conn.close()
