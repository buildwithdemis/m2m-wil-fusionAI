from chromadb import Client, HttpClient
import os

#client = Client()
#client = Client(host=os.getenv("CHROMADB_HOST", "localhost"), port=8000)

client = HttpClient(
    host=os.getenv("http://localhost"),
    port=8000,
    #port=int(os.getenv("CHROMADB_PORT", 443) if os.getenv("CHROMADB_PORT") else 8000),
)
collection = client.create_collection("knowledge_base")
collection.add(
    documents=[
        "FAQ: What is the price? The price is $100.",
        "Product: Widget X - $100, high-quality gadget.",
        "User Profile: John Doe, customer since 2023, prefers email support."
    ],
    ids=["faq1", "product1", "profile1"],
    metadatas=[{"type": "faq"}, {"type": "product"}, {"type": "profile"}]
)