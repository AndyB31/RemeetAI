
# https://paperswithcode.com/task/abstractive-text-summarization

# Abstractive summarization with BART model fine tuned on CNN daily mail 
# 


from transformers import pipeline, set_seed
from transformers import AutoTokenizer

# Import stopwords module
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download("all")

# Import the regular expression module
import re

import pprint as pprint

def bart_sum(file: str = None, text: str = None):
  if file:
    with open(file, "r") as f:
      short_aws_resume = f.read()
  else:
    short_aws_resume = text

  #remove non breaking space 
  short_aws_resume = short_aws_resume.replace("\xa0", " ")
  #remove not usefull white space 
  short_aws_resume = re.sub("\s+", " ", short_aws_resume)
  # Print the variable
  print(short_aws_resume)

  summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
  tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

  # Calculate the length of each part
  part_length = len(short_aws_resume) // 3

  # Get the first part by slicing from the start to part_length
  first_part = short_aws_resume[:part_length]
  # Get the second part by slicing from part_length to part_length * 2
  second_part = short_aws_resume[part_length:part_length * 2]
  # Get the third part by slicing from part_length * 2 to the end
  third_part = short_aws_resume[part_length * 2:]

  print(summarizer(first_part, max_length=130, min_length=30, do_sample=True, num_return_sequences=4))
  print(summarizer(second_part, max_length=130, min_length=30, do_sample=False))
  print(summarizer(third_part, max_length=130, min_length=30, do_sample=False))

  # Removing stop words to compare quality of summaries without them 
  # Tokenize your string into words
  words = word_tokenize(first_part)

  # Define the stop words for both languages
  stop_words = stopwords.words("english") + stopwords.words("french")

  # Remove the stop words from your words
  filtered_words = [word for word in words if word not in stop_words]

  # Print the filtered words
  print(filtered_words)
  print(len(filtered_words))
  first_part_without_stopwords = " ".join(filtered_words)
  print(summarizer(first_part, max_length=512, min_length=56, do_sample=False, num_beams=5, num_return_sequences=3))
  print(first_part)
  print(summarizer(first_part_without_stopwords, max_length=512, min_length=56, do_sample=False, num_beams=5, num_return_sequences=3))
  print(summarizer(first_part_without_stopwords, max_length=478, min_length=160, do_sample=False, num_beams=7, num_return_sequences=2))

  # **Using maximum tokens size to increase summaries quality**
  token_ids = tokenizer.encode_plus(short_aws_resume, max_length=1024, truncation=True)
  print(token_ids)
  short_aws_resume_truncated = tokenizer.decode(token_ids["input_ids"]) # decode
  print(short_aws_resume_truncated) 
  short_aws_resume_truncated = short_aws_resume_truncated[3:-4]
  print(short_aws_resume_truncated) 
  summarize = summarizer(short_aws_resume_truncated, max_length=1024, min_length=526, do_sample=False, num_beams=7, num_return_sequences=2)
  for elem in summarize:
    pprint.pprint(elem["summary_text"].replace("\xa0", " "))

  return summarize

  # **Using GPT2 to generate sentence from keywords**
  # keywords_sentence = "last month celebrity parties Harry Potter star Daniel Radcliffe Harry Potter fast cars party Potter author Rudyard Kipling Part II Rudyard Kipling the UK box office chart kid star DVDs Reuters gossip columnists Australian release fair game UK an Australian film Daniel Radcliffe the horror film a massive sports car collection wraps Potters latest » Hostel: Part II"
  # generator = pipeline('text-generation', model='gpt2')
  # set_seed(42)
  # generator(keywords_sentence, max_length=100, num_return_sequences=5)


