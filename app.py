from flask import Flask, jsonify
import asyncio
import aiohttp
import time
from datetime import datetime, timezone, timedelta
import os

app = Flask(__name__)

# الحسابات الأصلية
accounts = {
    "4338687160": "A86F7CCECF2731E68A22252F352D3C6AAD7C49663AB27D536B133609CC6D41F6",
    "3989455736": "0B93D03DBF9078633413645837D9F2E2CDDB9B83BE1CBF6E71124961168A59E6",
    "4220385214": "BY_ABOD-7OYCGFYUH-REDZED",
    "4268722048": "959E3441742B99AC24A2E8D30E924867EEC74AA975E63FEFF746E1EF35BF1126",
    "3756198751": "00D29449261142B744505560DD012F026F7594D60C01EFFF5197D85EDE494AAC",
    "4268593602": "97F0952F3AE8F53618F604339B339C06612D5FB5BCA5A0FF45A2F6E69F88F9CC",
    "4269466321": "C60E304CBD5B19F8EC817D6E398490641CFAE61012366F2C2419565B46DE62F9",
    "4274072265": "4430B30317C578C91633585579EB3B8886A04D0EE75940F54DBA2F77EFC322DB",
    "3594635824": "BA45A6EEB4CF122D3897FD623CE37A44319EF51535C2EC1C015A3C47E54FD56E",
    "4086328720": "6A57FCF9D4FABFA6858105465CEE4CFAFBB0604301D52AD0AA61B631B991CC17",
    "4270587824": "BC7F7746BA867D89E6CCF95E40F2FAC4099377A352CB4F31FAE207F2196C1926",
    "4271120087": "F03CDB4661AA27811958650A13A36A9FD981D2565472AA5E52FB41F1F3E5C32C",
    "4255192509": "DCA1E6974A961ED2E5880871E56AC48A0DF22FC390419A3413A1AF6232A51DC4",
    "4187894529": "A0DCDE1BB375E81FC8607C4245D6B5706980D46C51AC1D5D9E90E65D48E6C136",
    "4271431299": "C45DF3E219F9079053ECAE27FAF5CC49D1D1250291D7E44991D5147AAFEA8808",
    "3499432876": "FBB7B397558DA2D7B8FECBA4D27ED5DD60555C8D799CA6DB1454AAD4F08028F8",
    "4272229571": "5022F79D6A7AE33776A5404301685EB171F97248FB79B7F87DB23ED62D70FA51",
    "4272932473": "0969995B2B0CD91360EB6B94CE7E33DE612E5402D29F38A1DACB6B966DC796D1",
    "3981271926": "7D7BB07D77A209812A04A9B5DCA874A8B4927DAE7F67211639DF1B0902A14B6B",
    "4273006503": "E16D58207E430558C9490BE6C869CE1BA96273A3CEBF299D19C0FFD4A851B237",
    "4272426688": "CC5AC39BE8379E93973D8F6A760954267194E36227A943433F608CA93573AA84",
    "4272524260": "54C44D4502E6C120675B0F9DCE1850F83F96372D0D600C9E342263D65FBBCE2E",
    "4273203777": "687222952BEB9D3ACFB75C256EE838E0BAC8BD1E9AA4D8512F99F722F78FA857",
    "4270876324": "6143920BDCCBCD7D35E02B17C3A7E8857DAFF5F95C1EF1E1283B34B096EC589F",
    "4237310198": "36390FA83A0FE3049829AFFD1F888D8C974427580446E17284FD2DD9A47519D8",
    "4270904373": "841D21D6AE86D7DB5AA499639AA7739F9EE99BE7237D8AA325BE1CB2830377CB",
    "4273596196": "30DD24ADF3590A76495B6569514C95FF4FF36702F16B17A668CBF68D0D0A7278",
    "4273491101": "16E860D29705E11EB0054F007822E841469D8E9C8C4E3DBF99C1F02E1E220492",
    "4268033348": "D31052279FEBD1DFA2615703A74162E4A8ECE084BC7FB4B96248DC9151734891",
    "4275418921": "0D24B4014E2532AC3579B6A7D84489A93DB459F66FFA8BF0CADA3E4F8888E518",
    "4275417742": "CCBD38AAC5A1FA5807FD683B6DD0EE6C5F4F7447DD51C6D30062CD425B10E493",
    "2428687964": "5713EC8FD8E2E406C46147A012BA91C2BDDA12A66F1FBE95126FC07AC626AE38",
    "4276239366": "E315E8A8E20124EDA788BCEC0C90E3EF11855383FCC83DDE3659F0EB7675F8CC",
    "4275989434": "F474C4EEDE02F28CA32E63FE9F5804279DB17E6593ECA19ACA8F8450610973E9",
    "4276519063": "77DD2E8A4683FE16E874095B8DA19BA02E247A476CE90753DC6F0DCEC5F3086C",
    "4276791513": "F29C3A22AD819DEE2BB857EBF821C73ED2AAE6DBF372DED9789100BC601747A8",
    "4277204950": "2314BC5CCCD8FAE9C30CF56930E95C29B5A58D517DD10D537B1D77EE26234A99",
    "4276823090": "53BB48B3754DB41A6958AEB474034AAD2FAB3DFF929173448210C056050A28C0",
    "4273296060": "BoTAVHJJSQAGFADAI",
    "4273304242": "BoTFULUTCLTYFADAI",
    "4273296522": "BoTSLGSPONTQFADAI",
    "4273297120": "BoTPFOS5JNBKFADAI",
    "4273297227": "BoTLWK2QV7XZFADAI",
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

# الحسابات الجديدة (بدون تكرار)
new_accounts_list = [
    {"id": "3989455736", "password": "0B93D03DBF9078633413645837D9F2E2CDDB9B83BE1CBF6E71124961168A59E6"},
    {"id": "4220385214", "password": "BY_ABOD-7OYCGFYUH-REDZED"},
    {"id": "4268722048", "password": "959E3441742B99AC24A2E8D30E924867EEC74AA975E63FEFF746E1EF35BF1126"},
    {"id": "3756198751", "password": "00D29449261142B744505560DD012F026F7594D60C01EFFF5197D85EDE494AAC"},
    {"id": "4268593602", "password": "97F0952F3AE8F53618F604339B339C06612D5FB5BCA5A0FF45A2F6E69F88F9CC"},
    {"id": "4269466321", "password": "C60E304CBD5B19F8EC817D6E398490641CFAE61012366F2C2419565B46DE62F9"},
    {"id": "4274072265", "password": "4430B30317C578C91633585579EB3B8886A04D0EE75940F54DBA2F77EFC322DB"},
    {"id": "3594635824", "password": "BA45A6EEB4CF122D3897FD623CE37A44319EF51535C2EC1C015A3C47E54FD56E"},
    {"id": "4086328720", "password": "6A57FCF9D4FABFA6858105465CEE4CFAFBB0604301D52AD0AA61B631B991CC17"},
    {"id": "4270587824", "password": "BC7F7746BA867D89E6CCF95E40F2FAC4099377A352CB4F31FAE207F2196C1926"},
    {"id": "4271120087", "password": "F03CDB4661AA27811958650A13A36A9FD981D2565472AA5E52FB41F1F3E5C32C"},
    {"id": "4255192509", "password": "DCA1E6974A961ED2E5880871E56AC48A0DF22FC390419A3413A1AF6232A51DC4"},
    {"id": "4187894529", "password": "A0DCDE1BB375E81FC8607C4245D6B5706980D46C51AC1D5D9E90E65D48E6C136"},
    {"id": "4271431299", "password": "C45DF3E219F9079053ECAE27FAF5CC49D1D1250291D7E44991D5147AAFEA8808"},
    {"id": "3499432876", "password": "FBB7B397558DA2D7B8FECBA4D27ED5DD60555C8D799CA6DB1454AAD4F08028F8"},
    {"id": "4272229571", "password": "5022F79D6A7AE33776A5404301685EB171F97248FB79B7F87DB23ED62D70FA51"},
    {"id": "4272932473", "password": "0969995B2B0CD91360EB6B94CE7E33DE612E5402D29F38A1DACB6B966DC796D1"},
    {"id": "3981271926", "password": "7D7BB07D77A209812A04A9B5DCA874A8B4927DAE7F67211639DF1B0902A14B6B"},
    {"id": "4273006503", "password": "E16D58207E430558C9490BE6C869CE1BA96273A3CEBF299D19C0FFD4A851B237"},
    {"id": "4272426688", "password": "CC5AC39BE8379E93973D8F6A760954267194E36227A943433F608CA93573AA84"},
    {"id": "4272524260", "password": "54C44D4502E6C120675B0F9DCE1850F83F96372D0D600C9E342263D65FBBCE2E"},
    {"id": "4273203777", "password": "687222952BEB9D3ACFB75C256EE838E0BAC8BD1E9AA4D8512F99F722F78FA857"},
    {"id": "4270876324", "password": "6143920BDCCBCD7D35E02B17C3A7E8857DAFF5F95C1EF1E1283B34B096EC589F"},
    {"id": "4237310198", "password": "36390FA83A0FE3049829AFFD1F888D8C974427580446E17284FD2DD9A47519D8"},
    {"id": "4270904373", "password": "841D21D6AE86D7DB5AA499639AA7739F9EE99BE7237D8AA325BE1CB2830377CB"},
    {"id": "4273596196", "password": "30DD24ADF3590A76495B6569514C95FF4FF36702F16B17A668CBF68D0D0A7278"},
    {"id": "4273491101", "password": "16E860D29705E11EB0054F007822E841469D8E9C8C4E3DBF99C1F02E1E220492"},
    {"id": "4268033348", "password": "D31052279FEBD1DFA2615703A74162E4A8ECE084BC7FB4B96248DC9151734891"},
    {"id": "4275418921", "password": "0D24B4014E2532AC3579B6A7D84489A93DB459F66FFA8BF0CADA3E4F8888E518"},
    {"id": "4275417742", "password": "CCBD38AAC5A1FA5807FD683B6DD0EE6C5F4F7447DD51C6D30062CD425B10E493"},
    {"id": "2428687964", "password": "5713EC8FD8E2E406C46147A012BA91C2BDDA12A66F1FBE95126FC07AC626AE38"},
    {"id": "4276239366", "password": "E315E8A8E20124EDA788BCEC0C90E3EF11855383FCC83DDE3659F0EB7675F8CC"},
    {"id": "4275989434", "password": "F474C4EEDE02F28CA32E63FE9F5804279DB17E6593ECA19ACA8F8450610973E9"},
    {"id": "4276519063", "password": "77DD2E8A4683FE16E874095B8DA19BA02E247A476CE90753DC6F0DCEC5F3086C"},
    {"id": "4276791513", "password": "F29C3A22AD819DEE2BB857EBF821C73ED2AAE6DBF372DED9789100BC601747A8"},
    {"id": "4277204950", "password": "2314BC5CCCD8FAE9C30CF56930E95C29B5A58D517DD10D537B1D77EE26234A99"},
    {"id": "4276823090", "password": "53BB48B3754DB41A6958AEB474034AAD2FAB3DFF929173448210C056050A28C0"}
]

# تحويل القائمة الجديدة إلى dict وإضافتها إلى الحسابات الحالية
for account in new_accounts_list:
    account_id = account["id"]
    password = account["password"]
    
    # فقط أضف الحساب إذا لم يكن موجوداً بالفعل (لتجنب التكرار)
    if account_id not in accounts:
        accounts[account_id] = password
        print(f"تمت إضافة حساب جديد: {account_id}")
    else:
        # إذا كان موجوداً بالفعل، تحقق من تطابق كلمة المرور
        if accounts[account_id] != password:
            print(f"تنبيه: حساب {account_id} موجود بالفعل ولكن كلمة المرور مختلفة!")
            print(f"كلمة المرور القديمة: {accounts[account_id][:20]}...")
            print(f"كلمة المرور الجديدة: {password[:20]}...")

JWT_API_TEMPLATE = "https://jwt-liard-eight.vercel.app/get?uid={uid}&password={password}"

CACHE = {
    "tokens": {},   # dict {uid: token}
    "timestamp": 0,
    "total_accounts": len(accounts)  # تخزين عدد الحسابات الكلي
}

CACHE_DURATION = 10000  # ثانية
CONCURRENT_LIMIT = 50  # عدد الاتصالات المتزامنة

async def fetch_token(session, uid, password):
    url = JWT_API_TEMPLATE.format(uid=uid, password=password)
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                data = await resp.json()
                token = data.get("token")
                if token:
                    return uid, token
                else:
                    print(f"لم يتم العثور على token لـ {uid}")
                    return uid, None
            else:
                print(f"خطأ في استجابة API لـ {uid}: {resp.status}")
                return uid, None
    except asyncio.TimeoutError:
        print(f"انتهت المهلة لـ {uid}")
        return uid, None
    except Exception as e:
        print(f"خطأ في جلب token لـ {uid}: {e}")
        return uid, None

async def fetch_token_with_semaphore(semaphore, session, uid, password):
    async with semaphore:
        return await fetch_token(session, uid, password)

async def fetch_all_tokens():
    """جلب جميع التوكنز مرة واحدة"""
    tokens = {}
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
    
    print(f"جاري جلب التوكنز لـ {len(accounts)} حساب...")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_token_with_semaphore(semaphore, session, uid, password)
                 for uid, password in accounts.items()]
        results = await asyncio.gather(*tasks)
        
        successful = 0
        failed = 0
        
        for uid, token in results:
            if token:
                tokens[uid] = token
                successful += 1
            else:
                failed += 1
        
        elapsed_time = time.time() - start_time
        print(f"اكتمل جلب التوكنز: {successful} ناجح، {failed} فاشل")
        print(f"الوقت المستغرق: {elapsed_time:.2f} ثانية")
    
    return tokens

