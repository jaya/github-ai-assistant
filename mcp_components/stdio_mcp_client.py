from contextlib import AsyncExitStack
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_components.mcp_call import MCPCall
from mcp_components.mcp_response import MCPResponse


class StdioMCPClient:
    def __init__(self, server_params: StdioServerParameters):
        self._server_params = server_params
        self._stack: AsyncExitStack | None = None
        self._session: ClientSession | None = None

    async def _ensure_session(self) -> None:
        if self._session is not None:
            return
        self._stack = AsyncExitStack()
        read, write = await self._stack.enter_async_context(stdio_client(self._server_params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()

    async def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        await self._ensure_session()
        result = await self._session.call_tool(tool_name, arguments)
        return result.model_dump()

    async def list_tools(self) -> list:
        await self._ensure_session()
        tools_response = await self._session.list_tools()
        return [tool.model_dump() for tool in tools_response.tools]

    async def execute(self, mcp_call: MCPCall) -> MCPResponse:
        if mcp_call.method == "tools/list":
            result = await self.list_tools()
            data = {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                "isError": False,
            }
        elif mcp_call.method == "tools/call":
            data = await self.execute_tool(mcp_call.tool_name, mcp_call.arguments)
        else:
            raise ValueError(f"Unsupported method: {mcp_call.method}")

        return MCPResponse(data)

    async def cleanup(self) -> None:
        if self._stack is not None:
            await self._stack.aclose()
            self._stack = None
            self._session = None
