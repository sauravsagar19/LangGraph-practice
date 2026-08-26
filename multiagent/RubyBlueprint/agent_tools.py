from langchain_core.tools import tool

@tool
def arxiv():
    "It will be called when the query is related to any research paper"
    return "Arxiv tool called"
@tool
def wikipedia():
    "It will be called for basic general knowledge question"
    return "Wikipedia tool called"
@tool
def weather():
    "tools for weathers"
    return "weather tool called"

@tool
def delete_file():
    "It will be called when the user wants to delete a file"
    return "Delete file tool called"

@tool
def clear_cache():
    "It will be called when the user wants to clear the cache"
    return "Clear cache tool called"

@tool
def open_yt():
    "It will be called when the user wants to open youtube"
    return "Open youtube tool called"

Destructive_tools=['delete_file','clear_cache']
