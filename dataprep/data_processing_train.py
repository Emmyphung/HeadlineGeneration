#!/usr/bin/env python
# coding: utf-8

import sys
import os
import collections
import json
import multiprocessing
import os
import urllib.parse
import pandas as pd
from newspaper import Article
import requests
import re

from tqdm import tqdm
import nltk
import string
nltk.download('punkt')

class Processor():
    """
    This processor takes in json filepath as input
    and return a dataframe with url, title, main tex of articles.  
    """
    def _get_url_from_json(self, file_path):
        """Takes in json file_path and return a list of urls"""
        urls = []
        with open(file_path, "r") as article_json_file:
            article = json.load(article_json_file)
        #print(len(article))
        for art in article:
            #print(len(art['urls']))
            for url in art['urls']:
                urls.append(url)
        return urls
    
    def _get_content_from_url(self, url):
        """Takes in a single url and return article content and title"""
        #r = requests.get(url)

        try:
            r = requests.get(url,timeout=6)
            # print('successful!')
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry
            print(e)
            return ' ', ' '
        except requests.exceptions.RequestException as e:
            print(e)
            return ' ', ' '

        # save to file
        with open('file.html', 'wb') as fh:
            fh.write(r.content)
        #print('Running Article...')
        a = Article(url)

        # set html manually
        with open("file.html", 'rb') as fh:
            a.html = fh.read()
        #print('Done opening Article.html...')
        # need to set download_state to 2 for this to work
        a.download_state = 2

        a.parse()
        
        title = a.title
        content = re.sub("\n\n"," ",a.text)
        # Now the article should be populated
        return content, title

    def tokenize(self, text):
        """ function: tokenize
          ------------------
          generate list of tokens given a block of @text;
          :param text: string representing text field (title or body)
          :returns: list of strings of tokenized & sanitized words
        """
        # remove punctuation
        no_punctuation = text.translate(str.maketrans('','',string.punctuation))
        # tokenize
        tokens = nltk.word_tokenize(no_punctuation)
        return tokens
    
    def process(self, filepath,start,end):
        """Main function of the Processor class"""
        print('Processing json and extracting urls...')
        urls = self._get_url_from_json(os.path.join(filepath))
        print('Done extracting urls - Begin extracting article content...')
        print('There are {} urls...'.format(len(urls)))
        label = []
        text = []
	if type(start)== int:
	    # start = int(start)
	    urls = urls[start:]
	elif type(end)== int:
	    urls = urls[:end]
        
        print('Will process {} urls in this run...'.format(len(urls)))
        for url in tqdm(urls):
            content, title = self._get_content_from_url(url)
            content, title = self.tokenize(content), self.tokenize(title)
            label.append(title)
            text.append(content)

        print('Done extracting article content...')
        df = {'url':urls, 'title':label, 'text':text}
        print('Outputing a dataframe...')
        return pd.DataFrame(df)

# Example of command to use this class and methods:
# df_test = Processor().process('folder_name/test.json')
