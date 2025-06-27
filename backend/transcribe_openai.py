import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio_file_path = "sample_recitation.wav"

with open(audio_file_path, "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language="ar"
    )

print("📖 Transcribed Text:\n", transcript.text)
