import streamlit as st
import requests
import urllib.parse
import random

# ---------------- PAGE TITLE ----------------

st.title("My AI Image Generator")

# ---------------- SIDEBAR SETTINGS ----------------

st.sidebar.header("Settings")

art_style = st.sidebar.selectbox(
    "Select desired art style",
    [
        "Realistic",
        "Abstract",
        "Cartoon",
        "Anime",
        "Impressionist",
        "Sketch",
        "3D"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=768,
    step=64
)

# Magic Enhance Checkbox
magic_enhance = st.sidebar.checkbox(
    "✨ Enable Magic Enhance"
)


# ---------------- SURPRISE PROMPTS ----------------

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A giant dragon sleeping on top of a futuristic city",
    "A robot playing chess in space",
    "An underwater city where humans and mermaids live together"
]


# ---------------- IMAGE GENERATION FUNCTION ----------------

def generate_image(user_prompt):

  
    full_prompt = f"{user_prompt}, {art_style} style"

    if magic_enhance:
        full_prompt += (
            ", masterpiece, 8k resolution, highly detailed, "
            "trending on artstation, unreal engine 5 render"
        )

    encoded_prompt = urllib.parse.quote(full_prompt)


    url = (
        f"https://image.pollinations.ai/prompt/"
        f"{encoded_prompt}"
        f"?width={width}&height={height}"
    )

    try:

        with st.spinner("🎨 Rendering your image..."):

            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=60
            )

        if response.status_code == 200:

            st.success("✅ Image generated successfully!")

            st.image(
                response.content,
                caption=full_prompt,
                use_container_width=True
            )

            st.download_button(
                label="⬇️ Download Image",
                data=response.content,
                file_name=f"{art_style}_image.png",
                mime="image/png"
            )

        else:

            st.error(
                f"Failed to generate image. "
                f"Status Code: {response.status_code}"
            )

    except requests.exceptions.RequestException as error:

        st.error(f"Error connecting to image generation service: {error}")


# ---------------- USER PROMPT ----------------

user_prompt = st.text_input(
    "Describe the image you want to generate"
)


# ---------------- BUTTONS ----------------

generate_button = st.button("🎨 Generate Image")

surprise_button = st.button("🎲 Surprise Me!")


# ---------------- NORMAL GENERATION ----------------

if generate_button:

    if user_prompt:

        generate_image(user_prompt)

    else:

        st.warning("⚠️ Please enter an image description.")


# ---------------- SURPRISE ME FEATURE ----------------

if surprise_button:

    random_prompt = random.choice(surprise_prompts)

    st.info(
        f"✨ Surprise Prompt: {random_prompt}"
    )

    generate_image(random_prompt)
