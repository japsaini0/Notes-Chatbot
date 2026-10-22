# Notes Chatbot

A retrieval-augmented generation (RAG) chatbot that answers questions from your own study notes. It runs fully locally: local embeddings, a local vector database and a local LLM through Ollama, so your notes never leave your machine.

## Features

- Ingests a zip of notes (`.txt`, `.md`, `.pdf`, `.docx`, `.pptx`)
- Splits text into overlapping chunks and indexes them in ChromaDB
- Semantic search using `sentence-transformers` embeddings
- Answers grounded only in your notes, with source file names
- Chat history for follow-up questions
- Streamlit chat UI with a "Retrieved sources" panel
- Swappable LLM backend: any OpenAI-compatible API (Ollama by default)

## How it works

```
notes.zip -> extract -> convert to text -> chunk -> embed -> ChromaDB
                                                                |
question -> embed -> top-k similar chunks -> LLM prompt -> answer + sources
```

## Tech stack

Python, Streamlit, ChromaDB, sentence-transformers (`all-MiniLM-L6-v2`), Ollama (Qwen3), OpenAI Python client, pypdf, python-docx, python-pptx.

## Project structure

```
notes-chatbot/
├── app.py
├── requirements.txt
├── .env
├── .streamlit/config.toml
├── data/
│   ├── raw/          notes.zip goes here
│   ├── extracted/
│   └── text/
├── vectorstore/
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── convert.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── store.py
│   ├── retriever.py
│   ├── llm.py
│   └── pipeline.py
└── scripts/
    ├── build_index.py
    └── ask_cli.py
```

## Setup

1. Install [Ollama](https://ollama.com) and pull a model:

   ```
   ollama pull qwen3:1.7b
   ```

2. Create the environment and install dependencies:

   ```
   python -m venv venv
   venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```
   LLM_MODEL=qwen3:1.7b
   LLM_BASE_URL=http://localhost:11434/v1
   LLM_API_KEY=ollama
   ```

## Usage

1. Place your notes zip at `data/raw/notes.zip`
2. Build the index: `python -m scripts.build_index`
3. Chat in the terminal: `python -m scripts.ask_cli`
4. Or launch the UI: `streamlit run app.py`

Re-run step 2 whenever your notes change.

## Configuration

Edit `src/config.py`:

| Setting | Default | Meaning |
|---|---|---|
| `CHUNK_SIZE` | 800 | Characters per chunk |
| `CHUNK_OVERLAP` | 150 | Characters shared between neighbouring chunks |
| `TOP_K` | 4 | Chunks sent to the LLM per question |
| `HISTORY_TURNS` | 6 | Past messages included for follow-ups |

To use a hosted model instead, set `LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL` in `.env` for any OpenAI-compatible provider.

## Limitations

- Scanned or handwritten pages must be transcribed to text first
- Images and diagrams are not indexed
- Small local models can miss details in long answers

## Roadmap

- Vision model support for images in notes
- PDF page numbers in citations
- Hybrid keyword and semantic search
- Re-ranking of retrieved chunks
- Evaluation set to measure answer quality
