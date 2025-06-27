import sounddevice as sd
from scipy.io.wavfile import write
import tempfile



sd.default.device = (1, None)
def record_audio(duration=7, samplerate=16000):
    """
    Record audio from the microphone and save it as a temporary WAV file.

    Args:
        duration (int): Duration of recording in seconds.
        samplerate (int): Sample rate in Hz. Must be 16000 for Whisper compatibility.

    Returns:
        str: File path to the temporary WAV file.

    Invariants:
        - Output file is a valid PCM-encoded 16-bit mono WAV file at 16kHz.
        - Whisper can directly use the returned file path for transcription.
    """
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_wav.name, samplerate, audio)
    #print(f"📁 Saved audio to: {temp_wav.name}")
    return temp_wav.name
