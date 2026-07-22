import os
import time
from google import genai
from google.genai import errors

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """You are writing a short social media post (like a tweet) about the AI news article below.

Rules:
- Aim for 300-350 characters (use the space available, don't be overly brief)
- Include enough context that someone unfamiliar with the story understands why it matters
- No hashtags, no emojis
- Sound human and informative, not robotic or hype-y
- Do not use quotation marks around the whole post

Title: {title}
Summary: {summary}

Write only the post text, nothing else.
"""


def summarize_article(title, summary, max_retries=3, retry_delay=15):
    """Generate a short, post-ready summary of an article using Gemini.
    Retries automatically if Gemini's servers are temporarily overloaded (503)."""
    prompt = PROMPT_TEMPLATE.format(title=title, summary=summary)

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except errors.ServerError as e:
            print(f"Gemini server error (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                raise