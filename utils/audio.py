import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIRECTORY = "downloads"

os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)

def download_audio(url : str) -> str:
  output_path = os.path.join(DOWNLOAD_DIRECTORY, "%(title)s.%(ext)s")
  ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_path,
    "noplaylist": True,
    "quiet": False,
    "cookiefile": "cookies.txt",
    "postprocessors": [
      {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "wav",
        "preferredquality": "192",
      }
    ],
  }
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url=url, download=True)
    filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
  return filename


data = download_audio("https://www.youtube.com/watch?v=3GiS5xJoYRE")

def convert_to_wav(input : str) -> str:
  output_path = os.path.splitext(input)[0] + "_converted.wav"
  audio = AudioSegment.from_file(input)
  audio = audio.set_channels(1).set_frame_rate(16000)
  audio.export(output_path, format="wav")
  return output_path

print(convert_to_wav(data))