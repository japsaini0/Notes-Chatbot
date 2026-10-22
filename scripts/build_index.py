from src import chunker, embedder, store
from src.convert import convert_all
from src.extract import extract_zip


def main():
    print("Extracting zip...")
    extract_zip()

    print("Converting files to text...")
    converted, skipped = convert_all()
    print(f"Converted: {len(converted)} files")
    if skipped:
        print(f"Skipped: {len(skipped)} files")
        for name in skipped:
            print(f"  - {name}")

    print("Chunking...")
    records = chunker.load_chunks()
    print(f"Total chunks: {len(records)}")
    if not records:
        print("Nothing to index.")
        return

    print("Embedding...")
    embeddings = embedder.embed_texts([item["text"] for item in records], show_progress=True)

    print("Saving to vector store...")
    collection = store.reset_collection()
    store.add_chunks(collection, records, embeddings)
    print(f"Done. {collection.count()} chunks indexed.")


if __name__ == "__main__":
    main()