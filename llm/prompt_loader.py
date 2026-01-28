import os


class PromptLoader:
    @staticmethod
    def load_prompt(filename: str) -> str:
        path = os.path.join("llm/prompts", filename)
        with open(path, encoding="utf-8") as f:
            return f.read()
