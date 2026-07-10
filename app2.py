import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# --------------------------
# Load API Key
# --------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------
# Page Configuration
# --------------------------

st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="centered"
)

st.title("🌌 AI MULTIVERSE")
st.write("Talk to anyone from any universe.")

# --------------------------
# Sidebar
# --------------------------

st.sidebar.title("Settings")

mode = st.sidebar.radio(
    "Choose Personality Mode",
    ["Preset", "Custom"]
)

if mode == "Preset":

    personality = st.sidebar.selectbox(
        "Choose Personality",
        [
            "Sherlock Holmes",
            "Albert Einstein",
            "Donald Trump",
            "Cristiano Ronaldo",
            "Virat Kohli",
            "Iron Man",
            "Batman",
            "Deadpool",
            "Elon Musk",
            "Motivational Coach"
        ]
    )

else:

    personality = st.sidebar.text_input(
        "Enter Any Personality",
        placeholder="Example: Harry Potter"
    )

if personality == "":
    personality = "Helpful Assistant"

# --------------------------
# Session State
# --------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# New Chat Button
# --------------------------

if st.sidebar.button("🗑️ New Chat"):
    st.session_state.messages = []
    st.rerun()

# --------------------------
# Display Chat History
# --------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------
# Chat Input
# --------------------------

prompt = st.chat_input("Type your message...")

if prompt:

    # Store User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------
    # Build Conversation
    # --------------------------

    system_prompt = f"""
You are permanently roleplaying as {personality}.

Rules:

- Never say you are an AI.
- Never break character.
- Behave exactly like {personality}.
- Reply naturally.
- Be expressive.
- Continue the conversation normally.
- Remember previous messages.
"""

    conversation = system_prompt + "\n\n"

    for msg in st.session_state.messages:

        conversation += f"{msg['role']}: {msg['content']}\n"

    # --------------------------
    # Gemini Response
    # --------------------------

    with st.chat_message("assistant"):

        with st.spinner("Connecting to the Multiverse..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation
            )

            answer = response.text

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )