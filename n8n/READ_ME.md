# 🔄 n8n Workflow — Job Application Automation

Listens to the private Telegram channel and triggers the FastAPI browser agent for every new job post.

---

## 🧠 How It Works

```
Private Telegram Channel (new post)
        ↓  Telegram Trigger (webhook)
HTTP Request Node
        ↓
FastAPI → Browser Agent applies to job
```

---

## 📦 Installation

### 1. Install n8n locally

```bash
npm init -y || npm install using the package
npm install n8n
```

---

## ⚙️ Prerequisites

### ngrok (required for Telegram webhook)

Telegram needs a public HTTPS URL to send webhook events. Since n8n runs locally, use ngrok to expose it.

**Install ngrok:** [https://ngrok.com/download](https://ngrok.com/download)

```bash
ngrok http 5678
```

Copy the generated URL e.g. `https://0664-152-58-28-157.ngrok-free.app`

---

## 🚀 Running n8n

Run these commands in order every time you start n8n:

```powershell
# 1. Set webhook URLs (replace with your current ngrok URL)
$env:N8N_WEBHOOK_URL="https://your-ngrok-url.ngrok-free.app"
$env:WEBHOOK_URL="https://your-ngrok-url.ngrok-free.app"

# 2. Start n8n
.\node_modules\.bin\n8n
```

n8n will be available at: `http://localhost:5678`

> ⚠️ Free ngrok URLs change every time you restart ngrok. Update both env vars each time.

---

## 🔁 Workflow Structure

```
Telegram Trigger
    → Update Type: channel_post
    → Listens to your private channel

HTTP Request
    → Method: POST
    → URL: http://127.0.0.1:8000/api/v1/jobs/apply
    → Body (JSON): { "url": "{{ $json.url }}" }
```

---

## 🛠️ Workflow Setup (Step by Step)

### 1. Telegram Trigger Node
- Add a **Telegram Trigger** node
- Set **Update Type** to `channel_post`
- Connect your Telegram bot credentials
- Make sure your bot is added as admin to the private channel

### 2. HTTP Request Node
- Add an **HTTP Request** node
- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/api/v1/jobs/apply`
- **Body Content Type:** `JSON`
- **Body:**
```json
{
  "url": "{{ $json.message.text }}"
}
```
> Toggle the field to **expression mode** (click the `=` button) so `{{ }}` is evaluated

### 3. Activate the Workflow
- Click the **Active** toggle at the top of the editor to turn it **ON**
- Inactive = only runs on manual test click
- Active = listens continuously for new posts

---

## 📁 Project Structure

```
n8n/
│
├── node_modules/
├── package.json
└── (workflow saved inside n8n's internal DB)
```

---

## ▶️ Running Everything Together

You need **three terminals** running simultaneously:

| Terminal | Command | Purpose |
|---|---|---|
| 1 | `ngrok http 5678` | Expose n8n to internet for Telegram webhook |
| 2 | `$env:WEBHOOK_URL=... && .\node_modules\.bin\n8n` | n8n workflow engine |
| 3 | `uv run uvicorn main:app --reload` | FastAPI backend |
| 4 | `python telegram_forwarder.py` | Telegram channel listener |

---

## ⚠️ Known Limitations

- ❌ Free ngrok URL changes on every restart — must update env vars each time
- ❌ n8n workflow must be set to **Active** or it won't listen
- ❌ Telegram bot must be an **admin** in the private channel

---

## 🔮 Future Improvements

- Use a paid ngrok plan or self-hosted tunnel for a static URL
- Save ngrok URL to `.env` and load automatically on startup
- Add error handling node in n8n for failed API calls
- Add a Telegram notification node to confirm successful job applications

---

## 📜 License

MIT License