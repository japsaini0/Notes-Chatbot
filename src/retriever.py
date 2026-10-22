from src import config, embedder, store


def retrieve(question, k=config.TOP_K):
    collection = store.get_collection()
    if collection.count() == 0:
        return []
    embedding = embedder.embed_texts([question])[0]
    return store.search(collection, embedding, k)