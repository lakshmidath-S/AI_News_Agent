import os
from google import genai

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


def summarize_article(title, summary):
    """Generate a short, post-ready summary of an article using Gemini."""
    prompt = PROMPT_TEMPLATE.format(title=title, summary=summary)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text.strip()