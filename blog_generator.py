from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
import markdown
import logging

logger = logging.getLogger(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)

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

def generate_topic():
    logger.info("Generating blog topic")
    prompt = """
        Generate ONE unique SEO-friendly blog title.

        Randomly choose from:
        - AI
        - Python
        - Finance
        - Productivity
        - Fitness
        - Technology
        - Cybersecurity
        - Travel

        Return ONLY the title.
    """
    title = ask_gemini(prompt)
    logger.info("Generated blog topic")
    return title

def generate_blog(title):
    logger.info("Generating blog content")
    prompt = f"""
        Write a high-quality SEO blog.

        Title: {title}

        Requirements:
        - 1200–1800 words
        - Human-sounding
        - H1, H2, H3 headings
        - Meta description
        - Bullet lists
        - FAQ section
        - Conclusion

        Return the response in Markdown.
    """

    md = ask_gemini(prompt)

    html = markdown.markdown(
        md,
        extensions=["tables", "fenced_code"]
    )

    logger.info("Converted generated blog content to HTML")
    return html