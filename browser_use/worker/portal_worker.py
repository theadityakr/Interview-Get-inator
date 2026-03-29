import asyncio
import os
import json
from config.settings import Settings
from config.agent_config import AgentFactory
from config.env import get_env


def get_resume_data() -> dict:
    resume_data_raw = get_env("RESUME_DATA")
    if not resume_data_raw:
        raise ValueError("RESUME_DATA is not set in .env")
    return json.loads(resume_data_raw)


async def run_portal_task(url: str, max_jobs: int, max_minutes: int, service=None):
    resume_data = get_resume_data()
    resume_json = json.dumps(resume_data, indent=2)

    cdp_url = get_env("CHROME_CDP_URL", "http://localhost:9222")

    task = f"""
    You are an autonomous job portal agent. Your goal is to log in to a job portal and apply to as many relevant jobs as possible.

    PORTAL URL: {url}

    RESUME DATA:
    {resume_json}

    BROWSER NOTE:
    - You are using the user's real Chrome browser session
    - Cookies and existing logins are preserved
    - Do NOT clear cookies or log out

    STEP BY STEP INSTRUCTIONS:

    1. NAVIGATE to {url}

    2. LOGIN STEP:
       - If already logged in → skip to step 3
       - If login required:
         * Try "Sign in with Google" first → select {resume_data.get('email')} from Google account picker
         * If Google sign-in not available → use email/password: {resume_data.get('email')} / Life@is@2
         * Wait for login to complete

    3. NAVIGATE TO JOBS SECTION:
       - Go to Jobs / Search Jobs section
       - Search for relevant roles: Based on the Candidates experience and skills
       - Filter by: Experience , Locations: based on the candidates resume data

    4. APPLY TO JOBS LOOP (repeat until {max_jobs} jobs applied or {max_minutes} minutes elapsed):
       - Scan the job listings
       - For each job:
         a. Check if job matches tech stack (Java/Spring Boot/Python/Backend)
         b. Check if job is relevant for 1-3 years experience
         c. If relevant → click Apply
         d. Fill application form using resume data
         e. For any compensation fields: use the candidates data
         f. Submit application
         g. Note job title and company
         h. Go back to job listings
         i. Move to next job
       - Skip jobs that:
         * Require 5+ years experience
         * Are for completely different tech stacks (mobile, frontend only, ML only)
         * Have already been applied to (check for "Applied" badge)

    5. DROPDOWN HANDLING (CRITICAL):
       - Always click from dropdown suggestions, never just type
       - For city fields: type → wait → click matching option
       - For skills: select from available tags/chips

    6. PHONE NUMBER RULES:
       - If country code dropdown exists → select India (+91) → enter only candidates phone number
       - If single field → enter  phone number

    7. STOP when any of these conditions are met:
       - {max_jobs} jobs applied successfully
       - {max_minutes} minutes have elapsed
       - Captcha appears
       - OTP/phone verification required
       - No more relevant jobs found

    TRACKING:
    - Keep count of jobs applied
    - At the end, report: total applied, job titles, companies

    VOLUNTARY DISCLOSURES (if asked):
    - Gender: Male
    - Disability: No
    - Veteran: No
    - Race: Asian / Asian Indian
    """

    agent = AgentFactory.create_with_cdp(
        task_override=task,
        cdp_url=cdp_url
    )

    timeout = max_minutes * 60 + 60  # extra 60s buffer

    result = await asyncio.wait_for(
        agent.run(int(get_env("MAX_STEPS", 200))),
        timeout=timeout
    )

    return str(result)