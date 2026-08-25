from urllib.request import Request, urlopen
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)

RSS_FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "NVIDIA": "https://blogs.nvidia.com/feed/",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "arXiv AI": "https://export.arxiv.org/rss/cs.AI",
}

def _fetch_feed(source, url, limit_per_feed):
    try:
        request = Request(url, headers={"User-Agent": "BitCodeMatrix/1.0"})
        with urlopen(request, timeout=8) as response:
            root = ElementTree.fromstring(response.read())
        items = root.findall(".//item") or root.findall(".//{*}entry")
        return [
            f"{title.strip()} ({source})"
            for item in items[:limit_per_feed]
            for title in [item.findtext("title") or item.findtext("{*}title")]
            if title and title.strip()
        ]
    except Exception as exc:
        logger.warning("Could not fetch %s RSS feed: %s", source, exc)
        return []

def fetch_ai_headlines(limit_per_feed=5):
    with ThreadPoolExecutor(max_workers=len(RSS_FEEDS)) as executor:
        results = executor.map(
            lambda feed: _fetch_feed(feed[0], feed[1], limit_per_feed), RSS_FEEDS.items()
        )
        headlines = [headline for result in results for headline in result]
    logger.info("Collected %s AI news headlines", len(headlines))
    return headlines