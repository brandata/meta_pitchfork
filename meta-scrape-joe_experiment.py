import urllib.request  # html scraper
import urllib.error
from bs4 import BeautifulSoup  # html parser. More info at http://www.crummy.com/software/BeautifulSoup/
import sqlite3  # allows interaction with sql database (henceforth db)
import time
import numpy  # random.exponential determines variable sleep time between server requests; more human-like, for what it's worth.
import itertools  # count function is convenient iterator

BASE_URL = "http://www.metacritic.com/publication/pitchfork?page=" # adjusted
OPENER = urllib.request.build_opener()
OPENER.addheaders = [
    ('User-agent', 'Mozilla/5.0')]  # perhaps disingenuous, but claims web scraper is a user-agent vs bot
AVERAGE_SECONDS_BETWEEN_REQUESTS = 5  # that being said, be kind to pitchfork's servers
START_AT_PAGE = 1  # album review page at which to begin scraping/parsing. Update this if program hangs and must be rerun.
DATABASE_NAME = 'meta-reviews.db'  # must end in .db
META_URL = "www.metacritic.com"
PAGE_NUMBER = 0

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
# Scrape main meta critic page



# testing this up to page 5 to see if it will pull the first five pages
while PAGE_NUMBER < 5:

    page_to_pull = BASE_URL + str(PAGE_NUMBER)

    main_soup = get_site(page_to_pull)

    review_wraps = main_soup.find_all('div', class_='review_wrap')

    for r in review_wraps:

        # We pull four things from the initial review summary box - metascore, criticscore, pf_url, meta_url
        metascore = r.find_all('li', {'class': 'brief_metascore'})
        metascore = metascore[0].find_all('span', {'class': 'metascore_w'})[0].text
        criticscore = r.find_all('span', {'class': 'indiv'})[0].text
        pf_url = r.find_all('a', class_='external')[0].attrs['href']

        # needs an "http://" infront of it for it to be valid
        meta_url = "http://" + META_URL + r.find_all('a')[0].attrs['href']

        # Then we pull the necessary information from the metacritic review of that album.
        meta_soup = get_site(meta_url)
        user_score = meta_soup.find_all('div', {'class': 'metascore_w user'})
        meta_genre = meta_soup.findAll('li', {'class': 'summary_detail product_genre'})[0].text

        # This section is where we pull a couple necessary details from pitchfork - contributor(review author), genre, artist name, album name
        pitfrk_soup = get_site(pf_url)
        pitfrk_contributor = pitfrk_soup.find_all('a', {'class': 'authors-detail__display-name'})[0].text
        pitfrk_genre = pitfrk_soup.find_all('a', {'class': 'genre-list__link'})[0].text
        # artist
        pitfrk_soup.find_all('ul', {'class': 'artist-links'})[0].text
        # album name

        # At this point we should save the items to a database
        print(metascore, criticscore, pf_url, meta_url, pitfrk_contributor, pitfrk_genre)
        print(1)
        # time.sleep(numpy.random.exponential(AVERAGE_SECONDS_BETWEEN_REQUESTS, 1))

    PAGE_NUMBER += 1



