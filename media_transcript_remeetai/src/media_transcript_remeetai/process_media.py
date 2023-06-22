import sys
from .stt import whisper_stt
from .utils import extract_audio
from .clean_text import clean_duplicate
from .utils import debug

def trancript(mediafile: str, audio: bool = False):
  if not audio:
    audiofile = '.'.join(mediafile.split('.')[:-1]) + '.mp3'
    audio = extract_audio.extract_audio(mediafile, audiofile)
  else:
    audiofile = mediafile
  debug.print_debug(f"audiofile: {audiofile}")

  transcript1, transcript2, t_en = whisper_stt.speech_to_text(audiofile)

  t_clean = "tc"
  # t_clean = clean_duplicate.remove_duplicates(transcript2["text"])
  t_en_clean = clean_duplicate.remove_duplicates(transcript2["text"])
  t_clean = t_en_clean

  return (t_clean, t_en_clean, transcript1, transcript2)

# def main():
#   if len(sys.argv) < 2:
#     sys.exit(1)

#   t, t1, t2 = trancript(sys.argv[1])


# if __name__ == '__main__':
#   main()