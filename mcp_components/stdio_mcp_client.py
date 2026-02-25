from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class StdioMCPClient:
    def __init__(self, server_params: StdioServerParameters):
        self._server_params = server_params
        self._stack: AsyncExitStack | None = None
        self._session: ClientSession | None = None

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            raise RuntimeError("Session not initialized. Call connect() first.")
        return self._session

    async def connect(self) -> None:
        if self._session is not None:
            return
        self._stack = AsyncExitStack()
        read, write = await self._stack.enter_async_context(stdio_client(self._server_params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()

    async def cleanup(self) -> None:
        if self._stack is not None:
            try:
                await self._stack.aclose()
            except RuntimeError as e:
                print(f"⚠️ Cleanup warning: {e}")
            self._stack = None
            self._session = None
