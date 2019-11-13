#!/usr/local/bin/python
# coding: latin-1
"""
add cleaned version of tweets + urls for tweets that couldn't be extended
i.e. shortened tweet-text -> split off url(s)

NOTE: The url collection I needed to scrape was really messy and contained either urls to tweets or urls to random websites with completely different structures. Make sure to adapt this code if you know the structure of the website you are trying to scrape and want specific information, e.g. just headlines from some online newspaper. You can always right-click 'inspect' (in Chrome) on elements of the website to try figuring out which HTML/CSS tags specify the chunk of text you want to retrieve.

"""

#imports-------------
import pickle
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen
import requests
import re
import csv


#functions to download text from url-----------

#for twt urls
def crawl_twitter_urls(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        tweet = soup.find('p',class_='tweet-text').text
        return tweet
    except:
        return ''

#for other urls
def crawl_other_urls(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        title = ''
        headline = soup.find_all('h1')
        for element in headline:
            line = element.extract().get_text().replace('\n',' ').strip() + ' '
            if not(('403' in line) or ('404' in line)) :
                title = title + line
        return title

    except:
        return ''



#get urls
path_urls = 'urls.pickle'
with open(path_urls,'rb') as fin:
    url_list = pickle.load(fin)

#open result file & start scraping + write to file
path_results = 'results.txt'
with open(path_results,'a')as fout:

    url_text = {}
    #split into twitter & not twitter urls:
    for url in url_list:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        text = ''
        try:
            html = urlopen(req).geturl()
            if re.match('^https://twitter.com/',html):
                text = crawl_twitter_urls(html)
            else:
                text = crawl_other_urls(html)
        except:
            if not(re.match('^https://twitter.com/',url)) and not(re.match('^https://t.co/',url)):
                text = crawl_other_urls(url)

        cleantext = ' '.join([item for item in text.split('pic.twit') if not('ter.com/' in item)])
        cleantext = ' '.join([item for item in cleantext.split('http') if not('://' in item)])
        cleantext = cleantext.replace('\n',' ')
        print(cleantext)
        url_text[url]=cleantext


        fout.write(url.encode('utf-8'))
        fout.write('\t')
        fout.write(cleantext.encode('utf-8'))
        fout.write('\n')


#i double saved it with pickle, so:
path_pickle_results = 'results.pickle'
with open(path_pickle_results,'wb')as fout:
    pickle.dump(url_text,fout,protocol=pickle.HIGHEST_PROTOCOL)