def is_cache_valid():
    """التحقق من صلاحية الكاش"""
    return (time.time() - CACHE["timestamp"]) < CACHE_DURATION and len(CACHE["tokens"]) > 0

def get_last_update_vn():
    """الحصول على وقت آخر تحديث بتوقيت فيتنام"""
    if CACHE["timestamp"] == 0:
        return "لم يتم التحديث بعد"
    
    utc_time = datetime.fromtimestamp(CACHE["timestamp"], tz=timezone.utc)
    vn_time = utc_time + timedelta(hours=7)
    return vn_time.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/api/get_jwt", methods=["GET"])
def get_jwt_tokens():
    """الرئيسية لجلب التوكنز"""
    # إذا الكاش صالح، ارجعه مباشرة
    if is_cache_valid():
        return jsonify({
            "count": len(CACHE["tokens"]),
            "total_accounts": CACHE["total_accounts"],
            "last_update_vn": get_last_update_vn(),
            "cache_valid_until_vn": get_cache_expiry_vn(),
            "tokens": CACHE["tokens"]
        })
    
    # إذا انتهت صلاحية الكاش، جلب التوكنز الجديدة
    try:
        new_tokens = asyncio.run(fetch_all_tokens())
        
        # تحديث الكاش
        CACHE["tokens"] = new_tokens
        CACHE["timestamp"] = time.time()
        CACHE["total_accounts"] = len(accounts)
        
        return jsonify({
            "count": len(new_tokens),
            "total_accounts": len(accounts),
            "last_update_vn": get_last_update_vn(),
            "cache_valid_until_vn": get_cache_expiry_vn(),
            "tokens": new_tokens
        })
    except Exception as e:
        print(f"خطأ في جلب التوكنز: {e}")
        return jsonify({
            "error": str(e),
            "count": 0,
            "total_accounts": len(accounts),
            "tokens": {}
        }), 500

