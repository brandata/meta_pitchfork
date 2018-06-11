import requests
from bs4 import BeautifulSoup
import urllib.request  # html scraper
import urllib.error
import re
from bs4 import BeautifulSoup  # html parser. More info at http://www.crummy.com/software/BeautifulSoup/
import sys  # exit quits program prematurely in event of error
import sqlite3  # allows interaction with sql database (henceforth db)
import datetime  # strptime and strftime convert between date formats
import time  # sleep allows slight pause after each request to pitchfork's servers
import numpy  # random.exponential determines variable sleep time between server requests; more human-like, for what it's worth.
import itertools  # count function is convenient iterator
import \
    signal  # handles Timeout errors, in case scrape/parse takes too long. Only works on UNIX-based OS, sorry Windows users.

BASE_URL = "http://www.metacritic.com/publication/pitchfork?page=0"
OPENER = urllib.request.build_opener()
OPENER.addheaders = [
    ('User-agent', 'Mozilla/5.0')]  # perhaps disingenuous, but claims web scraper is a user-agent vs bot
AVERAGE_SECONDS_BETWEEN_REQUESTS = 5  # that being said, be kind to pitchfork's servers
START_AT_PAGE = 1  # album review page at which to begin scraping/parsing. Update this if program hangs and must be rerun.
DATABASE_NAME = 'meta-reviews.db'  # must end in .db
META_URL = "www.metacritic.com"


################################################
################################################

url = BASE_URL
#ADDING A COMMENT TO TEST


def get_site(url):
    html = None
    try:
        response = OPENER.open(url)
        if response.code == 200:
            print("Scraping %s" % url)
            html = response.read()
        else:
            print("Invalid URL: %s" % url)
    except urllib.request.HTTPError:
        print("Failed to open %s" % url)

    return BeautifulSoup(html, 'lxml')

#############################################
# Scrape main meta scritic page
main_soup = get_site(BASE_URL)

review_wraps = main_soup.find_all('div', class_='review_wrap')

for r in review_wraps:
    metascore = r.find_all('li', {'class': 'brief_metascore'})
    metascore = metascore[0].find_all('span', {'class': 'metascore_w'})[0].text

    criticscore = r.find_all('span', {'class': 'indiv'})[0].text

    pf_url = r.find_all('a', class_='external')[0].attrs['href']
    meta_url = META_URL + r.find_all('a')[0].attrs['href']
    print(metascore, criticscore, pf_url, meta_url)

################################################
################################################
pf_url = 'http://www.metacritic.com/music/listening-to-pictures-pentimento-volume-i/jon-hassell'
# Enter meta url and scrape
meta_soup = get_site(pf_url)
#meta_soup = meta_soup.find('div', {'id': 'main'})

#user_score = meta_soup.find_all('div', class_='module product_data product_data_summary')
#user_score = user_score[0].find_all('div', {'class': 'metascore_w user large album'})
user_score = meta_soup.findAll('div', {'class': '.metascore_w.user.large'})
#user_score = user_score[0].find_all('div', {'class': 'metascore_w user large'})


################################################
################################################
pit_url = 'https://pitchfork.com/reviews/albums/jon-hassell-listening-to-pictures-pentimento-volume-one/'

pitfrk_soup = get_site(pit_url)

# pitfrk genre
pitfrk_genre = pitfrk_soup.find_all('a', {'class': 'author-detail__display-name'})

#  Enter PF url and scrape
print(1)