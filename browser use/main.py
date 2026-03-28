import asyncio
from config.settings import Settings

async def main():
    agent = Settings.get_agent()

    result = await agent.run(
        max_steps=100
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())