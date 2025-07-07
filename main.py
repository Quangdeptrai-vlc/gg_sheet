import requests
import time
import hashlib

# === CẤU HÌNH ===
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmtim_Lg-D2R5ym2pfpBNkMZ0dJcV_Gg18X5teNJJId_aeLaRSHc7rl-hIa7JBtuLyNvbMxF5iPk5R/pub?output=csv&gid=0"
BOT_TOKEN = "8009452196:AAEpTgVa3gfbS1qUfXTg3IrcnQdCmmjF1UE"
CHAT_ID = "7193701944"
CHECK_INTERVAL = 300  # 5 phút

# === HÀM GỬI TELEGRAM ===
def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print("❌ Gửi Telegram thất bại:", r.text)
    except Exception as e:
        print("❌ Lỗi gửi Telegram:", e)

# === HÀM LẤY VÀ BĂM DỮ LIỆU GOOGLE SHEET ===
def get_sheet_hash():
    try:
        resp = requests.get(SHEET_CSV_URL)
        content = resp.text.strip()
        hash_value = hashlib.md5(content.encode()).hexdigest()
        return hash_value, content
    except Exception as e:
        print("❌ Lỗi khi lấy dữ liệu sheet:", e)
        return None, ""

# === KHỞI ĐỘNG ===
send_telegram_message("📊 Bot theo dõi Google Sheet đã khởi động!")

# === VÒNG LẶP THEO DÕI ===
last_hash = None

while True:
    current_hash, content = get_sheet_hash()
    if current_hash is None:
        time.sleep(CHECK_INTERVAL)
        continue

    if last_hash is None:
        last_hash = current_hash
    elif current_hash != last_hash:
        send_telegram_message("🔔 Google Sheet đã thay đổi!")
        last_hash = current_hash
    else:
        print("✅ Không có thay đổi.")

    time.sleep(CHECK_INTERVAL)
