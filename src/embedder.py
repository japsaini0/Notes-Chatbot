from sentence_transformers import SentenceTransformer

from src import config

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model


def embed_texts(texts, show_progress=False):
    vectors = get_model().encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=show_progress,
    )
    return vectors.tolist()