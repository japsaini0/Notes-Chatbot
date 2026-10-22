import streamlit as st

from src.pipeline import ask

st.set_page_config(page_title="Notes Chatbot", page_icon="📚", layout="centered")

st.title("📚 Notes Chatbot")
st.caption("Ask questions and get answers from your own notes.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Controls")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("Run `python -m scripts.build_index` after adding new notes.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Retrieved sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['source']}**")
                    st.text(source["text"])

question = st.chat_input("Ask something about your notes")

if question:
    history = [
        {"role": item["role"], "content": item["content"]}
        for item in st.session_state.messages
    ]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your notes..."):
            try:
                answer, chunks = ask(question, history)
            except Exception as error:
                answer, chunks = f"Error: {error}", []
        st.markdown(answer)
        if chunks:
            with st.expander("Retrieved sources"):
                for chunk in chunks:
                    st.markdown(f"**{chunk['source']}**")
                    st.text(chunk["text"])

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": chunks}
    )