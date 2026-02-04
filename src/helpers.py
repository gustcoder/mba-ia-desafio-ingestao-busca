import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

def check_env_keys():
    for key in ("OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
        if not os.getenv(key):
            raise RuntimeError(f"Please set the environment key: {key}.")

def get_embeddings():
    return OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

def get_pg_vector_store(embeddings):
    return PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
