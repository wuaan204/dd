# Telegram auto điểm danh (GitHub Actions)

Mục tiêu: dùng **tài khoản Telegram của bạn** (Telethon/MTProto) để tự động gửi tin nhắn “điểm danh” tới bot gốc mỗi ngày qua GitHub Actions.

> Lưu ý quan trọng: **Bot API thường không thể chủ động nhắn cho bot khác**. Vì vậy giải pháp ổn định là đăng nhập bằng **user account** (Telethon).

## 1) Tạo `TG_API_ID` và `TG_API_HASH`

- Vào `https://my.telegram.org` → **API development tools** → tạo app
- Lấy:
  - `api_id`
  - `api_hash`

## 2) Tạo `TG_SESSION_STRING` (chạy 1 lần trên máy cá nhân)

Cài và chạy đoạn sau trên máy bạn (không chạy trên GitHub Actions).

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install telethon==1.36.0
python
```

Trong Python REPL, chạy:

```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 123456
api_hash = "YOUR_API_HASH"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
```

- Telegram sẽ hỏi số điện thoại + OTP (và có thể 2FA).
- Copy chuỗi in ra → đó là `TG_SESSION_STRING`.

## 3) Set GitHub Secrets

Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

- `TG_API_ID`: ví dụ `123456`
- `TG_API_HASH`: ví dụ `abcd1234...`
- `TG_SESSION_STRING`: chuỗi session bạn tạo ở bước 2
- `TARGET_BOT`: ví dụ `@ten_bot_diem_danh` (hoặc id)
- `CHECKIN_MESSAGE`: ví dụ `/checkin` hoặc nội dung bot yêu cầu

## 4) Lịch chạy 00:00 hằng ngày

File workflow: `.github/workflows/checkin.yml` đang đặt:

- `cron: "0 0 * * *"` → chạy **00:00 UTC** mỗi ngày.

Nếu bạn muốn **00:00 theo giờ Việt Nam (UTC+7)** thì đổi cron thành:

- `cron: "0 17 * * *"` (vì 17:00 UTC = 00:00 VN ngày hôm sau)

## 5) Test thủ công

Vào tab **Actions** → chọn workflow → **Run workflow** để chạy thử ngay.

