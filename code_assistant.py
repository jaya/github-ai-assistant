from __future__ import annotations

import os
import uuid

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import MemorySaver

from conversation_loop import ConversationLoop
from llm.prompt_loader import PromptLoader
from mcp_components.github_mcp import GitHubMCP
from mcp_components.stdio_mcp_client import StdioMCPClient


class CodeAssistant:
    def __init__(self) -> None:
        self.mcp_client = StdioMCPClient(GitHubMCP.get_params())
        self.agent = None
        self.thread_id = str(uuid.uuid4())

    @classmethod
    async def create(cls) -> CodeAssistant:
        assistant = cls()
        await assistant._initialize()
        return assistant

    async def _initialize(self) -> None:
        await self.mcp_client.connect()
        tools = await load_mcp_tools(self.mcp_client.session)
        print(f"✅ {len(tools)} tools loaded from MCP")

        llm = _build_chat_model()
        system_prompt = _load_system_prompt()
        memory = MemorySaver()

        for tool in tools:
            tool.handle_tool_error = True

        self.agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt,
            checkpointer=memory,
        )

    async def start_conversation(self) -> None:
        loop = ConversationLoop()
        await loop.run(self.ask, self.mcp_client.cleanup)

    async def ask(self, question: str) -> str:
        config = {"configurable": {"thread_id": self.thread_id}}
        result = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=question)]},
            config=config,
        )

        return result["messages"][-1].content


def _build_chat_model() -> BaseChatModel:
    model = os.getenv("LLM_MODEL", "gemini-2.0-flash-exp")
    provider = os.getenv("LLM_PROVIDER")
    if provider:
        return init_chat_model(model, model_provider=provider, temperature=0)
    return init_chat_model(model, temperature=0)


def _load_system_prompt() -> str:
    template = PromptLoader.load_prompt("react-github.txt")
    return template.format(github_login=os.getenv("GITHUB_LOGIN", "unknown"))
