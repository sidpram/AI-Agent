from mcp_client import execute_tool

async def execute_action(action, state, client):

    # Step 4: Now call the client to call the tool name with query
    
        tool_result = await execute_tool(
                client,
                action
            )