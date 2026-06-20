
from fastmcp import FastMCP
mcp=FastMCP("mcp-git")

@mcp.tool()
def healtz():
    "''Health check tool for the MCP Git server'''"
    return "OK"

@mcp.tool()
def push():
    '''use this tool to push the current state of the graph to a remote repository'''
    return "Pushed to remote repository"

@mcp.tool()
def pull():
    '''use this tool to pull the current state of the graph from a remote repository'''
    return "Pulled from remote repository"



if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )