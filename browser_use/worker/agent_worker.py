import asyncio
import os
import json
from config.settings import Settings
from config.agent_config import AgentFactory
from config.env import get_env


def get_resume_context() -> tuple[str, str]:
    """
    Returns (resume_section_for_task, resume_path_or_none)
    Raises if neither resume path nor resume data is configured.
    """
    use_resume_data = get_env("USE_RESUME_DATA", "false").lower() == "true"

    if use_resume_data:
        resume_data_raw = get_env("RESUME_DATA")
        if not resume_data_raw:
            raise ValueError("USE_RESUME_DATA=true but RESUME_DATA is not set in .env")
        try:
            resume_data = json.loads(resume_data_raw)
        except json.JSONDecodeError:
            raise ValueError("RESUME_DATA in .env is not valid JSON")

        print("Using resume JSON data from env")
        section = f"""
        RESUME DATA (JSON — use this instead of reading a PDF):
        {json.dumps(resume_data, indent=2)}

        Use the above JSON directly to fill all form fields.
        Do NOT try to open or read any PDF file.
        """
        return section, None

    else:
        resume_path = Settings.get_resume_path()
        if not resume_path:
            raise ValueError("Neither USE_RESUME_DATA nor RESUME_PATH is configured in .env")
        if not os.path.exists(resume_path):
            raise ValueError(f"Resume PDF not found at: {resume_path}")

        print(f"Using resume PDF at: {resume_path}")
        section = f"""
        RESUME: {resume_path}
        Upload this PDF and use it to autofill and extract candidate details.
        """
        return section, resume_path


async def run_agent_task(url: str):
    try:
        resume_section, resume_path = get_resume_context()

        task = f"""
        You are an autonomous job application agent. Your goal is to fully complete and submit a job application.

        JOB URL: {url}

        {resume_section}

        CANDIDATE DETAILS:
        - Extract name, email, phone from resume
        - For Job Experience if "Present" is listed for a company, the candidate is currently working there
        - Gender: Male
        - Race/Ethnicity: Asian / Asian Indian
        - Religion: Hindu
        - Nationality: Indian
        - Previously employed by this company: No
        - Government affiliated: No
        - Disability: No / I do not have a disability
        - Veteran status: I am not a veteran / Not a protected veteran / None of the above
        - Work authorization: Yes, authorized to work
        - Sponsorship required: No

        CREDENTIALS FOR ACCOUNT CREATION (if required):
        - Email: use the email from the resume
        - Password: Life@is@2
        - Use the candidate's name from the resume for any name fields

        STEP BY STEP INSTRUCTIONS:

        1. NAVIGATE to the job URL
        2. CLICK "Apply" or "Apply Now" button
        3. ACCOUNT STEP (if required):
           - If sign in page appears, try creating a new account first
           - Use email extracted from resume + password: Life@is@2
           - Check any "I agree to terms" checkbox before submitting
           - If account already exists, sign in with same credentials
        4. RESUME UPLOAD:
           - If "Autofill with Resume" or "Upload Resume" option exists, use it
           - If using PDF: upload from {resume_path if resume_path else "N/A"}
           - If using JSON data: skip upload, fill fields manually from JSON
           - Wait for autofill to complete before proceeding
        5. MY INFORMATION:
           - Fill all personal details using resume data (name, email, phone, address)
           - Ensure all required fields marked with * are filled
        6. PHONE NUMBER FORMATTING RULES (CRITICAL):
           - Country Phone Code field is SEPARATE from Phone Number field
           - If "Country Phone Code" dropdown exists, select India (+91) there
           - In the "Phone Number" field enter ONLY the 10 digit number
           - Do NOT enter +91 or 91 or any country code in the Phone Number field
           - Do NOT enter hyphens or spaces unless the field explicitly requires it
           - If there is only one phone field with no country code dropdown, enter with +91 prefix
        7. MY EXPERIENCE:
           - Fill work experience from resume
           - Fill education details from resume
           - Fill skills from resume
        8. APPLICATION QUESTIONS:
           - "How did you hear about us?" → select "LinkedIn" or "Job Board" or closest option
           - "Previously employed here?" → No
           - "Are you a current employee?" → No
           - "Authorized to work?" → Yes
           - "Require sponsorship?" → No
           - "Government employee or affiliated?" → No
           - Any other yes/no eligibility questions → answer based on resume or select No
        9. VOLUNTARY DISCLOSURES:
           - Gender → Male
           - Disability → No / I do not have a disability
           - Veteran status → I am not a veteran / Not a protected veteran / None of the above
           - Race/Ethnicity → Asian / Asian Indian
           - Religion → Hindu (if asked)
           - Nationality → Indian (if asked)
           - Any other voluntary fields → Prefer not to disclose
           - Click if found where you need to acknowledge terms and conditions
        10. REVIEW:
            - Review all filled information
            - Fix any errors shown on the page before submitting
            - If phone number error appears, clear the field and re-enter ONLY the 10 digits
            - Click Submit
        11. CONFIRM success message appears

        ERROR HANDLING RULES:
        - If a field shows an error, read the error message carefully and fix it
        - If phone number format error appears → clear field → enter only 10 digits without country code
        - If a required field is empty → fill it using resume data or candidate details above
        - If dropdown has no exact match → pick the closest option
        - Always scroll down to check for more fields before submitting

        STOP CONDITIONS:
        - STOP if captcha appears
        - STOP if OTP or phone verification is required
        - Do NOT stop for account creation — handle it using credentials above
        - If a field is optional and data is unavailable, leave it blank
        """

        agent = AgentFactory.create(
            task_override=task,
            resume_path=resume_path
        )

        result = await asyncio.wait_for(
            agent.run(int(get_env("MAX_STEPS", 100))),
            timeout=int(get_env("TIME_OUT", 600))
        )

        print(f"Applied successfully: {url}")
        print(result)

    except ValueError as e:
        print(f"Configuration error: {e}")

    except Exception as e:
        print(f"Failed: {url}")
        print(str(e))