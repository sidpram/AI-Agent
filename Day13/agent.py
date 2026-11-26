import asyncio

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load configuration
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

from mcp_client import (
    connect,
    disconnect,
    discover_tools,
    execute_tool
)

# Build Tool Descriptions
def build_tool_descriptions(tools):

    descriptions = ""
    for tool in tools:
        descriptions += f"""
Tool:
{tool.name}

Description:
{tool.description}
----------------------------
"""

    return descriptions


def finalExecution(user_request, tools_result):
    prompt = f"""
    User asked: {user_request}
    Result: {tools_result}
    answer naturally
    """
    response = client.chat.completions.create (

        model= os.getenv("MODEL"),

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    #Ollama returns the tool name
    result = response.choices[0].message.content

    return result.strip()




def planner(user_request, tools):

    tool_descriptions = build_tool_descriptions(
        tools
    )

    ###Then create a prompt by combining user input and Tool Description.  and Give this prompt to Ollama. ###

    prompt = f"""
    You are an AI Planner.

    Available Tools

    {tool_descriptions}

    Instructions

    1. Select the best tool.
    2. Reply ONLY with the tool name.
    3. Do not explain.

    User Request

    {user_request}
    """
    # Give this prompt to ollama
    response = client.chat.completions.create (

        model= os.getenv("MODEL"),

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

#Ollama returns the tool name
    tool_name = response.choices[0].message.content

    return tool_name.strip()

async def main():
# Step 1: Connect to the MCP Server.
    client = await connect()

    # Step 2: Discover all available tools.
    tools = await discover_tools(
        client
    )
    print()
    print("Available Tools")
    print("----------------")

    for tool in tools:
        print(tool.name, ":")
        print(tool.description)
        print()
    print() 

    # Step 3: Take user input

    user_request = input("User:")

    tool_name = planner(user_request, tools)

    print()

    print( "Planner Selected:", tool_name)

    # Step 4: Now call the client to call the tool name with query

    tool_result = await execute_tool(
            client,
            tool_name
        )

   # print(tool_result)

    # Step 5 send the result to llm to get the result
    result = finalExecution(user_request, tool_result)
    print(result)
    
    await disconnect( client )

if __name__ == "__main__":
    asyncio.run(main())