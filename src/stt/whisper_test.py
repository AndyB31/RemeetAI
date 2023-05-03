import sys
import whisper
from typing import Type

def speech_to_text(audiofile: str):
  model = whisper.load_model("small")

  audio = whisper.load_audio(audiofile)
  audio = whisper.pad_or_trim(audio)

  mel = whisper.log_mel_spectrogram(audio).to(model.device)

  _, probs = model.detect_language(mel)
  print(f"Detected language: {max(probs, key=probs.get)}")

  options = whisper.DecodingOptions(fp16 = False)
  result = whisper.decode(model, mel, options)

  text = model.transcribe(audiofile)

  # print(result.text)
  return (result, text)

def main():
  audiofile = sys.argv[1]
  print (speech_to_text(audiofile)[1]['text'])

if __name__ == "__main__":
  main()