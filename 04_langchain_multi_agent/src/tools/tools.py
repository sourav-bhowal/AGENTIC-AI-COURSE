from langchain.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re
import requests
import os

# Load environment variables
load_dotenv()

# Get the API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize the Tavily Client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def web_search(query: str) -> str:
    """Search the web for information using the Tavily API. Returns the title, URL, and content of the results."""

    # Search the web for information using the Tavily API
    responses = tavily_client.search(query, max_results=5)

    # Initialize the output list
    output = []

    # Loop through the responses and add the title, URL, and content to the output
    for res in responses["results"]:
        output.append(f"Title: {res['title']}\nURL: {res['url']}\nContent: {res['content'][:300]}\n")

    # Join the output with newlines
    return "\n-----\n".join(output)

@tool
def web_scrape(url: str) -> str:
    """Scrape and extract clean readable content from a URL. Uses multiple extraction strategies for better reliability."""

    # Set headers to mimic a real browser request
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # ── Fetch page ─────────────────────────────────────
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        # Check if the request was successful
        response.raise_for_status()

        # Get the HTML content of the page
        html = response.text

        # ──────────────────────────────────────────────────
        # Strategy 1 → trafilatura (BEST for articles/blogs)
        # ──────────────────────────────────────────────────
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        # If trafilatura successfully extracted content and it's sufficiently long, return it
        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', extracted)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 2 → readability
        # ──────────────────────────────────────────────────

        # Use readability to extract the main content of the page
        doc = Document(html)

        # Get the summary of the document, which is the main content
        clean_html = doc.summary()

        # Remove unwanted tags like scripts, styles, and navigation elements
        soup = BeautifulSoup(clean_html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Get the text content from the cleaned HTML
        text = soup.get_text(separator=" ", strip=True)

        # If readability successfully extracted content and it's sufficiently long, return it
        if text and len(text.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', text)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 3 → fallback full page extraction
        # ──────────────────────────────────────────────────
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted tags like scripts, styles, and navigation elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Get the text content from the cleaned HTML
        text = soup.get_text(separator=" ", strip=True)

        # If the fallback extraction successfully extracted content and it's sufficiently long, return it
        cleaned = re.sub(r'\s+', ' ', text)

        # If any of the extraction strategies returned meaningful content, return it (limited to 5000 characters)
        if cleaned:
            return cleaned[:5000]

        return "Could not extract meaningful content from the page."

    # Handle exceptions and return appropriate error messages
    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
