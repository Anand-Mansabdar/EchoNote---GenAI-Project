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


# Transcribe a single chunk
def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:
  model = load_model()
  task = "translate" if translate else "transcribe"
  
  result = model.transcribe(chunk_path, task = task)
  
  return result["text"]

# Transscribing multiple chunks
def transcribe_all_chunks(chunks: list, translate: bool = False) -> str:
  final_transcription = ""
  
  for i, chunk in enumerate(chunks):
    print(f"Transcribing Chunk {i+1}")
    text = transcribe_chunk(chunk_path= chunk, translate = translate)
    
    final_transcription += text + " "
  
  print("Transcription Completed")
  return final_transcription