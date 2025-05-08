#!/usr/bin/env python3

import os
import asyncio
from typing import Optional
from agents import Agent, Runner, ItemHelpers, trace
from agents.extensions.models.litellm_model import LitellmModel

# Initialize agents with different models
claude_agent = Agent(
    name="claude_agent",
    model=LitellmModel(
        model="anthropic/claude-3-5-sonnet-latest",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
)

openai_agent = Agent(
    name="openai_agent",
    model="gpt-4o-mini"
)

async def main():
    msg = input("Enter your message to send to both Claude and GPT-4:\n\n")

    # Run both models in parallel within a single trace
    with trace("Parallel model responses"):
        claude_res, openai_res = await asyncio.gather(
            Runner.run(
                claude_agent,
                msg,
            ),
            Runner.run(
                openai_agent,
                msg,
            ),
        )

        outputs = {
            "Claude": ItemHelpers.text_message_outputs(claude_res.new_items),
            "GPT-4": ItemHelpers.text_message_outputs(openai_res.new_items),
        }

        # Print individual responses
        print("\n=== Claude's Response ===")
        print(outputs["Claude"])
        print("\n=== GPT-4's Response ===")
        print(outputs["GPT-4"])

if __name__ == "__main__":
    asyncio.run(main()) 