from chromadb import HttpClient
client = HttpClient(host="chromadb-842779538385.us-central1.run.app", ssl=True)
collection = client.get_collection("knowledge_base")
results = collection.get(where={"type": "conversation"})
print(results)