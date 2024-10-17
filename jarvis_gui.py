import streamlit as st
import ollama

# Set Streamlit to use dark mode (configure theme in config.toml)
st.set_page_config(page_title="Jarvis Command Center", layout="centered")

# CSS for Dark Mode customization
dark_mode_css = """
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .stTextInput > div > div > input {
            background-color: #333333;
            color: white;
        }
        .stButton > button {
            background-color: #333333;
            color: white;
        }
    </style>
    """
st.markdown(dark_mode_css, unsafe_allow_html=True)

st.title("This is a GUI for Jarvis, My second Year Project")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': 
            prompt}])
    msg = response["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)