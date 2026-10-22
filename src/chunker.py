from src import config


def split_text(text, size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP):
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + size, length)
        if end < length:
            cut = text.rfind("\n", start, end)
            if cut <= start + size // 2:
                cut = text.rfind(" ", start, end)
            if cut > start + size // 2:
                end = cut
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= length:
            break
        start = max(end - overlap, start + 1)
    return chunks


def load_chunks():
    records = []
    for path in sorted(config.TEXT_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for index, piece in enumerate(split_text(text)):
            records.append(
                {
                    "id": f"{path.name}::{index}",
                    "text": piece,
                    "source": path.name,
                }
            )
    return records