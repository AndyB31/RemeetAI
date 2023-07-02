#!/bin/python
import sys
import moviepy.editor as mp
from moviepy.audio.AudioClip import AudioArrayClip
from typing import Type

# chunk_size in second define length of subclips
def extract_audio(filepath: str, outfilepath: str = None, outfilename: str = None, chunk: bool = False, chunk_size: int = 60) -> Type[mp.AudioFileClip]:
  clip = mp.VideoFileClip(filepath)

  i = 1
  clips = []
  if chunk:
    fps = clip.audio.fps
    its = clip.audio.iter_chunks(chunk_duration=chunk_size)
    for it in its:
      aaclip = AudioArrayClip(it, fps=fps)
      clips.append(aaclip)
      if outfilepath:
        aaclip.write_audiofile(f"{outfilepath}/{i}_{outfilename}")
      i += 1
  else:
    clips.append(clip.audio)
    if outfilepath:
      clip.audio.write_audiofile(f"{outfilepath}/1_{outfilename}")
  return (clips, i)

# def main():
#   if len(sys.argv) < 2:
#     print("Please provide the filepath.")
#     sys.exit(1)
#   filepath = sys.argv[1]
#   try:
#     outfilepath = sys.argv[2]
#   except:
#     outfilepath = ''.join(filepath.split('.')[:-1]) + '.mp3'
#   extract_audio(filepath, outfilepath)

# if __name__ == '__main__':
#   main()