from fastmcp import FastMCP
mcp=FastMCP("mcp-math")

@mcp.tool()
def healtz():
    "''Health check tool for the MCP Math server'''"
    return "OK"

@mcp.tool()
def add(a: float, b: float) -> float:
    '''Add two numbers together'''
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    '''Subtract the second number from the first'''
    return abs(a - b)

@mcp.tool()
def multiply(a: float, b: float) -> float:
    '''Multiply two numbers together'''
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    '''Divide the first number by the second'''
    if b == 0:
        return "Error: Division by zero is undefined."
    return a / b

if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )
