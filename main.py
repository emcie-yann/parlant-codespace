import asyncio
import parlant.sdk as p
from guidelines import guidelines
from glossary import glossary
from journeys import journey

from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    async with p.Server(
        session_store="local",
        port=8820,
        migrate=True,
        log_level=p.LogLevel.TRACE,
    ) as server:
        agent = await server.create_agent(
            name="Haven",
            description=(
                "You are a luxury hotel reservation specialist and digital concierge. "
                "You are sophisticated, polite, funny, and proactive. "
                "Your goal is to curate perfect stays, handle bookings efficiently, "
                "and manage guest logistics with a warm, welcoming demeanor."
            ),
        )

        await glossary(agent)
        await guidelines(agent)
        await journey(agent)


asyncio.run(main())
