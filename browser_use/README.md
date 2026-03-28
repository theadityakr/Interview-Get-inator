# 🤖 Browser-Use Autonomous Agent (Env-Driven + API-Based Execution)

A **production-ready AI browser automation system** built using `browser_use`, fully configurable via environment variables and exposed via a **FastAPI backend**.

This project enables:

* 🌐 Autonomous browser control
* 🧠 LLM-driven decision making
* 🧾 Job application automation via API
* 🔁 Scalable & async architecture

---

# 🚀 Features

* ✅ Fully **env-driven configuration**
* ✅ Modular architecture (LLM, Browser, Agent separated)
* ✅ FastAPI endpoint for triggering automation
* ✅ Background task execution (non-blocking API)
* ✅ Resume handled via config (no upload needed)
* ✅ Vision-enabled automation (UI understanding)
* ✅ Fallback LLM support
* ✅ Debug logging + GIF recording
* ✅ Production-ready structure

---

# 📦 Installation (Using `uv` - Recommended)

## 1. Install uv

```bash
pip install uv

```

## 2. Initialize project

```bash
uv venv --python 3.12
source .venv/bin/activate
# On Windows use `.venv\Scripts\activate`
```

## 3. Add dependencies

```bash
uv pip install browser-use fastapi python-dotenv uvicorn
uvx browser-use install
```

## 4. Install Playwright browsers

```bash
playwright install
```

---

# ▶️ Running the API Server

```bash
mkdir logs
uv run python main.py
```

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
├── controller/
│   └── job_controller.py
│
├── service/
│   └── job_service.py
│
├── worker/
│   └── agent_worker.py
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
# ===== SERVER =====
PORT=8174
HOST=0.0.0.0

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

---

# 🌐 API Endpoint (Trigger Job Application)

## 📌 Endpoint

```
POST /api/v1/jobs/apply
```

## 📥 Request Body

```json
{
  "url": "https://example.com/job-posting"
}
```

## 📤 Response

```json
{
  "status": "started",
  "message": "Job application started in background"
}
```

---

# 🧩 Controller Layer

```python
from fastapi import APIRouter, BackgroundTasks
from service.job_service import apply_to_job

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])

@router.post("/apply")
async def apply_job(request: dict, background_tasks: BackgroundTasks):
    url = request.get("url")

    background_tasks.add_task(apply_to_job, url)

    return {
        "status": "started",
        "message": "Job application started in background"
    }
```

---

# ⚙️ Service Layer

```python
from worker.agent_worker import run_agent_task

async def apply_to_job(url: str):
    await run_agent_task(url)
```

---

# 🧠 Worker (Agent Execution)

```python
import asyncio
from config.settings import Settings

async def run_agent_task(url: str):
    try:
        agent = Settings.get_agent()

        agent.task = f"""
        Open the job URL and apply.

        URL: {url}

        Instructions:
        - Extract job details
        - Use resume from available files
        - Fill the application form
        - Submit application
        - Confirm success
        - Stop if captcha appears
        """

        result = await asyncio.wait_for(
            agent.run(max_steps=100),
            timeout=600
        )

        print(f"Applied successfully: {url}")
        print(result)

    except Exception as e:
        print(f"Failed: {url}")
        print(str(e))
```

---

# 🧠 Agent Configuration (Factory Pattern)

Supports overrides instead of mutation:

```python
AgentFactory.create(task_override=..., files_override=...)
```

---

# 📄 Resume Handling

❗ No file upload required

Resume is automatically picked from:

```env
RESUME_PATH=./resume.pdf
```

Injected into agent:

```python
available_file_paths=[resume_path]
```

---

# 🧰 Custom Tools (Optional)

```python
@tools.action("Get resume data")
async def get_resume(browser_session):
    return {
        "name": "Heinz Doof",
        "skills": ["Java", "Spring Boot"]
    }
```

👉 Use tools only if:

* You need structured data (not just PDF)
* You integrate DB / APIs

---

# 👁️ Vision Mode

```python
use_vision=True
```

Useful for:

* Dynamic UI
* Form detection
* Complex layouts

---

# ⚡ Performance Tips

* Reduce `max_steps`
* Use smaller models for extraction
* Avoid unnecessary screenshots
* Reuse browser sessions

---

# ⚠️ Known Limitations

* ❌ CAPTCHA blocking
* ❌ Some sites detect automation
* ❌ LLM may misinterpret forms
* ❌ Multi-step flows may loop

---

# 🛠️ Best Practices

* Track applied jobs (avoid duplicates)
* Add retry logic
* Add domain restrictions
* Log every action for debugging

---

# 🔮 Future Improvements

* Telegram job trigger bot
* Job deduplication system
* Resume parser (PDF → structured JSON)
* Multi-agent orchestration

---

# 📜 License

MIT License

---

# 🙌 Contributing

PRs are welcome. Build cool stuff 🚀
