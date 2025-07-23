import os, json, hmac, hashlib, requests
from aiohttp import web
from utils.config import load_config
from utils.wallet_client import send_stars

conf = load_config(".env")
PENDING = "data/pending.json"
ORDERS  = "data/orders.json"

def create_invoice(user_id: int, stars: int, price: int) -> str:
    url = "https://api.cryptocloud.plus/v1/invoice/create"
    headers = {
        "Authorization": f"Bearer {conf['CRYPTO_TOKEN']}",
        "Content-Type": "application/json"
    }
    order_id = f"{user_id}_{stars}_{int(os.times()[4])}"
    payload = {
        "project_id": conf["CRYPTO_PROJECT_ID"],
        "order_id": order_id,
        "currency": "RUB",
        "amount": price,
        "webhook_url": conf["WEBHOOK_URL"]
    }
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    result = r.json()["result"]
    inv_id = result["id"]
    pay_url = result["payment_url"]
    os.makedirs("data", exist_ok=True)
    pend = json.load(open(PENDING, encoding="utf-8")) if os.path.exists(PENDING) else {}
    pend[inv_id] = {"user_id": user_id, "stars": stars}
    json.dump(pend, open(PENDING, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return pay_url

async def crypto_webhook(request: web.Request):
    body = await request.text()
    sig = request.headers.get("X-Signature", "")
    expected = hmac.new(conf["CRYPTO_SECRET"].encode(), body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return web.Response(text="Bad signature", status=400)
    data = await request.json()
    inv_id = data.get("id")
    status = data.get("status")
    if status == "paid":
        pend = json.load(open(PENDING, encoding="utf-8"))
        info = pend.pop(inv_id, None)
        if info:
            await send_stars(to_user_id=info["user_id"], amount=info["stars"])
            orders = json.load(open(ORDERS, encoding="utf-8")) if os.path.exists(ORDERS) else []
            orders.append({"user_id": info["user_id"], "stars": info["stars"]})
            json.dump(orders, open(ORDERS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            json.dump(pend, open(PENDING, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return web.Response(text="OK")
