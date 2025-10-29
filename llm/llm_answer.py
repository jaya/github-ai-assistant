import json

from langchain_core.messages import AIMessage

from mcp_components.mcp_call import MCPCall


class LLMAnswer:
    def __init__(self, llm_result: AIMessage):
        raw_content = self._extract_raw_content(llm_result.content)
        json_content = self._try_parse_json(raw_content)

        if json_content:
            self._content = json_content
            self.structured = True
            content_type = json_content.get("type")
        else:
            self._content = raw_content
            self.structured = False
            content_type = None

        self.tool_call = content_type == "tool_call"
        self.final_answer = content_type == "final_answer"
        self.plain_text = not self.structured

    @staticmethod
    def _extract_raw_content(content: str | list[str | dict] | None) -> str:
        if isinstance(content, list):
            return "".join(str(item) for item in content).strip()
        return (content or "").strip()

    @staticmethod
    def _try_parse_json(text: str) -> dict | None:
        cleaned = text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None

    def text(self) -> str:
        if self.final_answer:
            return self._content.get("answer_markdown", "")
        if self.plain_text:
            return self._content
        return ""

    def raw_content(self) -> str:
        if self.plain_text:
            return self._content
        return json.dumps(self._content)

    def mcp_call(self) -> MCPCall | None:
        if not self.tool_call:
            return None
        return MCPCall(
            method=self._content.get("method"),
            tool_name=self._content.get("tool_name"),
            arguments=self._content.get("arguments"),
        )
