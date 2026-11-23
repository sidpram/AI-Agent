import asyncio

from mcp_client import (
    connect,
    disconnect,
    discover_tools
)

from planner import planner
from executor import execute_action
from loop import run_agent_loop
from answer import format_answer
from memory import create_database

async def main():

    create_database()
    client = await connect()

    tools = await discover_tools(client)

    print()
    print("Available Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)

    user_request = input("\nUser : ")

    while user_request != "quit" and user_request != "bye":
        state = await run_agent_loop(
            user_request,
            planner,
            execute_action,
            format_answer,
            tools,
            client
        )

        print("\nFinal Answer")
        print("------------")

        print(
            state["final_answer"]
        )
        user_request = input("\nUser : ")
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())