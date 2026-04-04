"""
Một lần: đăng nhập Telethon trên máy, in chuỗi session để dán vào .env (TG_SESSION_STRING)
và GitHub Secret cùng tên. Cần TG_API_ID + TG_API_HASH trong .env hoặc biến môi trường.
"""
import os
import sys

from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession


def main() -> None:
    load_dotenv()

    raw_id = os.getenv("TG_API_ID", "").strip()
    api_hash = os.getenv("TG_API_HASH", "").strip()
    if not raw_id or not api_hash:
        print("Thiếu TG_API_ID hoặc TG_API_HASH trong .env (hoặc môi trường).", file=sys.stderr)
        sys.exit(1)

    try:
        api_id = int(raw_id)
    except ValueError:
        print("TG_API_ID phải là số nguyên.", file=sys.stderr)
        sys.exit(1)

    with TelegramClient(StringSession(), api_id, api_hash) as client:
        client.start()
        s = client.session.save()
        print()
        print("--- Dán dòng sau vào .env ---")
        print(f"TG_SESSION_STRING={s}")
        print()
        print("--- Hoặc chỉ giá trị (dán vào GitHub Secret TG_SESSION_STRING) ---")
        print(s)


if __name__ == "__main__":
    main()
