"""
Professional Tavily Live Search MCP Server Tool using FastMCP SDK
Provides real-time web search capabilities through Tavily API.
"""

from mcp.server.fastmcp import FastMCP
import requests
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import aiohttp

# Initialize FastMCP server
mcp = FastMCP("Tavily Search Server")

class TavilySearchError(Exception):
    """Custom exception for Tavily search errors"""
    pass

class TavilySearch:
    """Professional Tavily search client with comprehensive search capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Tavily search client
        
        Args:
            api_key: Tavily API key (if not provided, will look for TAVILY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        if not self.api_key:
            raise TavilySearchError("Tavily API key not provided. Set TAVILY_API_KEY environment variable.")
        
        self.base_url = "https://api.tavily.com"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def search(
        self,
        query: str,
        search_depth: str = "basic",
        topic: str = "general",
        days: Optional[int] = None,
        max_results: int = 5,
        include_images: bool = False,
        include_answer: bool = True,
        include_raw_content: bool = False,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Perform a search using Tavily API
        
        Args:
            query: Search query
            search_depth: "basic" or "advanced"
            topic: "general" or "news"
            days: Number of days to limit search (for news)
            max_results: Maximum number of results to return
            include_images: Whether to include images in results
            include_answer: Whether to include AI-generated answer
            include_raw_content: Whether to include raw content
            include_domains: List of domains to include
            exclude_domains: List of domains to exclude
        
        Returns:
            Dictionary containing search results
        """
        endpoint = f"{self.base_url}/search"
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results,
            "include_images": include_images,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content
        }
        
        # Add optional parameters
        if days is not None:
            payload["days"] = days
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise TavilySearchError(f"Search request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise TavilySearchError(f"Invalid JSON response: {str(e)}")
    
    async def async_search(
        self,
        query: str,
        search_depth: str = "basic",
        topic: str = "general",
        days: Optional[int] = None,
        max_results: int = 5,
        include_images: bool = False,
        include_answer: bool = True,
        include_raw_content: bool = False,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Asynchronous version of search method
        """
        endpoint = f"{self.base_url}/search"
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results,
            "include_images": include_images,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content
        }
        
        # Add optional parameters
        if days is not None:
            payload["days"] = days
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    json=payload,
                    headers=self.headers,
                    timeout=30
                ) as response:
                    response.raise_for_status()
                    return await response.json()
                    
        except aiohttp.ClientError as e:
            raise TavilySearchError(f"Async search request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise TavilySearchError(f"Invalid JSON response: {str(e)}")

# Initialize Tavily client
try:
    tavily_client = TavilySearch()
except TavilySearchError as e:
    print(f"Warning: Tavily client initialization failed: {e}")
    tavily_client = None

# MCP Tool: Basic Web Search
@mcp.tool()
def web_search(
    query: str,
    api_key: Optional[str] = None,
    max_results: int = 5,
    search_depth: str = "basic",
    include_answer: bool = True
) -> Dict[str, Any]:
    """
    Search the web for information using Tavily API.
    
    Args:
        query: Search query string
        api_key: User's Tavily API key (optional, uses server default if not provided)
        max_results: Maximum number of results to return (1-20)
        search_depth: "basic" for faster results, "advanced" for more comprehensive
        include_answer: Whether to include AI-generated answer summary
    
    Returns:
        Dictionary containing search results with URLs, titles, content, and optional answer
    """
    try:
        # Use user's API key or fallback to server default
        if api_key:
            # Create temporary client with user's API key
            user_client = TavilySearch(api_key=api_key)
        elif tavily_client:
            # Use server's default client
            user_client = tavily_client
        else:
            return {
                "query": query,
                "error": "No API key provided. Please provide your Tavily API key or configure server default.",
                "success": False
            }
        
        # Validate parameters
        if max_results < 1 or max_results > 20:
            raise TavilySearchError("max_results must be between 1 and 20")
        
        if search_depth not in ["basic", "advanced"]:
            raise TavilySearchError("search_depth must be 'basic' or 'advanced'")
        
        results = user_client.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            include_answer=include_answer,
            topic="general"
        )
        
        return {
            "query": query,
            "results": results.get("results", []),
            "answer": results.get("answer", "") if include_answer else None,
            "search_depth": search_depth,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except TavilySearchError as e:
        return {
            "query": query,
            "error": str(e),
            "success": False
        }
    except Exception as e:
        return {
            "query": query,
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }

# MCP Tool: News Search
@mcp.tool()
def news_search(
    query: str,
    api_key: Optional[str] = None,
    days: int = 7,
    max_results: int = 5,
    include_answer: bool = True
) -> Dict[str, Any]:
    """
    Search for recent news articles using Tavily API.
    
    Args:
        query: News search query
        api_key: User's Tavily API key (optional, uses server default if not provided)
        days: Number of days to look back for news (1-30)
        max_results: Maximum number of results to return (1-20)
        include_answer: Whether to include AI-generated news summary
    
    Returns:
        Dictionary containing news search results
    """
    try:
        # Use user's API key or fallback to server default
        if api_key:
            user_client = TavilySearch(api_key=api_key)
        elif tavily_client:
            user_client = tavily_client
        else:
            return {
                "query": query,
                "error": "No API key provided. Please provide your Tavily API key or configure server default.",
                "success": False
            }
        
        # Validate parameters
        if days < 1 or days > 30:
            raise TavilySearchError("days must be between 1 and 30")
        
        if max_results < 1 or max_results > 20:
            raise TavilySearchError("max_results must be between 1 and 20")
        
        results = user_client.search(
            query=query,
            max_results=max_results,
            search_depth="basic",
            topic="news",
            days=days,
            include_answer=include_answer
        )
        
        return {
            "query": query,
            "days": days,
            "results": results.get("results", []),
            "answer": results.get("answer", "") if include_answer else None,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except TavilySearchError as e:
        return {
            "query": query,
            "error": str(e),
            "success": False
        }
    except Exception as e:
        return {
            "query": query,
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }

# MCP Tool: Advanced Search with Domain Filtering
@mcp.tool()
def advanced_search(
    query: str,
    max_results: int = 10,
    search_depth: str = "advanced",
    include_images: bool = False,
    include_raw_content: bool = False,
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Perform advanced web search with domain filtering and additional options.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (1-20)
        search_depth: "basic" or "advanced"
        include_images: Whether to include image results
        include_raw_content: Whether to include raw HTML content
        include_domains: List of domains to include in search
        exclude_domains: List of domains to exclude from search
    
    Returns:
        Dictionary containing comprehensive search results
    """
    if not tavily_client:
        return {
            "query": query,
            "error": "Tavily client not initialized. Please check API key configuration.",
            "success": False
        }
    
    try:
        # Validate parameters
        if max_results < 1 or max_results > 20:
            raise TavilySearchError("max_results must be between 1 and 20")
        
        if search_depth not in ["basic", "advanced"]:
            raise TavilySearchError("search_depth must be 'basic' or 'advanced'")
        
        results = tavily_client.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            include_images=include_images,
            include_raw_content=include_raw_content,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            include_answer=True
        )
        
        return {
            "query": query,
            "search_depth": search_depth,
            "include_images": include_images,
            "include_raw_content": include_raw_content,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "results": results.get("results", []),
            "answer": results.get("answer", ""),
            "images": results.get("images", []) if include_images else None,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except TavilySearchError as e:
        return {
            "query": query,
            "error": str(e),
            "success": False
        }
    except Exception as e:
        return {
            "query": query,
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }

# MCP Tool: Multi-query Search
@mcp.tool()
def multi_search(queries: List[str], max_results_per_query: int = 3) -> Dict[str, Any]:
    """
    Perform multiple searches simultaneously.
    
    Args:
        queries: List of search queries
        max_results_per_query: Maximum results per individual query
    
    Returns:
        Dictionary containing results for all queries
    """
    if not tavily_client:
        return {
            "queries": queries,
            "error": "Tavily client not initialized. Please check API key configuration.",
            "success": False
        }
    
    try:
        if len(queries) > 10:
            raise TavilySearchError("Maximum 10 queries allowed per multi-search")
        
        all_results = {}
        
        for i, query in enumerate(queries):
            try:
                results = tavily_client.search(
                    query=query,
                    max_results=max_results_per_query,
                    search_depth="basic",
                    include_answer=True
                )
                
                all_results[f"query_{i+1}"] = {
                    "query": query,
                    "results": results.get("results", []),
                    "answer": results.get("answer", ""),
                    "success": True
                }
                
            except Exception as e:
                all_results[f"query_{i+1}"] = {
                    "query": query,
                    "error": str(e),
                    "success": False
                }
        
        return {
            "queries": queries,
            "results": all_results,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except TavilySearchError as e:
        return {
            "queries": queries,
            "error": str(e),
            "success": False
        }
    except Exception as e:
        return {
            "queries": queries,
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }
