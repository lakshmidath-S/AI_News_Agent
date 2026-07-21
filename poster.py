import os
import tweepy

# All 4 credentials must be set as environment variables before running:
#   X_API_KEY
#   X_API_KEY_SECRET
#   X_ACCESS_TOKEN
#   X_ACCESS_TOKEN_SECRET


def get_client():
    return tweepy.Client(
        consumer_key=os.environ.get("X_API_KEY"),
        consumer_secret=os.environ.get("X_API_KEY_SECRET"),
        access_token=os.environ.get("X_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET"),
    )


def post_to_x(text):
    """Publish a post to X. Returns the response object."""
    client = get_client()
    response = client.create_tweet(text=text)
    return response


if __name__ == "__main__":
    # manual test - only run this if you actually want to post something real
    test_text = "Testing my AI news bot pipeline. This is a manual test post."
    result = post_to_x(test_text)
    print("Posted successfully:", result)