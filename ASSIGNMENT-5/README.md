
WATCH DEMO : 
 
Phase 1: The Director's Cut (UI & Configuration)
● Use @st.cache_resource to securely cache your Gemini client.
● Create a sidebar titled "Story Settings" with dropdowns for Story Genre and Art Style .
● Initialize st.session_state to store your chat history and the Gemini chat object.
Phase 2: The Structured JSON Engine (Research Required)
Currently, your AI just outputs a paragraph of text. For a true visual novel, the AI must give the

user specific choices.
● Your Task: You must instruct Gemini via your system prompt to strictly return its response

as a JSON Object containing three specific keys:
1. story_text: The narrative paragraph.
2. image_prompt: A heavily engineered prompt for the Pollinations API.
3. options: A Python list containing 2 to 3 distinct choices for the user's next action.
● The Engineering Challenge: You must research Python's built-in json library (import json)

to parse the AI's string response into a usable Python dictionary.

Phase 3: Dynamic UI Generation (Research Required)
Because the AI is generating the choices, you cannot use st.chat_input().
● Your Task: You must write a for loop that iterates over the options list from your parsed

JSON and dynamically generates an st.button() for each choice.
● If a user clicks one of those dynamically generated buttons, that specific text should be

sent to the Gemini API as their next move.
Phase 4: Multi-Media Rendering & TTS (Research Required)
● The Visuals: Send the parsed image_prompt to the Pollinations API, download the image,

and render both the story_text and the image on the screen using st.session_state so they

don't disappear.
● The Audio: A true visual novel has sound. You must independently research how to use a

Python Text-to-Speech (TTS) library (such as gTTS - Google Text-to-Speech) to convert

the AI's story_text into an audio file.
● Use Streamlit's st.audio() component to play the generated narration file directly inside the

browser.
Phase 5: Graceful Failures (Research Required)
● APIs fail. Networks time out. If Pollinations is busy, your entire app will crash with a massive
