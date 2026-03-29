# test_azure.py
import os
import httpx
import asyncio
from dotenv import load_dotenv
load_dotenv()

async def test():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    model = os.getenv("LLM_MODEL")

    url = f"{endpoint}/openai/deployments/{model}/chat/completions?api-version={api_version}"
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    body = {
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 50
    }

    print(f"Hitting: {url}")
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers=headers, json=body)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

asyncio.run(test())