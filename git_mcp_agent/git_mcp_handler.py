import os
from agents import Agent, Runner, ItemHelpers, trace
from agents.mcp import MCPServerStdio

async def get_git_mcp_response(message: str, repo_path: str) -> str:
    # Run the git MCP server as a subprocess
    async with MCPServerStdio(
        params={"command": "uvx", "args": ["mcp-server-git"]}
    ) as server:
        # Create the agent with the MCP server
        agent = Agent(
            name="Git Assistant",
            instructions=f"Answer questions about the git repository at {repo_path}, use that for repo_path",
            mcp_servers=[server]
        )

        # Run the agent with the message
        with trace("Git MCP response"):
            result = await Runner.run(agent, message)
            return ItemHelpers.text_message_outputs(result.new_items)