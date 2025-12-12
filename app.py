from flask import Flask, jsonify
import asyncio
import aiohttp
import time
from datetime import datetime, timezone, timedelta
import os

app = Flask(__name__)


group_accounts = [
    {
        "4182940828": "C4_RIZAKYI_BNGX_VIP_DMRBC7MS",
        "4182940823": "C4_RIZAKYI_BNGX_VIP_K34JKBYB",
        "4182940830": "C4_RIZAKYI_BNGX_VIP_DBFRALNM",
        "4182940837": "C4_RIZAKYI_BNGX_VIP_CMDFFYLB",
        "4182940841": "C4_RIZAKYI_BNGX_VIP_4KFHBOXF",
        "4182940835": "C4_RIZAKYI_BNGX_VIP_H7JDOQ8G",
        "4182940827": "C4_RIZAKYI_BNGX_VIP_KTUHWQBQ",
        "4182940825": "C4_RIZAKYI_BNGX_VIP_S0YSEBPX",
        "4182940843": "C4_RIZAKYI_BNGX_VIP_ZCZ53KDX",
        "4182940836": "C4_RIZAKYI_BNGX_VIP_ASK542PD",
        "4182940842": "C4_RIZAKYI_BNGX_VIP_EKQGFRUI",
        "4182940831": "C4_RIZAKYI_BNGX_VIP_JSVSLT3B",
        "4182940826": "C4_RIZAKYI_BNGX_VIP_SJL744AW",
        "4182940824": "C4_RIZAKYI_BNGX_VIP_KQJ3049C",
        "4182940840": "C4_RIZAKYI_BNGX_VIP_JOERBM3M",
        "4182940832": "C4_RIZAKYI_BNGX_VIP_NHAHXFRX",
        "4182940822": "C4_RIZAKYI_BNGX_VIP_KS6YLG56",
        "4182940833": "C4_RIZAKYI_BNGX_VIP_VVOADP3J",
        "4182940834": "C4_RIZAKYI_BNGX_VIP_64C5JAXT",
        "4182940829": "C4_RIZAKYI_BNGX_VIP_US2MGPBH",
        "4182943566": "C4_RIZAKYI_BNGX_VIP_YFVQMDJS",
        "4182943556": "C4_RIZAKYI_BNGX_VIP_ICXYL53U",
        "4182943559": "C4_RIZAKYI_BNGX_VIP_TMBYYXWA",
        "4182943562": "C4_RIZAKYI_BNGX_VIP_VDZXJUR8",
        "4182943571": "C4_RIZAKYI_BNGX_VIP_AD1JJGIO",
        "4182943572": "C4_RIZAKYI_BNGX_VIP_MNCO1SLZ",
        "4182943574": "C4_RIZAKYI_BNGX_VIP_GBFM4OWM",
        "4182943568": "C4_RIZAKYI_BNGX_VIP_TGHEPCML",
        "4182943557": "C4_RIZAKYI_BNGX_VIP_BKDGPICB",
        "4182943569": "C4_RIZAKYI_BNGX_VIP_6LO1RUBE",
        "4182943560": "C4_RIZAKYI_BNGX_VIP_MNPBLPQR",
        "4182943570": "C4_RIZAKYI_BNGX_VIP_3WR2J98L",
        "4182943561": "C4_RIZAKYI_BNGX_VIP_GG5XBRPF",
        "4182943573": "C4_RIZAKYI_BNGX_VIP_IXBIYQSK",
        "4182943555": "C4_RIZAKYI_BNGX_VIP_VYLMV9XN",
        "4182943563": "C4_RIZAKYI_BNGX_VIP_ELWLZ7GI",
        "4182943564": "C4_RIZAKYI_BNGX_VIP_TVQJ2HBB",
        "4182943565": "C4_RIZAKYI_BNGX_VIP_QEV6KMQY",
        "4182943558": "C4_RIZAKYI_BNGX_VIP_BR6HUVB7",
        "4182943567": "C4_RIZAKYI_BNGX_VIP_UKQYI2XB",
        "4182944867": "C4_RIZAKYI_BNGX_VIP_SEKMB6TW",
        "4182944869": "C4_RIZAKYI_BNGX_VIP_AG1OYXDL",
        "4182944868": "C4_RIZAKYI_BNGX_VIP_6TZH99QI",
        "4182944871": "C4_RIZAKYI_BNGX_VIP_H3F0VGAN",
        "4182944866": "C4_RIZAKYI_BNGX_VIP_H43THCGH",
        "4182944877": "C4_RIZAKYI_BNGX_VIP_HWARQTT6",
        "4182944874": "C4_RIZAKYI_BNGX_VIP_PB0VVZTM",
        "4182944880": "C4_RIZAKYI_BNGX_VIP_WC0NHWIC",
        "4182944878": "C4_RIZAKYI_BNGX_VIP_9JL17I9X",
        "4182944873": "C4_RIZAKYI_BNGX_VIP_PFGN4AOJ",
        "4182944875": "C4_RIZAKYI_BNGX_VIP_4TEJS0VG",
        "4182944872": "C4_RIZAKYI_BNGX_VIP_IDIRH2SN",
        "4182944883": "C4_RIZAKYI_BNGX_VIP_STIFACIR",
        "4182944884": "C4_RIZAKYI_BNGX_VIP_FA49BYCW",
        "4182944876": "C4_RIZAKYI_BNGX_VIP_UNW639LI",
        "4182944882": "C4_RIZAKYI_BNGX_VIP_GGWCZVXX",
        "4182944870": "C4_RIZAKYI_BNGX_VIP_RFVVDNRD",
        "4182944879": "C4_RIZAKYI_BNGX_VIP_QIN83IGW",
        "4182944881": "C4_RIZAKYI_BNGX_VIP_ATCLV3XX",
        "4182944885": "C4_RIZAKYI_BNGX_VIP_Z49H7L6P",
        "4182948046": "C4_RIZAKYI_BNGX_VIP_S3AQ4GRC",
        "4182948060": "C4_RIZAKYI_BNGX_VIP_L0IHXYVY",
        "4182948049": "C4_RIZAKYI_BNGX_VIP_OUNM5WJI",
        "4182948058": "C4_RIZAKYI_BNGX_VIP_2OGLKV80",
        "4182948052": "C4_RIZAKYI_BNGX_VIP_U07DPSTE",
        "4182948047": "C4_RIZAKYI_BNGX_VIP_KVTEUBNU",
        "4182948053": "C4_RIZAKYI_BNGX_VIP_TPTYWSZR",
        "4182948055": "C4_RIZAKYI_BNGX_VIP_W3Y8AKM8",
        "4182948062": "C4_RIZAKYI_BNGX_VIP_YG6SJDR5",
        "4182948050": "C4_RIZAKYI_BNGX_VIP_RFCZSJEL",
        "4182948045": "C4_RIZAKYI_BNGX_VIP_H8PTT1QL",
        "4182948057": "C4_RIZAKYI_BNGX_VIP_J35UDGBC",
        "4182948044": "C4_RIZAKYI_BNGX_VIP_C5R8EYZ5",
        "4182948043": "C4_RIZAKYI_BNGX_VIP_ELERPSHJ",
        "4182948056": "C4_RIZAKYI_BNGX_VIP_JUKFZNZS",
        "4182948054": "C4_RIZAKYI_BNGX_VIP_24FOYXXB",
        "4182948048": "C4_RIZAKYI_BNGX_VIP_WDLG8B7D",
        "4182948051": "C4_RIZAKYI_BNGX_VIP_8RVSBKQ1",
        "4182948059": "C4_RIZAKYI_BNGX_VIP_44UIOWJC",
        "4182948061": "C4_RIZAKYI_BNGX_VIP_PW7YJDEN",
        "4182949547": "C4_RIZAKYI_BNGX_VIP_MSUV6GT3",
        "4182949550": "C4_RIZAKYI_BNGX_VIP_MW2LXFWV",
        "4182949566": "C4_RIZAKYI_BNGX_VIP_OTX3KMMK",
        "4182949561": "C4_RIZAKYI_BNGX_VIP_PJ1RX789",
        "4182949551": "C4_RIZAKYI_BNGX_VIP_FGHRXGN7",
        "4182949555": "C4_RIZAKYI_BNGX_VIP_VHQ7GOLJ",
        "4182949570": "C4_RIZAKYI_BNGX_VIP_W5ILWOWB",
        "4182949557": "C4_RIZAKYI_BNGX_VIP_N0AFU4VV",
        "4182949560": "C4_RIZAKYI_BNGX_VIP_ZLYQKKFN",
        "4182949569": "C4_RIZAKYI_BNGX_VIP_1RQXUFHQ",
        "4182949563": "C4_RIZAKYI_BNGX_VIP_7BG6P51Y",
        "4182949567": "C4_RIZAKYI_BNGX_VIP_VIADTC6L",
        "4182949553": "C4_RIZAKYI_BNGX_VIP_PLH3HNFQ",
        "4182949562": "C4_RIZAKYI_BNGX_VIP_3PBD61OX",
        "4182949564": "C4_RIZAKYI_BNGX_VIP_844GVVM3",
        "4182949565": "C4_RIZAKYI_BNGX_VIP_71BYTPA0",
        "4197570463": "BNGX_Vip_is_here_2R8MALAQF",
        "4197570658": "BNGX_Vip_is_here_F8ZM7L61A",
        "4197570633": "BNGX_Vip_is_here_XPY4PU4B7"
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
