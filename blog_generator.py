from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
import markdown

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    chat = client.chats.create(model=GEMINI_MODEL)
    response = chat.send_message(prompt)
    return response.text.strip()

def generate_topic():
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
    return ask_gemini(prompt)

def generate_blog(title):
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

    return html