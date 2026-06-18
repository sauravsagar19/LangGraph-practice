# We are defining the most used tools here
# Arxiv, wikipedia, duck duck go.

import arxiv
import wikipedia
from duckduckgo_search import DDGS
from langchain.tools import tool

@tool
def search_arxiv(query_string: str, max_results: int = 2) -> list[dict]:
    """
    Queries the official arXiv API for research papers.
    Returns a list of dictionaries with paper metadata.
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query_string,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        # Calling client.results() is the modern, stable 2.x+ pattern
        for result in client.results(search):
            papers.append({
                "title": result.title,
                "summary": result.summary,
                "url": result.entry_id,
                "published": result.published.strftime("%Y-%m-%d"),
                "authors": [author.name for author in result.authors]
            })
        return papers
    except Exception as e:
        return [{"error": f"arXiv search failed: {str(e)}"}]
@tool
def search_wikipedia(query_string: str, sentences: int = 3) -> str:
    """
    Queries Wikipedia for summary definitions.
    Handles disambiguation conflicts safely.
    """
    # Force Wikipedia to look up variations cleanly
    wikipedia.set_lang("en") 
    try:
        # Bypassing background parsing frameworks saves memory
        return wikipedia.summary(query_string, sentences=sentences, auto_suggest=False)
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

@tool
def human_approval():
    '''
    The tool should only be called if there is need for human intervention.
    '''
    pass


# if __name__ == "__main__":
#     print("--- Testing arXiv ---")
#     arxiv_res = search_arxiv("1706.03762", 1)
#     print(f"Title: {arxiv_res[0].get('title')}\n")

#     print("--- Testing Wikipedia ---")
#     wiki_res = search_wikipedia("Transformer (deep learning architecture)")
#     print(f"Summary: {wiki_res}\n")

