from utils.audio_utils import record_audio
from ml.transcriber import transcribe_audio
from scripts.ayah_matcher import find_most_similar_ayah
from hifz.tracker import HifzTracker

class SessionManager:
    def __init__(self):
        self.tracker = None
        self.surah = None
        self.ayah_history = []
        self.session_active = False

    def reset_session(self):
        self.tracker = None
        self.surah = None
        self.ayah_history = []
        self.session_active = False
        print("🔁 Session reset.\n")

    def run_session(self):
        print("📿 Hifz Session Started. Begin reciting...\n")
        self.reset_session()

        try:
            while True:
                audio_path = record_audio(duration=7, samplerate=16000)
                transcript = transcribe_audio(audio_path)
                print(f"Transcript: {transcript}")

                # Match ayahs (filtered after session starts)
                matches = find_most_similar_ayah(
                    transcript,
                    surah_filter=self.surah if self.session_active else None
                )

                if not matches:
                    print("No match found.")
                    continue

                best = matches[0]
                surah = best["surah"]
                ayah = best["ayah"]
                similarity = best["similarity"]

                # Set appropriate similarity threshold
                min_similarity = 0.59 if not self.session_active else 0.35
                if similarity < min_similarity:
                    print(f"Match below similarity threshold ({similarity:.2f} < {min_similarity}). Try again.")
                    continue

                # First ayah → start session
                if not self.session_active:
                    self.surah = surah
                    self.tracker = HifzTracker(surah_num=surah, total_ayahs=999)  # TODO: pull actual count
                    self.tracker.expected = ayah + 1
                    self.ayah_history.append(ayah)
                    self.session_active = True
                    print(f"🎯 Starting session at Surah {surah}, Ayah {ayah}")
                    continue

                # Mid-session validation
                if surah != self.surah:
                    print(f" *WRONG SURAH* Expected Surah {self.surah}, got {surah}.")
                    continue

                status = self.tracker.update(ayah)
                self.ayah_history.append(ayah)

                print(f" Surah {surah}, Ayah {ayah} — {status.upper()} (score: {similarity:.2f})")
                print("-" * 40)

        except KeyboardInterrupt:
            print("\n🛑 Session ended by user.")
            self.reset_session()
