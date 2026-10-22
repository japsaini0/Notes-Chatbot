from src import llm, retriever

EMPTY_MESSAGE = (
    "The knowledge base is empty. Run `python -m scripts.build_index` after placing "
    "your notes zip in data/raw/."
)


def ask(question, history=None):
    chunks = retriever.retrieve(question)
    if not chunks:
        return EMPTY_MESSAGE, []
    answer = llm.generate_answer(question, chunks, history)
    return answer, chunks