from fastmcp import FastMCP

mcp = FastMCP("Weather Server")

@mcp.tool()

def get_weather(city):
    """ Return weather information"""



if __name__ == "__main__" : 
    print("Starting Weatehr MCP Server...")

mcp.run()