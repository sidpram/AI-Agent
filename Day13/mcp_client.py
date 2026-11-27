from fastmcp import Client
from pathlib import Path

# Comments on this file are only for understanding and not for MCP
async def connect(server):
    """Connect to the MCP Server."""

    client = Client(Path(server)) 
    await client.__aenter__()
    print(f"Connected to MCP {server}.")

    return client


async def disconnect(client):
    """ Close the MCP connection. """

    await client.__aexit__(
        None,
        None,
        None
    )


async def discover_tools(client):
    """ Retrieve all tools from the server."""

    tools = await client.list_tools()
    return tools


async def execute_tool(
    client,
    tool_name,
    arguments=None):
    """ Execute a tool."""

    if arguments is None:
        arguments = {}

    result = await client.call_tool(
        tool_name,
        arguments
    )

    return result