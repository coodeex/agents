import numpy as np
import sounddevice as sd
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline
from agents import Agent, trace
from pydub import AudioSegment
import io

# Initialize a basic agent for voice responses
voice_agent = Agent(
    name="Voice Agent",
    instructions="You are a helpful voice assistant that responds to user queries.",
)

async def voice_response(audio_data: bytes) -> bytes:
    """
    Process voice input and return voice response
    Args:
        audio_data: Raw audio data from Telegram voice message (OGG format)
    Returns:
        bytes: Audio response data
    """
    # Convert OGG to raw PCM using pydub
    audio_segment = AudioSegment.from_ogg(io.BytesIO(audio_data))
    
    # Convert to numpy array and ensure it's int16
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.sample_width == 2:  # 16-bit
        audio_array = samples.astype(np.int16)
    else:  # Convert to 16-bit
        audio_array = (samples * (32767 / samples.max())).astype(np.int16)
    
    # Create audio input
    audio_input = AudioInput(buffer=audio_array)
    
    # Initialize voice pipeline
    pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(voice_agent))
    
    # Process the voice input
    with trace("Voice Response"):
        result = await pipeline.run(audio_input)
    
    # Collect response audio chunks
    response_chunks = []
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            response_chunks.append(event.data)
    
    # Combine chunks into single response
    response_audio = np.concatenate(response_chunks, axis=0)
    
    # Convert to AudioSegment and then to OGG format
    response_segment = AudioSegment(
        response_audio.tobytes(), 
        frame_rate=audio_segment.frame_rate,
        sample_width=2,  # 16-bit
        channels=audio_segment.channels
    )
    
    # Export as OGG
    output = io.BytesIO()
    response_segment.export(output, format="ogg")
    return output.getvalue()
