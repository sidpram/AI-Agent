import asyncio

from mcp_manager import (
    create_tool_registry,
    run_tool,
    close_servers
)

async def main():

    servers = [
        "time-mcp-server/server.py",
        "weather-mcp-server/server.py"
    ]

    clients, tool_registry = (
        await create_tool_registry(
            servers
        )
    )

    try:
        print("\nAvailable Tools")
        print("----------------")

        for tool_name in tool_registry:
            print(tool_name)

        user_input = input("Enter City Name :")
        result = await run_tool(
            tool_registry,
            "get_weather",
            {"city": user_input}
        )

        print("\nTool Result:")
        print(result.content[0].text)

        result = await run_tool(
            tool_registry,
            "get_weather_forecast",
            {"city": user_input, "days": 3}
        )

        print("\nTool Result:")
        print(result.content[0].text)
        
    finally:
        await close_servers(
            clients
        )

if __name__ == "__main__":
    asyncio.run(main())