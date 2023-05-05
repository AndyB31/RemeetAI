import sys
from .stt import whisper_test
from .utils import extract_audio

def trancript(mediafile, audio = False):
  if not audio:
    audiofile = '.'.join(mediafile.split('.')[:-1]) + '.mp3'
    audio = extract_audio.extract_audio(mediafile, audiofile)
  else:
    audiofile = mediafile
  print (f"audiofile: {audiofile}")

  transcript1, transcript2 = whisper_test.speech_to_text(audiofile)

  print(transcript1.text, '[2]:\n', transcript2['text'])
  return (transcript1, transcript2)

def main():
  if len(sys.argv) < 2:
    sys.exit(1)

  t1, t2 = trancript(sys.argv[1])


if __name__ == '__main__':
  main()