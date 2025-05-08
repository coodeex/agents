#!/usr/bin/env python3

import os
import asyncio
from typing import List, Optional
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

# Example tool for demonstration
@function_tool
def get_weather(city: str):
    """Get the weather for a given city."""
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."

class AnthropicAssistant:
    def __init__(self, api_key: Optional[str] = None, model: str = "anthropic/claude-3-5-sonnet-latest"):
        """Initialize the Anthropic Assistant.
        
        Args:
            api_key: Anthropic API key. If not provided, will look for ANTHROPIC_API_KEY env variable
            model: Model to use, defaults to Claude 3 Sonnet
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable")
        
        self.model = model
        self.tools = [get_weather]  # Add more tools as needed
        
        # Initialize the agent
        self.agent = Agent(
            name="Assistant",
            instructions="You are a helpful and knowledgeable assistant. Answer questions clearly and concisely.",
            model=LitellmModel(model=self.model, api_key=self.api_key),
            tools=self.tools
        )

    async def get_response(self, prompt: str) -> str:
        """Get a response from the assistant for a given prompt."""
        try:
            result = await Runner.run(self.agent, prompt)
            return result.final_output
        except Exception as e:
            return f"Error getting response: {str(e)}"

async def interactive_session(assistant: AnthropicAssistant):
    """Run an interactive session with the assistant."""
    print("Welcome to Anthropic Assistant! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        try:
            prompt = input("\nYou: ").strip()
            if prompt.lower() in ['quit', 'exit']:
                break
            if not prompt:
                continue
                
            response = await assistant.get_response(prompt)
            print("\nAssistant:", response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
    
    print("\nGoodbye!")

async def main():
    # You can provide API key here or set it as an environment variable
    assistant = AnthropicAssistant()
    await interactive_session(assistant)

if __name__ == "__main__":
    asyncio.run(main()) 