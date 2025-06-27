from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class ArabicWav2Vec2:
    def __init__(self):
        self.processor = Wav2Vec2Processor.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")
        self.model = Wav2Vec2ForCTC.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-arabic")

    def transcribe(self, audio_path):
        import librosa, torch

        speech, rate = librosa.load(audio_path, sr=16000)
        input_values = self.processor(speech, return_tensors="pt", sampling_rate=16000).input_values

        with torch.no_grad():
            logits = self.model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]

        return transcription
