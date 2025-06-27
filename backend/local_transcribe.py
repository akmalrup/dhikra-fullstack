import whisper

model = whisper.load_model("medium")  # or "base" if you have low RAM

result = model.transcribe("sample_recitation.wav", task = "translate" )

print("📖 Transcribed Text:\n", result["text"])
