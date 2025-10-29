from dataclasses import dataclass


@dataclass
class MCPCall:
    method: str
    tool_name: str | None
    arguments: dict | None

    def __str__(self) -> str:
        return f"method={self.method}, tool={self.tool_name}, args={self.arguments}"
