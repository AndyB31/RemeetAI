# -*- coding: utf-8 -*-
"""TextRank_LSA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11T0Su3eURmKcVmetsWeitQO5Ya9DJdNx
"""

# Import libraries
import spacy
import pytextrank
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import nltk

from ..utils import debug

nltk.download("punkt")

# Setting path to the text file
file_name = ("./AWS - 1 (trimmed)2.txt")

def lsa_sum(filename: str = None, text_base: str = None, outpath: str = None, sentences_number: int = 5):
    if not filename and not text_base:
        raise Exception("filename or text must be specified.")
    if filename:
        # Loading the text file as a list of sentences
        with open(filename, mode='rt', encoding='utf-8') as fp:
            text = fp.read()
    else:
        text = text_base

    # Use LsaSummarizer from sumy library
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer_lsa = LsaSummarizer()
    summary_lsa = summarizer_lsa(parser.document, sentences_number) #  user input sentences number
    text_summary_lsa = ""
    for sentence in summary_lsa:
        text_summary_lsa += str(sentence)
    debug.print_debug("Summary by LsaSummarizer:")
    debug.print_debug(text_summary_lsa)

    if outpath:
        # Opening the summary file in write mode
        with open(outpath, mode='w', encoding='utf-8') as fp:
            # Write each string in the list to a separate line
            for sentence in summary_lsa:
                fp.write(str(sentence) + "\n")
    return text_summary_lsa

def textrank_sum(filename: str = None, text_base: str = None, outpath: str = None, sentences_number: int = 5):
    if not filename and not text_base:
        raise Exception("filename or text must be specified.")
    if filename:
        # Loading the text file as a list of sentences
        with open(filename, mode='rt', encoding='utf-8') as fp:
            text = fp.read()
    else:
        text = text_base
    # Use TextRank from pytextrank library
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank", last=True)
    doc = nlp(text)
    summary_textrank = doc._.textrank.summary(limit_phrases=sentences_number*3, limit_sentences=sentences_number) # user input sentences number
    debug.print_debug("Summary by TextRank:")
    sentenced_summary_textrank = []
    for sentence in summary_textrank:
        debug.print_debug(sentence)
    sentenced_summary_textrank.append(str(sentence))

    if outpath:
        # Open a new file in write mode
        with open(outpath, "w") as file:
            # Write each string in the list to a separate line
            for sentence in sentenced_summary_textrank:
                file.write(sentence + "\n")

    return '\n'.join(sentenced_summary_textrank)