import chromadb

from src import config

BATCH_SIZE = 500


def get_client():
    config.VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(config.VECTOR_DIR))


def get_collection():
    return get_client().get_or_create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection():
    client = get_client()
    try:
        client.delete_collection(config.COLLECTION_NAME)
    except Exception:
        pass
    return client.create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(collection, records, embeddings):
    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start:start + BATCH_SIZE]
        collection.add(
            ids=[item["id"] for item in batch],
            documents=[item["text"] for item in batch],
            metadatas=[{"source": item["source"]} for item in batch],
            embeddings=embeddings[start:start + BATCH_SIZE],
        )


def search(collection, embedding, k):
    result = collection.query(query_embeddings=[embedding], n_results=k)
    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]
    return [
        {"text": doc, "source": meta["source"], "distance": dist}
        for doc, meta, dist in zip(documents, metadatas, distances)
    ]