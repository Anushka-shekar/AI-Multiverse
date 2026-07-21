import os
from pathlib import Path
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

def speak(text: str, output_path: str = "output.mp3") -> str:

    if not text.strip():
        raise ValueError("Story text is empty.")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    tts.save(str(output_file))

    return str(output_file)
