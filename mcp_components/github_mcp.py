import os

from mcp import StdioServerParameters


class GitHubMCP:
    @staticmethod
    def get_params() -> StdioServerParameters:
        return StdioServerParameters(
            command="docker",
            args=[
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "ghcr.io/github/github-mcp-server:latest",
                "stdio",
            ],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")},
        )
