import chunk
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from rich import print
import os
from dotenv import load_dotenv
from helpers import check_env_keys, get_embeddings, get_pg_vector_store

load_dotenv()

def ingest_pdf():
    check_env_keys()
    pdf_path = os.getenv("PDF_PATH")

    print(f"[bold blue]Iniciando ingestão de dados...[/bold blue]")
    loader = PyPDFLoader(pdf_path)
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
    
    embeddings = get_embeddings()
    store = get_pg_vector_store(embeddings)

    store.add_documents(documents=enriched, ids=indexes)
    print(f"[bold green]Ingestão concluída com sucesso![/bold green]\n")


if __name__ == "__main__":
    ingest_pdf()