#!/usr/bin/env python
# coding: utf-8


import collections
import json
import multiprocessing
import os
import urllib.parse
import pandas as pd
from newspaper import Article
import requests
import re

class Processor():
    """
    This processor takes in json filepath (containing urls of articles) as input
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
        r = requests.get(url)

        # save to file
        with open('file.html', 'wb') as fh:
            fh.write(r.content)

        a = Article(url)

        # set html manually
        with open("file.html", 'rb') as fh:
            a.html = fh.read()

        # need to set download_state to 2 for this to work
        a.download_state = 2

        a.parse()
        
        title = a.title
        content = re.sub("\n\n"," ",a.text)
        # Now the article should be populated
        return content, title
    
    def process(self, filepath):
        """Main function of the Processor class"""
        print('Processing json and extracting urls...')
        urls = self._get_url_from_json(os.path.join(filepath))
        print('Done extracting urls - Begin extracting article content...')
        label = []
        text = []
        for url in urls:
            content, title = self._get_content_from_url(url)
            label.append(title)
            text.append(content)
        print('Done extracting article content...')
        df = {'url':urls, 'title':label, 'text':text}
        print('Outputing a dataframe...')
        return pd.DataFrame(data=df)

# Example of command to use this class and methods:
# df_test = Processor().process('folder_name/test.json')