def get_cache_expiry_vn():
    """الحصول على وقت انتهاء صلاحية الكاش بتوقيت فيتنام"""
    if CACHE["timestamp"] == 0:
        return "لا يوجد كاش"
    
    expiry_time = CACHE["timestamp"] + CACHE_DURATION
    utc_time = datetime.fromtimestamp(expiry_time, tz=timezone.utc)
    vn_time = utc_time + timedelta(hours=7)
    return vn_time.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/api/refresh", methods=["GET"])
def refresh_tokens():
    """تجديد التوكنز يدوياً"""
    try:
        new_tokens = asyncio.run(fetch_all_tokens())
        
        # تحديث الكاش
        CACHE["tokens"] = new_tokens
        CACHE["timestamp"] = time.time()
        CACHE["total_accounts"] = len(accounts)
        
        return jsonify({
            "message": "تم تجديد التوكنز بنجاح",
            "count": len(new_tokens),
            "total_accounts": len(accounts),
            "last_update_vn": get_last_update_vn(),
            "cache_valid_until_vn": get_cache_expiry_vn()
        })
    except Exception as e:
        print(f"خطأ في تجديد التوكنز: {e}")
        return jsonify({
            "error": str(e),
            "message": "فشل في تجديد التوكنز"
        }), 500

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """إحصائيات عن التوكنز"""
    success_count = len(CACHE["tokens"]) if CACHE["tokens"] else 0
    
    return jsonify({
        "total_accounts": len(accounts),
        "successful_tokens": success_count,
        "failed_tokens": len(accounts) - success_count,
        "cache_valid": is_cache_valid(),
        "last_update_vn": get_last_update_vn(),
        "cache_valid_until_vn": get_cache_expiry_vn(),
        "cache_duration_seconds": CACHE_DURATION
    })

@app.route("/api/accounts", methods=["GET"])
def get_accounts_list():
    """الحصول على قائمة الحسابات (دون كلمات المرور)"""
    account_ids = list(accounts.keys())
    return jsonify({
        "count": len(account_ids),
        "accounts": account_ids
    })

@app.route("/", methods=["GET"])
def home():
    """الصفحة الرئيسية"""
    return jsonify({
        "message": "JWT Token Service",
        "endpoints": {
            "/api/get_jwt": "جلب جميع التوكنز",
            "/api/refresh": "تجديد التوكنز يدوياً",
            "/api/stats": "إحصائيات الخدمة",
            "/api/accounts": "قائمة الحسابات"
        },
        "total_accounts": len(accounts),
        "cache_duration_seconds": CACHE_DURATION
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"بدء الخدمة على المنفذ {port}")
    print(f"عدد الحسابات الكلي: {len(accounts)}")
    app.run(host="0.0.0.0", port=port)
