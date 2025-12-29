# VECTOR STORE AND EMBEDDINGS
from langchain_ollama import ChatOllama, OllamaEmbeddings
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

# PROMPTING
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import asyncio
from websockets.server import serve
import os
import json

import signal


# Load local LLM model from Ollama server
# LLM Model: deepseek-r1:8b
#model = ChatOllama(model="deepseek-r1:8b", base_url="http://localhost:11434")
model = ChatOllama(model="deepseek-r1:8b", base_url="http://localhost:11434")

# Initialize Ollama Embedding model
embeddings = OllamaEmbeddings(model='nomic-embed-text:v1.5', base_url="http://localhost:11434")

# Load vector database
#BASE_DIR = "/home/rochefym/projects/11172025_ver2_websockets"
BASE_DIR = "/home/k503/下載/20251124_Recommender_System-main/"
db_path = os.path.join(BASE_DIR, "dietary_reference_intakes")
new_vector_store = FAISS.load_local(db_path, embeddings=embeddings, allow_dangerous_deserialization=True)

# Prompt Template
prompt = ChatPromptTemplate.from_template("""
You are a professional clinical nutritionist specializing in elderly care in Taiwan.

Use the retrieved context below to support your reasoning.
- If context provides relevant data, use it directly.
- If it lacks exact values, give only safe, general suggestions.
- Do NOT make up numbers or conversions.
- Be concise, clear, and compassionate.
- Give the response in English.

Question:
{question}

Context:
{context}

Based on this meal intake and his calculated daily DRIs, please provide:
1. **Analysis** — summarize the nutritional content and adequacy.
2. **Suggestions** — what can be improved or balanced .
3. **Recommendations** — practical next steps for elderly dietary care.
""")

# Create a vector store Retriever
retriever = new_vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 10,          # fewer but higher-quality chunks
        "fetch_k": 50,   # how many to initially fetch before filtering
        "lambda_mult": 1  # balance between diversity and relevance
    }
)

# Function to format Retrieved documents from the vector store
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Define RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

async def echo(websocket):
    async for message in websocket:        
        results = rag_chain.invoke(message)
        await websocket.send(results)

async def main():
    # Allow overriding host/port via environment variables
    ws_address = os.environ.get("WS_HOST", "0.0.0.0")
    ws_port = int(os.environ.get("WS_PORT", "25002"))
    async with serve(echo, ws_address, ws_port):
        print("[INFO] please connect to the WebSocket service:", f"ws://{ws_address}:{ws_port}")
    
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())