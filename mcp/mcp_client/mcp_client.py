# 1. MCP Client & Tool Adapter
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

class mcp_client:
    """
    Connects to a specific server, initializes the session, 
    and extracts the tools into a LangChain-compatible format.
    """

    def __init__(self, config):
        self.client = MultiServerMCPClient(config)
        self.tools = []
        self.session = {}

    async def get_tools_from_server(self,server_name:str):
        
        #creating session
        session=await self.client.session(server_name).__aenter__()
        self.session[server_name]=session

        #loading the mcp tools as langchain tools 
        server_tools=await load_mcp_tools(session=session)
        self.tools.extend(server_tools)

        return server_tools
    
    async def close_connections(self):
        for session in self.session.values():
            await session.__aexit__(None, None, None)


