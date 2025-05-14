import os
from typing import Optional
from agents import Agent, Runner, ItemHelpers, trace, WebSearchTool, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from dataclasses import dataclass
from asyncio import Lock

@dataclass
class StreamingState:
    text: str = ""
    is_complete: bool = False
    lock: Lock = Lock()

# Initialize the OpenAI agent
openai_agent = Agent(
    name="streaming_agent",
    model="gpt-4o-mini",  # You can adjust the model as needed
    instructions="""You are a helpful assistant that provides detailed and thoughtful responses.
    Your responses should be well-structured and informative."""
)

async def get_streaming_response(message: str, state: StreamingState):
    """
    Get streaming response from the OpenAI agent and update the shared state.
    
    Args:
        message: The user's input message
        state: Shared state object for storing the accumulated text
    """
    with trace("Streaming response"):
        result = Runner.run_streamed(openai_agent, message)
        
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                chunk = event.data.delta
                if chunk:  # Only process non-empty chunks
                    async with state.lock:
                        state.text += chunk
        
        # Mark streaming as complete
        async with state.lock:
            state.is_complete = True 