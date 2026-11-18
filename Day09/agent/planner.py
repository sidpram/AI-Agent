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


def planner(state, tools):

    tool_descriptions = build_tool_descriptions(tools)
    prompt = f"""
    you are an AI planner.
    You job is to decide ONLY the next action.
    User Request: 
    {state["user_request"]}
    Completed Action:
    {state["action"]}
    Previous Observation:
    {state["observation"]}
    Available tools:
    {tool_descriptions}

Rules:
1. Select the best tool.
    2. Reply ONLY with the tool name.
    3. Do not explain.

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