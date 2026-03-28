from browser_use import Tools, ActionResult

tools = Tools()

@tools.action("Get resume data")
async def get_resume(browser_session):
    return ActionResult(
        extracted_content={
            "name": "Aditya Kumar",
            "skills": ["Java", "Spring Boot"]
        }
    )