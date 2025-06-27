from ml.models.wav2vec2_model import ArabicWav2Vec2

model = ArabicWav2Vec2()
text = model.transcribe("cleaned.wav")

print("📖 Transcribed Text:\n", text)
