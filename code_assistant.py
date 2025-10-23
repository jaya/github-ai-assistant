from conversation_loop import ConversationLoop
from llm.llm_answer import LLMAnswer
from llm.llm_session import LLMSession
from mcp_components.github_mcp import GitHubMCP
from mcp_components.stdio_mcp_client import StdioMCPClient


class CodeAssistant:
    def __init__(self) -> None:
        self.mcp_client = StdioMCPClient(GitHubMCP.get_params())
        self.llm_session: LLMSession | None = None

    @classmethod
    async def create(cls) -> "CodeAssistant":
        assistant = cls()
        await assistant._initialize()
        return assistant

    async def _initialize(self) -> None:
        tools_list = await self.mcp_client.list_tools()
        print(f"✅ {len(tools_list)} tools carregadas do MCP")

        self.llm_session = LLMSession(tools_list)

    async def start_conversation(self) -> None:
        loop = ConversationLoop()
        await loop.run(self.ask, self.mcp_client.cleanup)

    async def ask(self, question: str) -> str:
        answer = self.llm_session.ask(question)
        result = await self._process(answer)
        return result

    async def _process(self, answer: LLMAnswer) -> str:
        if answer.tool_call:
            mcp_call = answer.mcp_call()
            print(f"MCP request: {mcp_call}")

            mcp_response = await self.mcp_client.execute(mcp_call)
            next_answer = self.llm_session.ask(mcp_response.text())
            return await self._process(next_answer)

        return answer.text()
