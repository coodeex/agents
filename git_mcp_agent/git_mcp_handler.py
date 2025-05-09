import asyncio
import shutil
from pydantic import BaseModel
from agents import Agent, Runner, trace, InputGuardrail, GuardrailFunctionOutput
from agents.mcp import MCPServer, MCPServerStdio


class GitOperationOutput(BaseModel):
    is_read_only: bool
    reasoning: str


git_guardrail_agent = Agent(
    name="Git Guardrail",
    instructions="Check if the user's request involves any write operations to the git repository (like push, commit, modify files, add comments etc). Any write operation should be flagged as not read-only.",
    output_type=GitOperationOutput,
)


async def git_readonly_guardrail(ctx, agent, input_data):
    result = await Runner.run(git_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(GitOperationOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_read_only,
    )


async def run(mcp_server: MCPServer, directory_path: str):
    agent = Agent(
        name="Assistant",
        instructions=f"Answer questions about the git repository at {directory_path}, use that for repo_path",
        mcp_servers=[mcp_server],
        input_guardrails=[
            InputGuardrail(guardrail_function=git_readonly_guardrail),
        ],
    )

    message = "Who's the most frequent contributor?"
    print("\n" + "-" * 40)
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    message = "Summarize the last change in the repository."
    print("\n" + "-" * 40)
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    # Ask the user for the directory path
    directory_path = input("Please enter the path to the git repository: ")

    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        params={"command": "uvx", "args": ["mcp-server-git"]},
    ) as server:
        with trace(workflow_name="MCP Git Example"):
            await run(server, directory_path)


if __name__ == "__main__":
    if not shutil.which("uvx"):
        raise RuntimeError("uvx is not installed. Please install it with `pip install uvx`.")

    asyncio.run(main())