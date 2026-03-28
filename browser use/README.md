# 🤖 Browser-Use Autonomous Agent (Env-Driven Setup)

A **production-ready AI browser automation system** built using `browser_use`, fully configurable via environment variables.

This project enables:

* 🌐 Autonomous browser control
* 🧠 LLM-driven decision making
* 🧾 Job application automation
* 🔁 Scalable & configurable architecture

---

# 🚀 Features

* ✅ Fully **env-driven configuration**
* ✅ Modular architecture (LLM, Browser, Agent separated)
* ✅ Custom tools support (resume, DB, APIs)
* ✅ Vision-enabled automation (UI understanding)
* ✅ Fallback LLM support
* ✅ Debug logging + GIF recording
* ✅ Production-ready structure

---

# 📦 Installation

```bash
pip install browser-use python-dotenv
playwright install
```

> `browser_use` allows you to configure agent, browser, and LLM behavior programmatically for automation tasks ([Browser Use Cloud][1])

---

# 📁 Project Structure

```
project/
│
├── config/
│   ├── env.py
│   ├── llm_config.py
│   ├── browser_config.py
│   ├── agent_config.py
│   └── settings.py
│
├── tools/
│   └── custom_tools.py
│
├── main.py
├── .env
└── README.md
```

---

# ⚙️ Environment Configuration (`.env`)

```env
# ===== LLM =====
LLM_MODEL=o3
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000

FALLBACK_MODEL=gpt-4o-mini
EXTRACTION_MODEL=gpt-4o-mini

OPENAI_API_KEY=your_key

# ===== BROWSER =====
HEADLESS=false
BROWSER_SECURITY=false
BROWSER_ARGS=--disable-blink-features=AutomationControlled,--start-maximized

# ===== AGENT =====
MAX_STEPS=100
MAX_ACTIONS_PER_STEP=5
MAX_FAILURES=5
USE_VISION=true
VISION_DETAIL=high

# ===== FILES =====
RESUME_PATH=./resume.pdf
LOG_PATH=logs/conversation.json

# ===== DEBUG =====
GENERATE_GIF=true
```

📌 `browser_use` supports config merging from `.env`, YAML, and runtime params with clear precedence rules ([DeepWiki][2])

---

# 🧠 Configuration Layers

## 1. LLM Config

* Model selection
* Temperature / tokens
* Fallback LLM
* Extraction LLM

## 2. Browser Config

* Headless mode
* Window size / args
* Proxy / CDP
* Session persistence

```python
Browser(
    headless=False,
    window_size={'width': 1000, 'height': 700}
)
```

> Browser settings include headless mode, viewport, and launch options ([Browser Use Cloud][3])

---

## 3. Agent Config

* Task prompt (core intelligence)
* Tools injection
* Vision mode
* Execution limits

```python
Agent(
    task="Your task",
    llm=llm,
    browser=browser
)
```

---

# 🧰 Custom Tools

Extend agent capabilities:

```python
@tools.action("Get resume data")
async def get_resume(browser_session):
    return {
        "name": "Aditya",
        "skills": ["Java", "Spring"]
    }
```

Use cases:

* Resume injection
* Database checks
* API integrations

---

# ▶️ Running the Agent

```bash
python main.py
```

```python
agent = Settings.get_agent()

result = await agent.run(max_steps=100)
```

* `max_steps` controls execution loop length ([Browser Use Cloud][1])

---

# 👁️ Vision Mode

Enable UI understanding:

```python
use_vision=True
```

Useful for:

* Dynamic websites
* Form detection
* Button interaction

---

# 🔐 Authentication (Advanced)

Supported methods:

* Chrome profile reuse
* Storage state (cookies/session)
* 2FA handling

```python
browser = Browser.from_system_chrome()
```

> Browser-use supports persistent sessions and authentication reuse ([Browser Use Cloud][4])

---

# ⚡ Performance Tips

* Reduce `max_steps`
* Use smaller models for extraction
* Avoid unnecessary screenshots
* Reuse browser sessions

---

# ⚠️ Known Limitations

* ❌ Websites may block automation
* ❌ CAPTCHA handling required
* ❌ LLM may hallucinate fields
* ❌ Multi-step flows can loop

---

# 🛠️ Best Practices

* Always validate form submission
* Add retry logic
* Track applied jobs (DB/cache)
* Use domain restrictions for safety

---

# 🔮 Future Improvements

* Telegram trigger integration
* Job deduplication system
* Resume auto-parser (PDF → JSON)
* Multi-agent orchestration

---

# 📜 License

MIT License

---

# 🙌 Contributing

PRs are welcome. Build cool stuff 🚀

[1]: https://docs.browser-use.com/customize/agent/basics?utm_source=chatgpt.com "Configuration - Browser Use"
[2]: https://deepwiki.com/browser-use/browser-use/9.2-configuration-management?utm_source=chatgpt.com "Configuration Management | browser-use/browser-use | DeepWiki"
[3]: https://docs.browser-use.com/customize/browser/basics?utm_source=chatgpt.com "Configuration - Browser Use"
[4]: https://docs.browser-use.com/customize/browser/authentication?utm_source=chatgpt.com "Authentication - Browser Use"
