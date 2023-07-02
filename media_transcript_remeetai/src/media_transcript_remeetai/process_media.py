import sys
from .stt import whisper_stt
from .utils import extract_audio
from .clean_text import clean_duplicate
from .utils import debug

def trancript(mediafile: str, audio: bool = False):
  if not audio:
    audiofile = '.'.join(mediafile.split('.')[:-1]) + '.mp3'
    afilename = audiofile.split('/')[-1]
    afilepath = audiofile.replace(f"/{afilename}", "")
    audio_clip, i = extract_audio.extract_audio(mediafile, outfilepath=afilepath, outfilename=afilename)
    audiofile = f"{afilepath}/1_{afilename}"
  else:
    audiofile = mediafile
  debug.print_debug(f"audiofile: {audiofile}")

  transcript1, transcript2, t_en = whisper_stt.speech_to_text(audiofile)

  t_clean = "tc"
  # t_clean = clean_duplicate.remove_duplicates(transcript2["text"])
  t_en_clean = transcript2
  # t_en_clean = clean_duplicate.remove_duplicates(transcript2["text"])
  t_clean = t_en_clean
  debug.print_debug(f"t_clean: {t_clean}")

  return (t_clean, t_en_clean, transcript1, transcript2)

def iter_transcript_chunk(mediafile: str):
  audiofile = '.'.join(mediafile.split('.')[:-1]) + '.mp3'
  afilename = audiofile.split('/')[-1]
  afilepath = audiofile.replace(f"/{afilename}", "")
  audio_clip, i = extract_audio.extract_audio(mediafile, outfilepath=afilepath, outfilename=afilename)


  for y in range(i):

    chunkfile = f"{y+1}_{afilename}"

    debug.print_debug(f"chunkfile: {chunkfile}")

    transcript1, transcript2, t_en = whisper_stt.speech_to_text(f"{afilepath}/{chunkfile}")

    t_clean = "tc"
    # t_clean = clean_duplicate.remove_duplicates(transcript2["text"])
    t_en_clean = transcript2["text"]
    # t_en_clean = clean_duplicate.remove_duplicates(transcript2["text"])
    t_clean = t_en_clean
    debug.print_debug(f"t_clean: {t_clean}")

    yield t_clean
# def main():
#   if len(sys.argv) < 2:
#     sys.exit(1)

#   t, t1, t2 = trancript(sys.argv[1])


# if __name__ == '__main__':
#   main()