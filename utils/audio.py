import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIRECTORY = "downloads"

os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)

def download_audio(url : str) -> str:
  output_path = os.path.join(DOWNLOAD_DIRECTORY, "%(title)s.%(ext)s")
  ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl" : output_path,
    "postprocessors" : [
      {
        "key" : "FFmpegExtractAudio",
        "preferredcodec": "wav",
        "preferredquality" : "192"
      }
    ],
    "quiet" : True
  }
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url=url, download=True)
    filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
  return filename


print(download_audio("https://www.youtube.com/watch?v=xlYJhtL0qbQ&t=554s"))