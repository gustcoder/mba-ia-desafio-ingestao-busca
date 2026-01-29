import chunk
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from rich import print
import os
from dotenv import load_dotenv

load_dotenv()

for key in ("OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if not os.getenv(key):
        raise RuntimeError(f"Please set the environment key: {key}.")

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    print(f"[bold blue]Iniciando ingestão de dados...[/bold blue]")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
    )
    if not splitter:
        raise SystemExit(0)

    chunks = splitter.split_documents(docs)
    print("Chunks: ", len(chunks))

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in chunks
    ]

    indexes = [f"doc-{i}" for i in range(len(enriched))]
    
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=indexes)
    print(f"[bold green]Ingestão concluída com sucesso![/bold green]\n")


if __name__ == "__main__":
    ingest_pdf()