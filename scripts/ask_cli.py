from src.pipeline import ask


def main():
    history = []
    print("Notes chatbot. Type 'exit' to quit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue
        answer, chunks = ask(question, history)
        print(f"\nBot: {answer}\n")
        sources = sorted({chunk["source"] for chunk in chunks})
        if sources:
            print("Sources:", ", ".join(sources), "\n")
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()