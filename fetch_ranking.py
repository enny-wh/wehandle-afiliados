import os
import json
import requests
from datetime import datetime, timezone
from collections import defaultdict

SYMPLA_TOKEN = os.environ["SYMPLA_TOKEN"]
EVENT_ID = os.environ["SYMPLA_EVENT_ID"]

BASE_URL = "https://api.sympla.com.br/public/v4"
HEADERS = {"s_token": SYMPLA_TOKEN}

def fetch_all_orders():
    orders = []
    page = 1
    page_size = 100
    while True:
        url = f"{BASE_URL}/events/{EVENT_ID}/orders?page={page}&page_size={page_size}"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("data", [])
        orders.extend(batch)
        pagination = data.get("pagination", {})
        if page >= pagination.get("total_page", 1):
            break
        page += 1
    return orders

def build_ranking(orders):
    coupon_stats = defaultdict(lambda: {"uses": 0, "names": set()})
    for order in orders:
        coupon = order.get("discount_name") or order.get("promo_code") or ""
        coupon = coupon.strip().upper()
        if not coupon:
            continue
        buyer = order.get("buyer_name", "")
        coupon_stats[coupon]["uses"] += 1
        if buyer:
            coupon_stats[coupon]["names"].add(buyer)

    ranking = []
    for code, stats in coupon_stats.items():
        ranking.append({
            "code": code,
            "uses": stats["uses"],
        })

    ranking.sort(key=lambda x: x["uses"], reverse=True)
    for i, item in enumerate(ranking):
        item["position"] = i + 1

    return ranking

def main():
    print("Buscando pedidos da Sympla...")
    orders = fetch_all_orders()
    print(f"Total de pedidos: {len(orders)}")

    ranking = build_ranking(orders)
    print(f"Cupons encontrados: {len(ranking)}")

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "event_id": EVENT_ID,
        "total_orders": len(orders),
        "ranking": ranking
    }

    os.makedirs("data", exist_ok=True)
    with open("data/ranking.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("Arquivo data/ranking.json atualizado com sucesso.")
    for item in ranking[:5]:
        print(f"  #{item['position']} {item['code']}: {item['uses']} usos")

if __name__ == "__main__":
    main()
