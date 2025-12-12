from flask import Flask, jsonify
import asyncio
import aiohttp
import time
from datetime import datetime, timezone, timedelta
import os

app = Flask(__name__)


group_accounts = [
{
    "4332665848": "AMIN_X-WYVBECRZA-FLASH",
    "4332666031": "AMIN_X-WXTTCTJGX-FLASH",
    "4332666183": "AMIN_X-T6LSCLZ4G-FLASH",
    "4332667449": "AMIN_X-3Z3DB3LDF-FLASH",
    "4332676345": "AMIN_X-KYCYVD1YP-FLASH",
    "4332676487": "AMIN_X-BZYNYNNQH-FLASH",
    "4332676618": "AMIN_X-M4TAJ4X57-FLASH",
    "4332676785": "AMIN_X-LZYUOWB3P-FLASH",
    "4332676928": "AMIN_X-WQ5TPE08L-FLASH",
    "4332677091": "AMIN_X-XCRX7HXDV-FLASH",
    "4332677242": "AMIN_X-DXVJASXV5-FLASH",
    "4332677368": "AMIN_X-4XNQQTNAP-FLASH",
    "4332677554": "AMIN_X-BGSPROZZM-FLASH",
    "4332677692": "AMIN_X-SHGNAOX6Y-FLASH",
    "4332677833": "AMIN_X-WPZXYA8LA-FLASH",
    "4332677963": "AMIN_X-QLV8ER0GX-FLASH",
    "4332678102": "AMIN_X-QHDZLHALG-FLASH",
    "4332678235": "AMIN_X-GIVY93C5I-FLASH",
    "4332678382": "AMIN_X-Z4ZGMPAVA-FLASH",
    "4332678514": "AMIN_X-XQVF1AHMG-FLASH",
    "4332678633": "AMIN_X-6W0XCX7AY-FLASH",
    "4332678760": "AMIN_X-NGQ1PCBDH-FLASH",
    "4332678910": "AMIN_X-ONEISETHX-FLASH",
    "4332679689": "AMIN_X-L9FVCIO8T-FLASH",
    "4332679932": "AMIN_X-AKIUERZI5-FLASH",
    "4332680442": "AMIN_X-N4HAFABXU-FLASH",
    "4332680558": "AMIN_X-AVOJJCFDM-FLASH",
    "4332680726": "AMIN_X-2P7IQXRT5-FLASH",
    "4332680887": "AMIN_X-TZIG8ASKJ-FLASH",
    "4332681041": "AMIN_X-EDMLVAU6U-FLASH",
    "4332681182": "AMIN_X-LKZEJWAQN-FLASH",
    "4332681326": "AMIN_X-JTUCI7UXM-FLASH",
    "4332681453": "AMIN_X-FJOMSZK0D-FLASH",
    "4332681662": "AMIN_X-59IDVGQNM-FLASH",
    "4332681824": "AMIN_X-SCB02LCDC-FLASH",
    "4332681988": "AMIN_X-USIPORYTY-FLASH",
    "4332682145": "AMIN_X-DFCQ0RLWT-FLASH",
    "4332682264": "AMIN_X-GFH0TA5WC-FLASH",
    "4332682833": "AMIN_X-S3CAGAKQC-FLASH",
    "4332723425": "AMIN_X-AKKTNGCZ7-FLASH",
    "4332723566": "AMIN_X-UW74QIMRH-FLASH",
    "4332723655": "AMIN_X-UFFQFSH8Z-FLASH",
    "4332723738": "AMIN_X-8K6XXUTTC-FLASH",
    "4332723841": "AMIN_X-KXMV5VVCB-FLASH",
    "4332724046": "AMIN_X-TCQWREJ5Y-FLASH",
    "4332724411": "AMIN_X-CME1JUFYS-FLASH",
    "4332724649": "AMIN_X-XFWOMFHRO-FLASH",
    "4332724837": "AMIN_X-Q1D4APA4G-FLASH",
    "4332725025": "AMIN_X-ZLUOB7G8Z-FLASH",
    "4332725229": "AMIN_X-6R1YLYQKF-FLASH",
    "4332725468": "AMIN_X-CIEZWJ3OK-FLASH",
    "4332725825": "AMIN_X-HBZCVFF7P-FLASH",
    "4332726079": "AMIN_X-ASRODG4W5-FLASH",
    "4332726307": "AMIN_X-LJAIDAQZ0-FLASH",
    "4332726487": "AMIN_X-UB9DJF5IB-FLASH",
    "4332726681": "AMIN_X-A7QLC1X04-FLASH",
    "4332726918": "AMIN_X-GXT4VE3KU-FLASH",
    "4332727288": "AMIN_X-1VNWAVMVI-FLASH",
    "4332727555": "AMIN_X-MP23U8ASR-FLASH",
    "4332727725": "AMIN_X-QDFHLD6CG-FLASH"
}
]
JWT_API_TEMPLATE = "https://jwt-ten-kappa.vercel.app/get?uid={uid}&password={password}"

