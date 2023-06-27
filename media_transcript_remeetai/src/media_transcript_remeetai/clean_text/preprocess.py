import re
import nltk

def text_preprocessing(text):
  # Convert words to lower case
  text = text.lower()
  
  # # Expand contractions
  # if True:
  #     text = text.split()
  #     new_text = []
  #     for word in text:
  #         if word in contractions:
  #             new_text.append(contractions[word])
  #         else:
  #             new_text.append(word)
  #     text = " ".join(new_text)
      
  # Format words and remove unwanted characters
  text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
  text = re.sub(r'\<a href', ' ', text)
  text = re.sub(r'&amp;', '', text) 
  text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
  text = re.sub(r'<br />', ' ', text)
  text = re.sub(r'\'', ' ', text) 

  # Tokenize each word
  text = nltk.WordPunctTokenizer().tokenize(text)

  # Lemmatize each word
  text = [nltk.stem.WordNetLemmatizer().lemmatize(token, pos='v') for token in text if len(token)>1]

  return text