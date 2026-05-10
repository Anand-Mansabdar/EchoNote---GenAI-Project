import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

def get_model():
  return ChatMistralAI(model="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY"), temperature=0.3)


def split_transcript(transcript:str) -> list:
  splitter = RecursiveCharacterTextSplitter(
    chunk_size = 3000,
    chunk_overlap = 200
  )
  
  return splitter.split_text(text=transcript)


def transcript_summary(transcript:str) -> str:
  model = get_model()
  
  map_prompt= ChatPromptTemplate.from_messages(
    [
      ("system", "Summarize this portion of a meeting transcript concisely."),
      ("human", "{text}")
    ]
  )
  
  map_chain = map_prompt | model | StrOutputParser()
  chunks = split_transcript(transcript=transcript)
  
  chunk_summary = [map_chain.invoke({"text" : chunk}) for chunk in chunks]
  
  final_summary = "\n\n".join(chunk_summary)
  
  combined_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert meeting summarizer. Combine these partial summaries into onefinal professional meeting summary in bullet points."),
    ("human", "{text}")
  ])
  
  combined_chain = (
    RunnablePassthrough() | RunnableLambda(lambda x : {"text" : x}) | combined_prompt | model | StrOutputParser()
  )
  
  return combined_chain.invoke(final_summary)


def generate_title(transcript : str) -> str:
  model = get_model()

  title_chain = (
    RunnablePassthrough() | RunnableLambda(lambda x : {"text" : x}) | ChatPromptTemplate.from_messages([
      ("system", "Based on the meeting transcript, generate a short professional meeting title(max 8 words). Only return the title and nothing else"),
      ("human", "{text}")
    ]) | model | StrOutputParser()
  )
  
  return title_chain.invoke(transcript[:2000])