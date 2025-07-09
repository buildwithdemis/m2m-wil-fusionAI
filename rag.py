import chromadb
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
import uuid
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

# Initialize ChromaDB HTTP client for Cloud Run
# Create a Chroma client with the service URL and API token
client = chromadb.HttpClient(host=os.getenv("CHROMADB_HOST"), port=443, ssl=True,
                             settings=Settings(chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                                               chroma_client_auth_credentials=os.getenv("CHROMADB_API_TOKEN"),
                                               anonymized_telemetry=False))

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