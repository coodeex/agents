from agents import Agent, Runner, WebSearchTool

agent = Agent(
    name="WebSearchAgent",
    tools=[WebSearchTool()],
)

async def main():
    result = await Runner.run(agent, "What's the latest news on AI?")
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())