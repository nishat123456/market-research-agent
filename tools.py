"""
Tools for the market research agent.
Uses DuckDuckGo for free web search (no API key required).
"""

import time
from ddgs import DDGS
from ddgs.exceptions import RatelimitException


def search_web(query: str, max_results: int = 5, retries: int = 3) -> list[dict]:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        retries: Number of retry attempts on rate limit
        
    Returns:
        List of search results with title, url, and body
    """
    for attempt in range(retries):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            return results
        except RatelimitException:
            if attempt < retries - 1:
                wait_time = (attempt + 1) * 5  # 5s, 10s, 15s
                print(f"   ⏳ Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"   ⚠️  Search rate limited, skipping web results")
                return []
    return []


def search_news(query: str, max_results: int = 3, retries: int = 3) -> list[dict]:
    """
    Search recent news using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        retries: Number of retry attempts on rate limit
        
    Returns:
        List of news results
    """
    for attempt in range(retries):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.news(query, max_results=max_results))
            return results
        except RatelimitException:
            if attempt < retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"   ⏳ Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"   ⚠️  News search rate limited, skipping")
                return []
    return []
