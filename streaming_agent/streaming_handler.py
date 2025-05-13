import os
from typing import Optional
from agents import Agent, Runner, ItemHelpers, trace, WebSearchTool, function_tool
from openai.types.responses import ResponseTextDeltaEvent

# Initialize the OpenAI agent
openai_agent = Agent(
    name="streaming_agent",
    model="gpt-4o-mini",  # You can adjust the model as needed
    instructions="""You are a helpful assistant that provides detailed and thoughtful responses.
    Your responses should be well-structured and informative."""
)

async def get_streaming_response(message: str, callback):
    """
    Get streaming response from the OpenAI agent.
    
    Args:
        message: The user's input message
        callback: Async function to call with each chunk of the response
    """
    with trace("Streaming response"):
        accumulated_text = ""
        result = Runner.run_streamed(openai_agent, message)
        
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                chunk = event.data.delta
                if chunk:  # Only process non-empty chunks
                    accumulated_text += chunk
                    await callback(accumulated_text)
        
        return accumulated_text 