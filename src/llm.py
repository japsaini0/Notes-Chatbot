import os
import re

from openai import OpenAI

from src import config

SYSTEM_PROMPT = (
    "You are a study assistant that answers questions using only the provided context "
    "from the student's own notes. If the context does not contain the answer, say that "
    "the notes do not cover it instead of guessing. Mention the source file names you "
    "used at the end of your answer. Keep explanations clear and structured."
)

_client = None


def get_client():
    global _client
    if _client is None:
        _client = OpenAI(
            base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
            api_key=os.getenv("LLM_API_KEY", "ollama"),
        )
    return _client


def build_context(chunks):
    blocks = [f"[Source: {chunk['source']}]\n{chunk['text']}" for chunk in chunks]
    return "\n\n---\n\n".join(blocks)


def clean_output(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def generate_answer(question, chunks, history=None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history[-config.HISTORY_TURNS:])
    content = f"Context:\n{build_context(chunks)}\n\nQuestion: {question}"
    if "qwen3" in config.LLM_MODEL.lower():
        content += " /no_think"
    messages.append({"role": "user", "content": content})
    response = get_client().chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        temperature=0.2,
    )
    return clean_output(response.choices[0].message.content)