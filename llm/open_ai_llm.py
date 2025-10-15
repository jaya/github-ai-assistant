import json
import os

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from llm.prompt_loader import PromptLoader


class OpenAiSession:
    def __init__(self) -> None:
        self._load_system_prompts()
        self.messages: list[SystemMessage | HumanMessage | AIMessage] = [
            SystemMessage(content=p) for p in self.system_prompts
        ]

    def _load_system_prompts(self) -> None:
        self.system_prompt = PromptLoader.load_prompt("natural-github.txt")
        self.tools_prompt = PromptLoader.load_prompt("tools.json")
        self.identity_msg = {
            "type": "identity",
            "github_login": os.getenv("GITHUB_LOGIN"),
        }

        self.system_prompts = [
            self.system_prompt,
            json.dumps(self.tools_prompt),
            json.dumps(self.identity_msg),
        ]

    def ask(self, question: str) -> str:
        self.messages.append(HumanMessage(content=question))
        model_name = os.getenv("OPENAI_MODEL", "gpt-5")
        llm = ChatOpenAI(model=model_name)
        result = llm.invoke(self.messages)
        answer = (result.content or "").strip()
        self.messages.append(AIMessage(content=answer))
        return answer