CACHE = {
    "tokens": {},   # dict {uid: token}
    "timestamp": 0
}

COLLECTED_TOKENS = {}
GROUP_INDEX = 0  # مؤشر المجموعة الحالية

CACHE_DURATION = 10000  # ثانية
CONCURRENT_LIMIT = 50  # عدد الاتصالات المتزامنة

async def fetch_token(session, uid, password):
    url = JWT_API_TEMPLATE.format(uid=uid, password=password)
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                token = data.get("token")
                if token:
                    return uid, token
            return uid, None
    except Exception as e:
        print(f"Error fetching token for uid {uid}: {e}")
        return uid, None

async def fetch_token_with_semaphore(semaphore, session, uid, password):
    async with semaphore:
        return await fetch_token(session, uid, password)

async def fetch_tokens_for_group(group):
    tokens = {}
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_token_with_semaphore(semaphore, session, uid, password)
                 for uid, password in group.items()]
        results = await asyncio.gather(*tasks)
        for uid, token in results:
            if token:
                tokens[uid] = token
    return tokens

def is_cache_valid():
    return (time.time() - CACHE["timestamp"]) < CACHE_DURATION and len(CACHE["tokens"]) > 0

def get_last_update_vn():
    utc_time = datetime.fromtimestamp(CACHE["timestamp"], tz=timezone.utc)
    vn_time = utc_time + timedelta(hours=7)
    return vn_time.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/api/get_jwt", methods=["GET"])
def get_jwt_tokens():
    global GROUP_INDEX, COLLECTED_TOKENS

    if is_cache_valid():
        return jsonify({
            "count": len(CACHE["tokens"]),
            "last_update_vn": get_last_update_vn(),
            "tokens": CACHE["tokens"]
        })

    async def process_groups():
        global GROUP_INDEX
        groups_to_fetch = []

        # جلب الجروب الحالي
        groups_to_fetch.append(group_accounts[GROUP_INDEX])

        # جلب الجروب اللي بعده
        next_index = (GROUP_INDEX + 1) % len(group_accounts)
        if next_index != GROUP_INDEX:
            groups_to_fetch.append(group_accounts[next_index])

        all_tokens = {}
        for group in groups_to_fetch:
            tokens = await fetch_tokens_for_group(group)
            all_tokens.update(tokens)

        # تحديث المؤشر (+2 كل مرة)
        GROUP_INDEX = (GROUP_INDEX + 2) % len(group_accounts)

        return all_tokens

    new_tokens = asyncio.run(process_groups())
    COLLECTED_TOKENS.update(new_tokens)

    if GROUP_INDEX == 0:  # يعني خلصنا دورة كاملة
        CACHE["tokens"] = COLLECTED_TOKENS.copy()
        CACHE["timestamp"] = time.time()
        COLLECTED_TOKENS.clear()

    return jsonify({
        "count": len(COLLECTED_TOKENS) if not CACHE["tokens"] else len(CACHE["tokens"]),
        "last_update_vn": get_last_update_vn() if CACHE["tokens"] else None,
        "tokens": CACHE["tokens"] if CACHE["tokens"] else COLLECTED_TOKENS
    })
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
