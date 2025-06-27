from utils.audio_utils import record_audio
from ml.transcriber import transcribe_audio
from scripts.ayah_matcher import find_most_similar_ayah


import sys
import os
sys.path.append(os.path.abspath("."))




def run_voice_to_ayah_pipeline():
    """
    End-to-end voice recognition pipeline using Whisper and ayah matching.

    Steps:
        1. Record audio from mic
        2. Transcribe using Whisper
        3. Embed and match to closest ayah using cosine similarity

    Invariants:
        - Input is live spoken Arabic of a Quranic verse.
        - Output includes top ayah matches sorted by similarity.
    """
    audio_path = record_audio(duration=30, samplerate=16000)

    print("📜 Transcribing...")
    transcript = transcribe_audio(audio_path)
    print("🧠 Transcript:", transcript)

    print("🔍 Matching to ayah...")
    matches = find_most_similar_ayah(transcript)

    for r in matches:
        print(f"Surah {r['surah']}, Ayah {r['ayah']} — Score: {r['similarity']:.3f}")
        print("Arabic:", r["arabic_text"])
        print("English:", r["english_text"])
        print("-" * 40)

if __name__ == "__main__":
    run_voice_to_ayah_pipeline()
