import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession


def env(name: str, required: bool = True, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if required and (value is None or str(value).strip() == ""):
        raise RuntimeError(f"Thiếu biến môi trường bắt buộc: {name}")
    return value


async def run() -> None:
    api_id = int(env("TG_API_ID"))
    api_hash = env("TG_API_HASH")
    session_string = env("TG_SESSION_STRING")

    # Có thể dùng username (@botname) hoặc numeric id.
    target = env("TARGET_BOT")  # ví dụ: @my_checkin_bot
    message = env("CHECKIN_MESSAGE")  # ví dụ: /checkin hoặc "Điểm danh"

    client = TelegramClient(StringSession(session_string.strip()), api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError(
                "Session Telethon không hợp lệ hoặc đã hết hạn (GitHub Actions không thể nhập số điện thoại). "
                "Tạo lại TG_SESSION_STRING trên máy local (cùng TG_API_ID / TG_API_HASH), "
                "dán vào GitHub Secrets, không thêm dấu ngoặc hay xuống dòng."
            )
        me = await client.get_me()
        print(f"[{datetime.utcnow().isoformat()}Z] Đăng nhập OK: {getattr(me, 'username', None) or me.id}")
        await client.send_message(target, message)
        print(f"[{datetime.utcnow().isoformat()}Z] Đã gửi tới {target}: {message!r}")
    finally:
        await client.disconnect()


def main() -> None:
    load_dotenv()
    try:
        import asyncio

        asyncio.run(run())
    except Exception as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()

