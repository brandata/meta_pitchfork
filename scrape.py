import requests
from bs4 import BeautifulSoup
import urllib2  # html scraper
from bs4 import BeautifulSoup  # html parser. More info at http://www.crummy.com/software/BeautifulSoup/
import sys  # exit quits program prematurely in event of error
import sqlite3  # allows interaction with sql database (henceforth db)
import datetime  # strptime and strftime convert between date formats
import time  # sleep allows slight pause after each request to pitchfork's servers
import numpy  # random.exponential determines variable sleep time between server requests; more human-like, for what it's worth.
import itertools  # count function is convenient iterator
import signal  # handles Timeout errors, in case scrape/parse takes too long. Only works on UNIX-based OS, sorry Windows users.


BASE_URL = 'https://pitchfork.com/reviews/albums/?page='
OPENER = urllib2.build_opener()
OPENER.addheaders = [('User-agent', 'Mozilla/5.0')]  # perhaps disingenuous, but claims web scraper is a user-agent vs bot

AVERAGE_SECONDS_BETWEEN_REQUESTS = 5  # that being said, be kind to pitchfork's servers
START_AT_PAGE = 1  # album review page at which to begin scraping/parsing. Update this if program hangs and must be rerun.
DATABASE_NAME = 'pitchfork-reviews2.db'  # must end in .db


URL = "https://pitchfork.com/reviews/albums/?page=1"

page = requests.get(URL)
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')


reviews = soup.find_all('div', class_="review")

for r in reviews:
    pub = r.find_all('time', class_="pub-date")[0].
    artist = r.find_all('ul', class_="artist-list review__title-artist")[0].text
    album = r.find_all('h2', class_="review__title-album")[0].text
    print artist, "--", album
    print "_______________"
    # album
    #

paragraphs = soup.find_all('p')
genres = soup.find_all("a", class_= "genre-list__link")

for g in genres:
    print g.text

print("------------------------")

for t in paragraphs:
    print t.text

