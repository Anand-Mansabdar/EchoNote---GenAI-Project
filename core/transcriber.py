import os
import whisper

whisper_model = os.getenv("WHISPER_MODEL", default="small")

_model = None

# Function to Load Whisper Model
def load_model():
  global _model
  
  if _model is None:
    print(f"Loading model...")
    _model = whisper.load_model(whisper_model)
    print(f"Whisper Model loaded successfully...")
  return _model