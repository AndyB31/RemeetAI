#!/bin/python
import sys
import moviepy.editor as mp
from typing import Type

def extract_audio(filepath: str, outfilepath: str = None) -> Type[mp.AudioFileClip]:
  clip = mp.VideoFileClip(filepath)

  if outfilepath:
    clip.audio.write_audiofile(outfilepath)
  return clip.audio

def main():
  print (sys.argv)
  if len(sys.argv) < 2:
    print("Please provide the filepath.")
    sys.exit(1)
  filepath = sys.argv[1]
  try:
    outfilepath = sys.argv[2]
  except:
    outfilepath = filepath.split('.')[0] + '.mp3'
  extract_audio(filepath, outfilepath)

if __name__ == '__main__':
  main()