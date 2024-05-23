from llama_index.llms.groq import Groq
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def get_llm():
    llm = Groq(model="llama3-8b-8192", api_key=GROQ_API_KEY)
    return llm

def get_embeddings():
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return embed_model