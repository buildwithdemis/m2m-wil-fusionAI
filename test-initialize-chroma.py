import chromadb
import os
from dotenv import load_dotenv
from chromadb.config import Settings

load_dotenv()

# Create a Chroma client with the service URL and API token
client = chromadb.HttpClient(host=os.getenv("CHROMADB_HOST"), port=443, ssl=True,
                             settings=Settings(chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                                               chroma_client_auth_credentials=os.getenv("CHROMADB_API_TOKEN"),
                                               anonymized_telemetry=False))


collection = client.get_or_create_collection("knowledge_base")
collection.add(
    documents=[
        "FAQ: What is the price? The price is $100.",
        "Product: Widget X - $100, high-quality gadget.",
        "User Profile: John Doe, customer since 2023, prefers email support."
    ],
    ids=["faq1", "product1", "profile1"],
    metadatas=[{"type": "faq"}, {"type": "product"}, {"type": "profile"}]
)