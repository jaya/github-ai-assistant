import os


def setup_langsmith() -> None:
    """Setup LangSmith tracing if enabled and API key is configured.

    Environment variables:
        LANGSMITH_API_KEY: API key for LangSmith
        LANGSMITH_PROJECT: Project name in LangSmith
        TRACING_ENABLED: Set to "false" to disable tracing (default: true)
    """
    tracing_enabled = os.getenv("TRACING_ENABLED", "true").lower() not in {"false", "0", "no"}
    api_key = os.getenv("LANGSMITH_API_KEY")
    project = os.getenv("LANGSMITH_PROJECT")

    if not tracing_enabled:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        return

    if api_key and project:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = api_key
        os.environ["LANGCHAIN_PROJECT"] = project
        print(f"✅ LangSmith tracing enabled for project: {project}")
