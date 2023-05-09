from . import preprocess
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import nltk

try:
  from nltk.corpus import stopwords
except:
  nltk.download('stopwords')
  from nltk.corpus import stopwords

def count_words(texts):
  # Join all word corpus
  review_words = ','.join(texts)

  # Count and find the 30 most frequent
  counter = Counter(review_words.split())
  most_frequent = counter.most_common(30)

  # Bar plot of frequent words
  fig = plt.figure(1, figsize = (20,10))
  count = pd.DataFrame(most_frequent, columns=("words","count"))
  sns.barplot(x = 'words', y = 'count', data = count, palette = 'winter')
  plt.xticks(rotation=45)
  return count

def remove_stopwords(words, lang = 'french'):
  stopws = set(stopwords.words[lang])
  words_filtered = []
  for w in words:
    if w not in stopws:
        words_filtered.append(w)
  return words_filtered

def to_string(text):
  text = ' '.join(map(str, text))

def extract_topics(texts):
  texts = [remove_stopwords(preprocess(text)) for text in texts]
  texts_strings = list(map(to_string, texts))
  
  

