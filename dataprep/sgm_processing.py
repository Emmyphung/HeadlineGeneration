import os
import sys
import string
import nltk
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from nltk.stem.porter import *
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.model_selection import train_test_split

# 'tokenize' function adopted from @https://github.com/ankailou/reuters-preprocessing/blob/master/preprocess.py
def tokenize(text):
    """ function: tokenize
        ------------------
        generate list of tokens given a block of @text;
        :param text: string representing text field (title or body)
        :returns: list of strings of tokenized & sanitized words
    """
#     # encode unicode to string
#     ascii = text.encode('ascii', 'ignore')
    # remove digits
    no_digits = text.translate(str.maketrans('','',string.digits))
    # remove punctuation
    no_punctuation = no_digits.translate(str.maketrans('','',string.punctuation))
    # tokenize
    tokens = nltk.word_tokenize(no_punctuation)
    # remove stopwords - assume 'reuter'/'reuters' are also irrelevant
    no_stop_words = [w for w in tokens if not w in stopwords.words('english')]
    # filter out non-english words
    eng = [y for y in no_stop_words if wordnet.synsets(y)]
#     # lemmatization process
#     lemmas = []
#     lmtzr = WordNetLemmatizer()
#     for token in eng:
#         lemmas.append(lmtzr.lemmatize(token))
#     # stemming process
#     stems = []
#     stemmer = PorterStemmer()
#     for token in lemmas:
#         stems.append(stemmer.stem(token).encode('ascii','ignore'))
#     # remove short stems
#     terms = [x for x in stems if len(x) >= 4]
    return eng

def generate_pairs(folder):
    data = {'body': [], 'title': []}
    for file in os.listdir(folder):
        if file.endswith(".sgm"):
            print("Opening", file)
            try:
                sgm = open(os.path.join(os.getcwd(), folder, file), 'r', encoding='utf-8')
                text = sgm.read()
                sgm.close()
            except:
                lines = []
                for line in open(os.path.join(os.getcwd(), folder, file), 'rb').readlines():
                    line = line.decode('utf-8','ignore') 
                    lines.append(line)
                text = '\n'.join(lines)
            parsedText = BeautifulSoup(text.lower(), 'html.parser')
            for reuter in tqdm(parsedText.find_all('reuters')):
                if reuter.body and reuter.title:
                    data['body'].append(tokenize(reuter.body.get_text(strip=True)))
                    data['title'].append(tokenize(reuter.title.get_text(strip=True)))
    return data

def split_and_save(data):
    train, valid_test = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)
    valid, test = train_test_split(valid_test, test_size=0.5, random_state=42, shuffle=True)
    train.to_csv(os.path.join(os.getcwd(), 'data', 'reuters_train.csv'), index=False)
    valid.to_csv(os.path.join(os.getcwd(), 'data', 'reuters_valid.csv'), index=False)
    test.to_csv(os.path.join(os.getcwd(), 'data', 'reuters_test.csv'), index=False)