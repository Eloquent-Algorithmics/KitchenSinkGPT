
# !/usr/bin/env python
# coding: utf-8
# Filename: nytimes_tools.py
# Path: plugins\_news_expert\nytimes_tools.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17

"""
This module contains functions to fetch news from New York Times.
"""

from typing import List
import aiohttp
from rich.console import Console

# Initialize the rich console
console = Console()


# Define the function to fetch news from New York Times
async def get_news_from_nytimes(query: str, api_key: str, url: str) -> List:

    """
    This function fetches news from New York Times based on a query.
    :param query: The search query for the New York Times API
    :param api_key: The API key for the New York Times API
    :param url: The URL for the New York Times API
    :return: A list of news articles
    """

    # Define the parameters for the request
    params = {
        "q": query,
        "api-key": api_key,
    }

    # Make the request to the New York Times API
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as res:  # Use the 'url' parameter here
                res.raise_for_status()
                data = await res.json()
                nyt_news = []
                for doc in data["response"]["docs"]:
                    nyt_news.append(
                        {
                            "title": doc["headline"]["main"],
                            "description": doc["abstract"],
                            "snippet": doc["lead_paragraph"],
                            "link": doc["web_url"],
                        }
                    )
                return nyt_news
        except ValueError as error:
            console.print(f"Failed to fetch news from NYT: {error}")
            return []


nytimes_news_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_news_from_nyt",
            "description": "Fetch news from New York Times based on a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for the New York Times API",
                    },
                },
                "required": ["query"],
            },
        },
    },
]
