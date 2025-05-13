import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, ItemHelpers, function_tool
import random
import time

# Define a simple tool that returns a random number of jokes
@function_tool
def how_many_jokes() -> int:
    """Returns a random number between 1 and 5"""
    return random.randint(1, 5)

async def stream_raw_responses():
    """Example of streaming raw responses (token by token)"""
    print("\n=== Raw Response Streaming Example ===")
    agent = Agent(
        name="Joker",
        instructions="""You are a helpful assistant that tells detailed jokes. 
        Each joke should be at least 3-4 sentences long with setup and punchline.
        Add line breaks between jokes for readability.""",
    )

    result = Runner.run_streamed(agent, input="Tell me 3 detailed jokes. Make them long with good setups.")
    print("\nStarting to stream jokes token by token:\n")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    print("\n")

async def stream_run_items():
    """Example of streaming run items (higher level events)"""
    print("\n=== Run Items Streaming Example ===")
    agent = Agent(
        name="Joker",
        instructions="""First call the `how_many_jokes` tool to determine the number of jokes.
        Tell detailed jokes with good setups and punchlines.
        Each joke should be at least 3-4 sentences long.""",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(agent, input="Tell me some detailed jokes with pauses between them!")
    print("Run starting...")

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("🔧 Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"📤 Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"💬 Message output:\n{ItemHelpers.text_message_output(event.item)}")
                print("\n")  # Add extra line break for readability

    print("Run complete!")

async def main():
    # Run both examples
    await stream_raw_responses()
    await stream_run_items()

if __name__ == "__main__":
    asyncio.run(main()) 