from google import genai
import markdown
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError
from google.genai.errors import APIError

from config import GEMINI_API_KEY
    
client = genai.Client(api_key=GEMINI_API_KEY)
MODELS = [
    "gemini-3.6-flash",
    "gemini-3.6-pro"
]


@retry(
    retry=retry_if_exception_type(ServerError),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    stop=stop_after_attempt(5),
    reraise=True,
)
def ask_gemini(prompt: str) -> str:
    last_error = None

    for model in MODELS:
        try:
            chat = client.chats.create(model=model)
            return chat.send_message(prompt).text.strip()
        except APIError as e:
            last_error = e
            continue

    raise last_error

def generate_topic():
    prompt = """
        Generate ONE unique SEO-friendly blog title.

        Pick a random category from:
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
        - Human sounding
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