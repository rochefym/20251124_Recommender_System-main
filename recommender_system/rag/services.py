# VECTOR STORE AND EMBEDDINGS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# PROMPTING
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import os
from ollama_llm.services import get_ollama_llm_response

# Load local LLM model from Ollama server
# LLM Model: deepseek-r1:8b
model = ChatOllama(model="deepseek-r1:8b", base_url="http://localhost:11434")

# Initialize Ollama Embedding model
embeddings = OllamaEmbeddings(model='nomic-embed-text:v1.5', base_url="http://localhost:11434")

# Load vector database
#BASE_DIR = "/home/rochefym/projects/11172025_ver2_websockets"
BASE_DIR = "/home/k503/下載/20251124_Recommender_System-main/"
db_path = os.path.join(BASE_DIR, "dietary_reference_intakes")
new_vector_store = FAISS.load_local(db_path, embeddings=embeddings, allow_dangerous_deserialization=True)

# Create a vector store Retriever
retriever = new_vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 10,          # fewer but higher-quality chunks
        "fetch_k": 50,   # how many to initially fetch before filtering
        "lambda_mult": 1  # balance between diversity and relevance
    }
)

# Prompt Template
# Create detailed prompt for recommendation
prompt = ChatPromptTemplate.from_template("""
You are a clinical nutrition assistant writing guidance for non-medical caregivers.

TASK:
Review the patient information, recommended daily intake, and meals, then provide clear dietary guidance that compares actual intake patterns against recommended needs. Use the retrieved context below to support your reasoning.

CRITICAL OUTPUT RULES:
- Output PLAIN TEXT only
- Do NOT use JSON
- Do NOT use markdown
- Do NOT use bullet symbols other than the ones shown below
- Do NOT use code blocks or backticks
- Do NOT include medical disclaimers
- Do NOT include any introductory or closing remarks
- If it lacks exact values, give only safe, general suggestions.
- Do NOT make up numbers or conversions.

FORMAT RULES (MUST FOLLOW EXACTLY):

Summary:
(2 short sentences describing overall diet vs recommended intake)

Key Health Concerns:
- Line 1
- Line 2

Dietary Issues Observed:
- Line 1
- Line 2

Caregiver Action Steps:
1. Step one
2. Step two
3. Step three

CONTENT LIMITS:
- Keep total length under 140 words
- Use simple, supportive language                                  
- Focus on food choices, portion size, and balance
- Reference recommended intake only when helpful for guidance

Query:
{question}

Context:
{context}
                                          
FINAL CHECK:
Return ONLY the formatted text exactly as specified above. No extra text.
""")


# Function to format Retrieved documents from the vector store
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


# Define RAG chain
rag_chain = (
    {"context": retriever | format_docs, 
     "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


def generate_recommendation(question):
    try:
        results = rag_chain.invoke(question)
        results = summarize_text_with_ollama(results)

        return results
    except Exception as e:
        print(f"Error: {e}")
        return Exception
    
    
def generate_translated_recommendation(question):
    try:
        results = rag_chain.invoke(question)
        results = translate_text_with_ollama(results)

        return results
    except Exception as e:
        print(f"Error: {e}")
        return Exception
    

def summarize_text_with_ollama(text: str) -> str:
    prompt = f"""Please provide a comprehensive summary with 150 or less words: 
{text}

But keep the same format rules below
FORMAT RULES (MUST FOLLOW EXACTLY)

Summary:
(2 short sentences describing overall diet vs recommended intake)

Key Health Concerns:
- Line 1
- Line 2

Dietary Issues Observed:
- Line 1
- Line 2

Caregiver Action Steps:
1. Step one
2. Step two
3. Step three
"""

    try:
        response = get_ollama_llm_response(prompt)
        return response

    except Exception as e:
        raise RuntimeError(f"Ollama summarization failed: {e}")
    

def translate_text_with_ollama(text: str) -> str:
    prompt = f"Please translate the following text into Traditional Chinese: \n\n{text}"

    try:
        response = get_ollama_llm_response(prompt)
        return response

    except Exception as e:
        raise RuntimeError(f"Ollama translation failed: {e}")


def summarize_and_translate_text_with_ollama(text: str) -> str:
    prompt = f"""Please provide a comprehensive summary with 150 or less words:
{text}

But keep the same format rules below
FORMAT RULES (MUST FOLLOW EXACTLY)

Summary:
(2 short sentences describing overall diet vs recommended intake)

Key Health Concerns:
- Line 1
- Line 2

Dietary Issues Observed:
- Line 1
- Line 2

Caregiver Action Steps:
1. Step one
2. Step two
3. Step three

Then translate the text into Traditional Chinese and only reply with the translated text.
"""

    try:
        response = get_ollama_llm_response(prompt)
        return response

    except Exception as e:
        raise RuntimeError(f"Ollama summarization failed: {e}")