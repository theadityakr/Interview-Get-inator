# 📡 Telegram Channel Forwarder

Automatically listens to multiple public Telegram channels and forwards new posts to your private channel — triggering the n8n automation pipeline.

---

## 🧠 How It Works

```
Public Channels (multiple)
        ↓  Telethon userbot (always running)
Private Channel
        ↓  Telegram Trigger (n8n)
HTTP Request → FastAPI → Browser Agent applies to job
```

---

## 📦 Installation

## 0. Initialize project

```bash
uv venv --python 3.12
source .venv/bin/activate
# On Windows use `.venv\Scripts\activate`
```

### 1. Install dependencies

```bash
uv pip install telethon python-dotenv
```

---

## ⚙️ Environment Configuration

Add these to your `.env` file:

```env
# ===== TELEGRAM =====
API_ID=12345678
API_HASH=your_api_hash_here
PRIVATE_CHANNEL=@your_private_channel
SOURCE_CHANNELS=@channel_one,@channel_two,@channel_three
```

### How to get `API_ID` and `API_HASH`

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Click **API Development Tools**
4. Create a new application
   - App title: anything (e.g. `interview-get-inator`)
   - Short name: 5–32 alphanumeric characters (e.g. `igiapp`)
   - Platform: **Desktop**
   - URL and Description: leave blank
5. Copy `App api_id` and `App api_hash`

---

## 📁 File

```
project/
│
├── telegram_forwarder.py   ← the forwarder script
├── .env                    ← your credentials
└── ...
```

---

## 🚀 Running

```bash
python telegram_forwarder.py
```

### First-time login

On first run, Telethon will prompt:

```
Please enter your phone number: +91xxxxxxxxxx
Please enter the code you received: 12345
```

Enter your Telegram phone number (with country code) and the OTP sent to your Telegram app. A `forwarder_session.session` file is saved — you won't need to log in again.

---

## 🔁 Running Everything Together

You need **two terminals** running simultaneously:

| Terminal 1 | Terminal 2 |
|---|---|
| `uv run uvicorn main:app --reload` | `python telegram_forwarder.py` |
| FastAPI backend | Telegram listener |

---

## ⚠️ Known Limitations

- ❌ Script must stay running — if it stops, posts during downtime are missed
- ❌ Telegram rate limits may apply if channels post very frequently
- ❌ Account must have joined/access to the source public channels

---

## 🔮 Future Improvements

- Run as a background service (Windows Task Scheduler / Linux systemd)
- Filter posts by keyword before forwarding
- Extract job URLs directly and hit FastAPI without the private channel middleman
- Add deduplication to avoid applying to the same job twice

---

## 📜 License

MIT License
