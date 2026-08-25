from google import genai
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LANGSMITH_API_KEY,
    LANGSMITH_BLOG_PROMPT,
    LANGSMITH_TOPIC_PROMPT,
)
from langsmith import Client, traceable
import markdown
import logging
import random
import re

logger = logging.getLogger(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)
langsmith_client = Client(api_key=LANGSMITH_API_KEY)

@traceable(name="gemini.generate", run_type="llm")
def ask_gemini(prompt: str) -> str:
    logger.debug("Sending prompt to Gemini model=%s", GEMINI_MODEL)
    try:
        chat = client.chats.create(model=GEMINI_MODEL)
        response = chat.send_message(prompt)
        logger.debug("Received Gemini response")
        return response.text.strip()
    except Exception as exc:
        logger.error("Gemini request failed: %s", exc)
        raise

def pull_prompt(prompt_name: str | None, fallback: str, **variables: str) -> str:
    if not prompt_name:
        logger.warning("LangSmith prompt name is not configured; using local fallback")
        return fallback

    logger.info("Pulling prompt from LangSmith name=%s", prompt_name)
    try:
        prompt = langsmith_client.pull_prompt(prompt_name)
        return prompt.invoke(variables).to_string()
    except Exception as exc:
        logger.error("LangSmith prompt pull failed for %s: %s", prompt_name, exc)
        raise

EDITORIAL_FORMATS = [
    "Breaking News Analysis",
    "Architecture Deep Dive",
    "Research Breakdown",
    "Tool Comparison",
    "Industry Trends",
    "Future Predictions",
    "Engineering Case Study",
]

BANNED_TITLE_PATTERNS = [
    r"\boom\b", r"\bexecutor\b", r"memory tuning", r"linux commands?",
    r"docker compose", r"\bkubectl\b", r"rolling update", r"troubleshooting",
    r"\berror\b", r"\bfix(?:ing)?\b", r"\bhow to\b", r"\bwhat is\b",
]

def choose_editorial_format() -> str:
    return random.choice(EDITORIAL_FORMATS)

def is_allowed_topic(title: str) -> bool:
    return not any(
        re.search(pattern, title, flags=re.IGNORECASE)
        for pattern in BANNED_TITLE_PATTERNS
    )

def generate_topic(previous_titles=None, headlines=None, editorial_format=None):
    logger.info("Generating editorial blog topic")
    previous_titles = previous_titles or []
    headlines = headlines or []
    editorial_format = editorial_format or choose_editorial_format()
    previous_title_text = "\n".join(f"- {title}" for title in previous_titles)
    headline_text = "\n".join(f"- {headline}" for headline in headlines)

    fallback = f"""
        You are the editor of the AI engineering publication BitCodeMatrix.

        Choose ONE fresh blog topic based on today's real headlines when available.
        This must feel like an AI newsletter analysis, not an evergreen troubleshooting guide.

        Today's headlines:
        {headline_text or "- No feed headlines are available; choose a recent AI development."}

        Already published titles:
        {previous_title_text or "- None recorded yet."}

        Content buckets: Breaking AI Releases (40%), AI Research (20%),
        AI Engineering (20%), Data Engineering Trends (10%), Industry Analysis (10%).

        Write the title as a {editorial_format}. Avoid anything semantically similar
        to the published titles. Never generate Docker, Linux command, Kubernetes
        troubleshooting, PySpark tuning, or OOM articles. Avoid tutorial framing,
        generic beginner content, "How to", and "What is". Return ONLY the title.
        """
    prompt = pull_prompt(
        LANGSMITH_TOPIC_PROMPT,
        fallback,
        question=fallback,
        previous_titles=previous_title_text,
        headlines=headline_text,
        editorial_format=editorial_format,
    )
    prompt = f"{prompt}\n\nMANDATORY EDITORIAL BRIEF:\n{fallback}"

    for attempt in range(3):
        title = ask_gemini(prompt).strip().strip('"')
        if is_allowed_topic(title):
            return title
        logger.warning("Rejected banned topic from Gemini (attempt %s/3)", attempt + 1)
        prompt += "\nThe previous title violated the banned-topic rules. Generate a different title."

    raise ValueError("Gemini did not produce an allowed editorial topic after 3 attempts")

def generate_blog(title, editorial_format="Technical Analysis"):
    logger.info("Generating blog content")

    fallback = f"""
        You are a senior AI engineer and technical writer for BitCodeMatrix, an AI
        engineering publication. Write an original article about the topic below.

        Editorial format: {editorial_format}

        TITLE:
        {title}

        Audience:
        - AI and ML engineers
        - Platform and data engineers building AI systems
        - Engineering leaders evaluating AI platforms

        Word Count:
        1200–2200 words

        Writing Style:
        - Analytical, precise, and production-aware
        - Explain what changed, why it matters, and what engineers should do next
        - Distinguish confirmed facts from informed analysis
        - Avoid unnecessary marketing language

        Structure:

        1. SEO Meta Description (150–160 characters)

        2. Introduction
        - Explain the real-world problem.
        - Why engineers should care.

        3. Table of Contents

        4. Main Sections using H2 and H3 headings.

        5. Technical implications and practical engineering considerations

        6. Limitations, open questions, and risks

        7. Recommendations for engineering teams

        8. Conclusion

        Content Rules:
        - Use Markdown.
        - Include code blocks with proper language tags.
        - Include code or configuration only when it clarifies the AI engineering topic.
        - Include performance, security, cost, and operational considerations where relevant.
        - Compare tools where relevant.
        - Never invent statistics unless clearly stated as an estimate.
        - Make the article feel like an experienced engineer wrote it.

        - Do not turn the article into a generic Docker, Linux, Kubernetes, or PySpark tutorial.

        SEO Requirements:
        - Naturally repeat the primary keyword.
        - Include related keywords.
        - Use descriptive headings.
        - Write for Google's Helpful Content guidelines.

        Return the complete article in Markdown only.
        """
    prompt = pull_prompt(
        LANGSMITH_BLOG_PROMPT,
        fallback,
        title=title,
        editorial_format=editorial_format,
    )
    prompt = f"{prompt}\n\nMANDATORY ARTICLE BRIEF:\n{fallback}"
    md = ask_gemini(prompt)

    html = markdown.markdown(
        md,
        extensions=["tables", "fenced_code"]
    )
    logger.info("Converted generated blog content to HTML")
    return html