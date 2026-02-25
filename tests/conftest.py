from __future__ import annotations

import asyncio
import uuid

from dotenv import load_dotenv
import pytest

from code_assistant import CodeAssistant
from config.langsmith_config import setup_langsmith


load_dotenv()
setup_langsmith()


@pytest.fixture(scope="session")
def _assistant():  # noqa: ANN202
    loop = asyncio.new_event_loop()
    assistant = loop.run_until_complete(CodeAssistant.create())
    yield assistant, loop
    loop.run_until_complete(assistant.mcp_client.cleanup())
    loop.close()


@pytest.fixture
def ask(_assistant):  # noqa: ANN201
    assistant, loop = _assistant
    assistant.thread_id = str(uuid.uuid4())
    return lambda q: loop.run_until_complete(assistant.ask(q))
