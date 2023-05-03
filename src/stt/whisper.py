import whisper
from typing import Type

def speech_to_text(audiofile: str) -> Type[whisper.DecodingResult]:
  model = whisper.load_model("small")

  audio = whisper.load_audio(audiofile)
  audio = whisper.pad_or_trim(audio)

  mel = whisper.log_mel_spectrogram(audio).to(model.device)

  _, probs = model.detect_language(mel)
  print(f"Detected language: {max(probs, key=probs.get)}")

  options = whisper.DecodingOptions()
  result = whisper.decode(model, mel, options)

  # print(result.text)
  return (result)