import os
from litellm import embedding
from dotenv import load_dotenv

load_dotenv()

model = "text-embedding-ada-002"
api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(query: str) -> list[float]:
    resp = embedding(
        model=model,
        input=query,
        api_key=api_key,
    )
    return resp["data"][0]["embedding"]
