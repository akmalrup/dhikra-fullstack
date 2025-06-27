import whisper
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
import os
import warnings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")

import whisper

# Load Whisper model once
model = whisper.load_model("medium")  # use "medium" or "large" for better accuracy

def transcribe_audio(filepath):
    result = model.transcribe(filepath, task="translate", language="ar")
    return result["text"]
