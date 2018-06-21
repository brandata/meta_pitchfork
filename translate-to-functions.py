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


def create_sql_db(db_name):
    print("Opening connection to database")
    con = sqlite3.connect(db_name)
    sql = con.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS music_data(
		album TEXT PRIMARY KEY,
		artist TEXT,
		meta_url TEXT,
		metascore NUMERIC,
		pf_url TEXT,
		user_score NUMERIC,
		review_author TEXT,
		pitchfork_genre TEXT,
	);""")

    return con, sql


def main():
    """Loop through all pages and parse their albums."""
    con = None  # initialize to None in case connection with db cannot be made
    try:
        con, sql = create_sql_db(DATABASE_NAME)  # con is connection to db, sql is cursor to interact with db
        for page in itertools.count(PAGE_NUMBER):
            page_to_pull = BASE_URL + str(page)
            html = get_site_new(page_to_pull)
            if not html:  # scrape_html fails to open BASE_URL + href because it does not exist (i.e., no more pages left)
                print("Done parsing")
                break
            if html:
                parse_meta_publications(sql, html)  # inserts ~20 albums into db
                con.commit()  # commit changes to db after page fully parsed
                time.sleep(
                    numpy.random.exponential(AVERAGE_SECONDS_BETWEEN_REQUESTS, 1))  # pause between server requests

    finally:  # close connection to db before exiting
        if con:
            print("Closing connection to database")
            con.close()

def parse_meta_publications(sql, html):
    review_wraps = BeautifulSoup(html, 'lxml').find_all('div', class_='review_wrap')

    for r in review_wraps:

        meta_url = "http://" + META_URL + r.find_all('a')[0].attrs['href']
        if not sql.execute("SELECT 1 FROM music_data WHERE id = ?;",
                           (meta_url,)).fetchone():  # if album does not exist in db

            # We pull four things from the initial review summary box - metascore, criticscore, pf_url, meta_url
            metascore = r.find_all('li', {'class': 'brief_metascore'})
            metascore = metascore[0].find_all('span', {'class': 'metascore_w'})[0].text
            criticscore = r.find_all('span', {'class': 'indiv'})[0].text
            pf_url = r.find_all('a', class_='external')[0].attrs['href']
            meta_url = "http://" + META_URL + r.find_all('a')[0].attrs['href']

            # Then we pull the necessary information from the metacritic review of that album.
            meta_html = get_site_new(meta_url)
            meta_soup = BeautifulSoup(meta_html, 'lxml')
            user_score = meta_soup.findAll('div', {'class': '.metascore_w.user.large'})
            meta_genre = meta_soup.findAll('li', {'class': 'summary_detail product_genre'})[0].text

            # This section is where we pull a couple necessary details from pitchfork - contributor(review author), genre, artist name, album name
            pitfrk_html = get_site_new(pf_url)
            pitfrk_soup = BeautifulSoup(pitfrk_html, 'lxml')
            pitfrk_contributor = pitfrk_soup.find_all('a', {'class': 'authors-detail__display-name'})[0].text
            pitfrk_genre = pitfrk_soup.find_all('a', {'class': 'genre-list__link'})[0].text
            pitfrk_artist = pitfrk_soup.find_all('ul', {'class': 'artist-links'})[0].text
            pitfrk_album = pitfrk_soup.find_all('h1', {'class': 'single-album-tombstone__review-title'})[0].text


            print(metascore, criticscore, pf_url, meta_url, user_score, meta_genre, pitfrk_contributor, pitfrk_genre, pitfrk_artist, pitfrk_album)

            # put the data that we've pulled into a list - insert that list into our database
            data = [metascore, criticscore, pf_url, meta_url, user_score, meta_genre, pitfrk_contributor, pitfrk_genre, pitfrk_artist, pitfrk_album]
            insert(sql, data)

            print(1)


def get_site_new(url):
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

    return html

def insert(sql, data):
    """Inserts the given data into the database."""
    sql.execute("INSERT OR IGNORE INTO music_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],))