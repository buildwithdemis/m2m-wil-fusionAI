from chromadb import HttpClient
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
import uuid

# Initialize ChromaDB HTTP client for Cloud Run
'''
client = HttpClient(
    Settings(chroma_api_impl="rest", chroma_server_host=os.getenv("CHROMADB_HOST", "localhost"), chroma_server_http_port=8000)
)
'''
client = HttpClient(
    host=os.getenv("CHROMADB_HOST"),
    port=int(os.getenv("CHROMADB_PORT")),
    ssl=True if os.getenv("CHROMADB_PORT") == "443" else False
)
embeddings = OpenAIEmbeddings()

async def get_context(query: str) -> str:
    vector_store = Chroma(client=client, collection_name="knowledge_base", embedding_function=embeddings)
    docs = vector_store.similarity_search(query, k=1)
    return docs[0].page_content if docs else ""

async def store_conversation(transcription: str, intent: str):
    call_id = str(uuid.uuid4())
    collection = client.get_collection("knowledge_base")
    collection.add(
        documents=[transcription],
        ids=[call_id],
        metadatas=[{"type": "conversation", "intent": intent, "call_id": call_id}]
    )