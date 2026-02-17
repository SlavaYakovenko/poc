import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")

client = OpenAI(api_key=api_key)

def generate_post(agent_name, stance, feed):
    feed_text = "\n".join([f"{p['author']}: {p['content']}" for p in feed])
    system_prompt = f"""
    You are a social media user named {agent_name}.
    Your ideological stance is: {stance}.

    Here is the current feed:
    {feed_text}

    Write a short post (1-3 sentences) reacting to the feed.
    Stay consistent with your stance.
    Do not repeat posts verbatim.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()