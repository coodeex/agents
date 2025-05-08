import os
import asyncio
from typing import Optional, Tuple
from agents import Agent, Runner, ItemHelpers, trace, WebSearchTool
from agents.extensions.models.litellm_model import LitellmModel


# Initialize agents with different models
claude_agent = Agent(
    name="claude_agent",
    model=LitellmModel(
        model="anthropic/claude-3-5-sonnet-latest",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
)

web_search_agent = Agent(
    name="WebSearchAgent",
    tools=[WebSearchTool()],
)

openai_agent = Agent(
    name="openai_agent",
    model="gpt-4o-mini",
    handoffs=[web_search_agent]
)

async def get_parallel_responses(message: str) -> Tuple[str, str]:
    # Run both models in parallel within a single trace
    with trace("Parallel model responses"):
        claude_res, openai_res = await asyncio.gather(
            Runner.run(
                claude_agent,
                message,
            ),
            Runner.run(
                openai_agent,
                message,
            ),
        )

        claude_response = ItemHelpers.text_message_outputs(claude_res.new_items)
        openai_response = ItemHelpers.text_message_outputs(openai_res.new_items)

        return claude_response, openai_response 