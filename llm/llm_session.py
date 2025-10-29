import json
import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from llm.llm_answer import LLMAnswer
from llm.prompt_loader import PromptLoader


class LLMSession:
    def __init__(self, tools_list: list) -> None:
        self._load_system_prompts(tools_list)
        self.system_messages = [SystemMessage(content=p) for p in self.system_prompts]
        self.messages: list[HumanMessage | AIMessage] = []
        self.llm = self._create_llm()

    def _load_system_prompts(self, tools_list: list) -> None:
        system_prompt = PromptLoader.load_prompt("natural-github.txt")
        identity_msg = {
            "type": "identity",
            "github_login": os.getenv("GITHUB_LOGIN"),
        }
        tools_data = {"type": "tools_list", "tools": tools_list}

        self.system_prompts = [
            system_prompt,
            json.dumps(tools_data),
            json.dumps(identity_msg),
        ]

    @staticmethod
    def _create_llm() -> BaseChatModel:
        model = os.getenv("LLM_MODEL", "gemini-2.0-flash-exp")
        provider = os.getenv("LLM_PROVIDER")

        if provider:
            return init_chat_model(model, model_provider=provider, temperature=0)
        return init_chat_model(model, temperature=0)

    def ask(self, question: str) -> LLMAnswer:
        self.messages.append(HumanMessage(content=question))

        full_messages = self.system_messages + self.messages
        result = self.llm.invoke(full_messages)
        answer = LLMAnswer(result)

        self.messages.append(AIMessage(content=answer.raw_content()))

        return answer
