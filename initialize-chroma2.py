from chromadb import HttpClient
import os
from dotenv import load_dotenv

load_dotenv()

client = HttpClient(host=os.getenv("CHROMADB_HOST"))

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