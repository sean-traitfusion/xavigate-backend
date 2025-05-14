import os
import openai
# Load environment variables from root and service .env for unified configuration
from dotenv import load_dotenv
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)
service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Model for embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def get_embedding(text: str) -> list[float]:
    """
    Call OpenAI to get an embedding for the given text.
    """
    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding