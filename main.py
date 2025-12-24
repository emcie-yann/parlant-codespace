import asyncio
import parlant.sdk as p
from dotenv import load_dotenv
load_dotenv()



async def main():
  async with p.Server(
    session_store='local',
    port=8800,
    migrate=True,
    log_level=p.LogLevel.TRACE,
  ) as server:
    agent = await server.create_agent(
        name="Otto Carmen",
        description="You work at a car dealership",
    )

asyncio.run(main())