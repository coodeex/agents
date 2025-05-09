import os
import time
import subprocess
from pathlib import Path
from pydantic import BaseModel
from agents import Agent, Runner, ItemHelpers, trace, InputGuardrail, GuardrailFunctionOutput
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

# Global variable to track last pull time
_last_pull_time = 0

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


async def get_git_mcp_response(message: str) -> str:
    global _last_pull_time
    repo_path = os.getenv("GIT_MCP_REPO_PATH")
    if not repo_path:
        raise ValueError("Please set GIT_MCP_REPO_PATH in your .env file")

    # Check if we need to pull (if more than 60 seconds have passed)
    current_time = time.time()
    if current_time - _last_pull_time > 60:
        script_dir = Path(__file__).parent
        pull_script = script_dir / "git_pull.sh"
        try:
            subprocess.run([str(pull_script), repo_path], check=True)
            _last_pull_time = current_time
        except subprocess.CalledProcessError as e:
            print(f"Warning: Git pull failed with error: {e}")

    # Run the git MCP server as a subprocess
    async with MCPServerStdio(
        params={"command": "uvx", "args": ["mcp-server-git"]}
    ) as server:
        # Create the agent with the MCP server and guardrails
        agent = Agent(
            name="Git Assistant",
            instructions=f"Answer questions about the git repository at {repo_path}, use that for repo_path",
            mcp_servers=[server],
            input_guardrails=[
                InputGuardrail(guardrail_function=git_readonly_guardrail),
            ],
        )

        # Run the agent with the message
        with trace("Git MCP response"):
            result = await Runner.run(agent, message)
            return ItemHelpers.text_message_outputs(result.new_items)