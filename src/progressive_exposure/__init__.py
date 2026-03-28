import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables before importing the agent,
# as the orchestrator reads them at import time.
load_dotenv(Path(__file__).parent / "agents" / ".env")

from progressive_exposure.agents.orchestrator import agent  # noqa: E402


async def main() -> None:
    """Runs the orchestrator agent in an interactive CLI loop."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)

    logger.info("Orchestrator agent ready. Type 'exit' to quit.")
    session = agent.create_session()
    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip().lower() in ("exit", "quit"):
            break

        response_stream = agent.run(user_input, stream=True, session=session)
        async for update in response_stream:
            print(update.text, end="", flush=True)
        print()

        response = await response_stream.get_final_response()
        logger.info("Agent: %s", response.text)


def cli() -> None:
    """Sync entry point for the console script."""
    asyncio.run(main())
