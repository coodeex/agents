# Requires libportaudio2
# %%
import numpy as np
import sounddevice as sd
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline
from agents import Agent, trace

basic_agent = Agent(
    name="Basic Agent",
    instructions="You are a helpful agent.",
)

async def voice_agent():
    samplerate = sd.query_devices(kind='input')['default_samplerate']

    while True:
        pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(basic_agent))

        # Check for input to either provide voice or exit
        cmd = input("Press Enter to speak your query (or type 'q' + Enter to exit): ")
        if cmd.lower() == "q":
            print("Exiting...")
            break      
        print("Listening ... press Enter to stop")
        recorded_chunks = []

         # Start streaming from microphone until Enter is pressed
        with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16', callback=lambda indata, frames, time, status: recorded_chunks.append(indata.copy())):
            input()

        print("Reasoning...")

        # Concatenate chunks into single buffer
        recording = np.concatenate(recorded_chunks, axis=0)

        # Input the buffer and await the result
        audio_input = AudioInput(buffer=recording)

        with trace("Voice Agent"):
            result = await pipeline.run(audio_input)

         # Transfer the streamed result into chunks of audio
        response_chunks = []
        async for event in result.stream():
            if event.type == "voice_stream_event_audio":
                response_chunks.append(event.data)

        response_audio = np.concatenate(response_chunks, axis=0)

        # Play response
        print("Agent is responding...")
        sd.play(response_audio, samplerate=samplerate)
        sd.wait()
        print("---")

async def main():
    await voice_agent()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 