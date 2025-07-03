import requests
import smtplib
import time
import os
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

URL = "https://www.goethe.de/ins/vn/vi/sta/han/prf/gzb2.cfm"
CHECK_INTERVAL = 2  # giây

def send_email(subject, body):
    sender = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_PASSWORD")
    receiver = os.environ.get("RECEIVER_EMAIL")

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def get_page_content():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error fetching page: {e}")
        return ""

def main():
    print("🔄 Bắt đầu theo dõi Goethe B2...")
    old_content = get_page_content()
    while True:
        time.sleep(CHECK_INTERVAL)
        new_content = get_page_content()
        if new_content and new_content != old_content:
            print("⚠️ PHÁT HIỆN THAY ĐỔI TRANG!")
            send_email("Goethe B2 – PHÁT HIỆN THAY ĐỔI!", URL)
            old_content = new_content
        else:
            print("⏳ Không thay đổi...")

if __name__ == "__main__":
    main()