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

def generate_topic():
    logger.info("Generating blog topic")

    fallback = """
        You are the content strategist for a technical blog called BitCodeMatrix.

        Generate ONE unique, SEO-friendly blog title that has high Google search potential.

        Primary categories (highest priority):
        - DevOps
        - Cloud Native
        - Kubernetes
        - Docker
        - Linux Commands
        - Networking
        - Distributed Systems
        - Python for DevOps
        - Data Engineering
        - Big Data

        Secondary categories:
        - Snowflake
        - Redshift
        - PySpark
        - Data Warehousing
        - Data Pipelines
        - Istio
        - Algorithms
        - Data Structures
        - Linux Administration

        Rules:
        - Choose ONE topic only.
        - Prefer practical, production-oriented tutorials.
        - Avoid generic beginner titles.
        - Use long-tail keywords that people actually search.
        - Make the title click-worthy without sounding like clickbait.
        - Do not use quotation marks.
        - Return ONLY the title.

        Examples of good titles:
        - Kubernetes Rolling Updates Explained with Real Production Examples
        - 25 Linux Commands Every DevOps Engineer Uses Daily
        - Docker Multi-Stage Builds: Reduce Image Size by 80%
        - Istio Traffic Routing Explained with Hands-On Examples
        - How Network Namespaces Work Inside Docker
        - Python Automation Scripts Every DevOps Engineer Should Know
        """
    prompt = pull_prompt(LANGSMITH_TOPIC_PROMPT, fallback)
    return ask_gemini(prompt)

def generate_blog(title):
    logger.info("Generating blog content")

    fallback = f"""
        You are a Senior DevOps Engineer and Technical Writer writing for BitCodeMatrix.

        Write a comprehensive, original, SEO-optimized technical blog.

        TITLE:
        {title}

        Audience:
        - DevOps Engineers
        - Platform Engineers
        - Cloud Engineers
        - SREs
        - Backend Engineers
        - Engineering students preparing for interviews

        Word Count:
        1500–2500 words

        Writing Style:
        - Conversational but technical
        - Production-focused
        - Explain WHY, not just HOW
        - Include practical examples
        - Avoid unnecessary marketing language

        Structure:

        1. SEO Meta Description (150–160 characters)

        2. Introduction
        - Explain the real-world problem.
        - Why engineers should care.

        3. Table of Contents

        4. Main Sections using H2 and H3 headings.

        5. Practical Examples
        - Linux commands
        - Docker commands
        - Kubernetes YAML
        - Python snippets
        - Bash scripts
        - Networking diagrams (ASCII if needed)

        6. Common Mistakes

        7. Production Best Practices

        8. Interview Questions (5–10)

        9. FAQ (5–8 questions)

        10. Conclusion

        Content Rules:
        - Use Markdown.
        - Include code blocks with proper language tags.
        - Explain every command.
        - Include performance and security considerations.
        - Mention common troubleshooting steps.
        - Compare tools where relevant.
        - Never invent statistics unless clearly stated as an estimate.
        - Make the article feel like an experienced engineer wrote it.

        When appropriate include:
        - Docker Compose examples
        - Kubernetes manifests
        - Helm commands
        - kubectl examples
        - Linux CLI examples
        - Networking commands (ping, traceroute, netstat, ss, tcpdump)
        - Python automation scripts
        - CI/CD examples (GitHub Actions or Jenkins)

        SEO Requirements:
        - Naturally repeat the primary keyword.
        - Include related keywords.
        - Use descriptive headings.
        - Write for Google's Helpful Content guidelines.

        Return the complete article in Markdown only.
        """
    prompt = pull_prompt(LANGSMITH_BLOG_PROMPT, fallback, title=title)
    md = ask_gemini(prompt)

    html = markdown.markdown(
        md,
        extensions=["tables", "fenced_code"]
    )
    logger.info("Converted generated blog content to HTML")
    return html