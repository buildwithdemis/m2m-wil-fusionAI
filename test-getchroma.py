import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os
load_dotenv()

# Create a Chroma client with the service URL and API token
client = chromadb.HttpClient(host=os.getenv("CHROMADB_HOST"), port=443, ssl=True,
                             settings=Settings(chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                                               chroma_client_auth_credentials=os.getenv("CHROMADB_API_TOKEN"),
                                               anonymized_telemetry=False))


collection = client.get_collection("knowledge_base")
results = collection.get(where={"type": "conversation"})
print(results)