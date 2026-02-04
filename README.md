# 🚀 Desafio MBA Engenharia de Software com IA - Full Cycle

![Status](https://img.shields.io/badge/Status-Em%20Progresso-green?style=for-the-badge&logo=github)
![IA](https://img.shields.io/badge/Focus-AI%20Engineering-blueviolet?style=for-the-badge&logo=openai)
![FullCycle](https://img.shields.io/badge/School-FullCycle-yellow?style=for-the-badge)

**Objetivos:**
* **Ingestão:** Ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector.
* **Busca:** Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF.

---

## 🛠️ Tecnologias e Requisitos

* Linguagem: Python
* Framework: LangChain
* Banco de dados: PostgreSQL + pgVector
* Execução do banco de dados: Docker & Docker Compose (docker-compose fornecido no repositório de exemplo)

---

## 💻 Como Executar o Desafio

```bash
# Navegue até a raiz da pasta do desafio
cd mba-ia-desafio-ingestao-busca

# Suba o ambiente
docker compose up -d

# OPEN AI KEY
Preencha a variável "OPENAI_API_KEY" no .env com sua chave

# Realizar Ingestão
docker exec -it python_app python src/ingest.py

# Executar o CLI
docker exec -it python_app python src/chat.py
