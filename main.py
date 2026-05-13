from dotenv import load_dotenv
from utils.audio import process_input
from core.transcriber import transcribe_all
from core.main_executer import build_rag_chain, ask_question
from core.summarize import transcript_summary, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions

load_dotenv()

def run_pipeline(source: str, language: str = "english") -> dict:
  print("AI Assistant Starting")
  
  chunks = process_input(source=source)
  transcript = transcribe_all(chunks=chunks, language=language)
  
  print("Raw Transcription (first 300 characters)", transcript[:300])
  
  title = generate_title(transcript=transcript)
  video_summary = transcript_summary(transcript=transcript)
  action_item = extract_action_items(transcript=transcript)
  decisions = extract_key_decisions(transcript=transcript)
  questions = extract_questions(transcript=transcript)
  
  rag_chain = build_rag_chain(transcript=transcript)
  
  return {
    "title": title,
    "transcript": transcript,
    "summary": video_summary,
    "action_items": action_item,
    "decisions": decisions,
    "questions": questions,
    "rag_chain": rag_chain
  }


if __name__ == "__main__":
  # CLI entry point
  source = input("Enter YouTube URL or local file path: ").strip()
  language = input("Language (english/hinglish): ").strip() or "english"
  result = run_pipeline(source, language)

  print("\n" + "=" * 60)
  print(f"📌 Title: {result['title']}")
  print(f"\n📋 Summary:\n{result['summary']}")
  print(f"\n✅ Action Items:\n{result['action_items']}")
  print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
  print(f"\n❓ Open Questions:\n{result['open_questions']}")
  print("=" * 60)

  # Phase 2 — Chat with your meeting via RAG
  print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
  rag_chain = result["rag_chain"]
  while True:
    question = input("You: ").strip()
    if question.lower() in ["exit", "quit", "q"]:
      print("👋 Goodbye!")
      break
    if not question:
        continue
    answer = ask_question(rag_chain, question)
    print(f"\n🤖 Assistant: {answer}\n")