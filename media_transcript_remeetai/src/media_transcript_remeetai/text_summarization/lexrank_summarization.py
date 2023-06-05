# https://iq.opengenus.org/lexrank-text-summarization/

# Importing the required packages
from ..utils import debug
from lexrank import STOPWORDS, LexRank

# Setting path to the text file
# file_name = ("./AWS - 1 (trimmed)2.txt")

def lexrank_sum(filename: str = None, text_base: str = None, outpath: str = None):
    if not filename and not text_base:
        raise Exception("filename or text must be specified.")
    
    if filename:
      with open(filename, mode='rt', encoding='utf-8') as fp:
          text = fp.read()
    else:
       text = text_base

    # Creating a LexRank instance
    lxr = LexRank([text], stopwords=STOPWORDS['fr'])
    # Splitting the text by space
    words = text.split()
    # Computing the number of words
    num_words = len(words)
    # Splitting the text by "."
    sentences = text.split(".")
    # Computing the number of sentences
    num_sentences = len(sentences)
    # Calculating the average sentence length in words
    average_length = num_words / num_sentences
    debug.print_debug(average_length)
    user_summary_size_sentence = 9 #user input parameter
    # Setting the desired summary size in words
    summary_size_words = average_length * user_summary_size_sentence 
    # Estimating the summary size in sentences
    summary_size_sentences = int(summary_size_words / average_length)
    # Summarizing the text with summary_size_sentences total
    summary = lxr.get_summary(sentences, summary_size=summary_size_sentences)

    if outpath:
      # Opening the summary file in write mode
      with open(outpath, mode='wt', encoding='utf-8') as fp:
          # Writing the summary to the file
          fp.write('\n'.join(summary))

    # Printing the summary
    return '\n'.join(summary)

