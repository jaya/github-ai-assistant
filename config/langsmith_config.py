import os


def setup_langsmith() -> None:
    """Setup LangSmith tracing if API key is configured."""
    api_key = os.getenv("LANGSMITH_API_KEY")
    project = os.getenv("LANGSMITH_PROJECT")

    if api_key and project:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = api_key
        os.environ["LANGCHAIN_PROJECT"] = project
        print(f"✅ LangSmith tracing enabled for project: {project}")
