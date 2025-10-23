import asyncio

from dotenv import load_dotenv

from code_assistant import CodeAssistant
from config.langsmith_config import setup_langsmith


# Load environment variables from .env file
load_dotenv()

# Setup LangSmith tracing
setup_langsmith()


async def main() -> None:
    assistant = await CodeAssistant.create()
    await assistant.start_conversation()


if __name__ == "__main__":
    asyncio.run(main())
