import os
from dotenv import load_dotenv
from helpers import check_env_keys, get_embeddings, get_pg_vector_store

from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(user_question: str = None):
  check_env_keys()
  open_ai_key = os.getenv("OPENAI_API_KEY")

  embeddings = get_embeddings()
  store = get_pg_vector_store(embeddings)
  context = store.similarity_search_with_score(user_question, k=10)

  prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
  model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=open_ai_key
  )

  chain = prompt | model

  result = chain.invoke(
    {
      "context": context,
      "question": user_question
    }
  )

  return result.content
