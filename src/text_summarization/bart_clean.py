# -*- coding: utf-8 -*-
"""Bart_clean.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hhCxfI6PamF6395da5WAYrRgIHjRYlDR
"""

from transformers import pipeline, set_seed
from transformers import AutoTokenizer
from deep_translator import GoogleTranslator,single_detection
import re

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

def bart_sum(filename: str = None, text_base: str = None):
    if not filename and not text_base:
        raise Exception("filename or text must be specified.")
    
    if filename:
        with open(filename, "r") as f:
            text = f.read()
    else:
        text = text_base
    #remove non breaking space 
    text = text.replace("\xa0", " ")
    #remove not usefull white space 
    text = re.sub("\s+", " ", text)
    # Print the variable
    print(text)

    token_ids = tokenizer.encode_plus(text, max_length=1000, truncation=True)
    short_text_truncated = tokenizer.decode(token_ids["input_ids"]) # decode
    short_text_truncated = short_text_truncated[3:-4]

    #for prototype use this one 
    summarize_high_beams = summarizer(short_text_truncated, do_sample=False, num_beams=7, num_return_sequences=1)
    print(summarize_high_beams)
    summarize_low_beams = summarizer(short_text_truncated, do_sample=False, num_beams=3, num_return_sequences=2)
    print(summarize_low_beams)