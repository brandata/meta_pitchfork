import urllib.request  # html scraper
import urllib.error
from bs4 import BeautifulSoup  # html parser. More info at http://www.crummy.com/software/BeautifulSoup/
import sqlite3  # allows interaction with sql database (henceforth db)

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

# pulling the genre, though we will need to do some string manipulation to clean it up. will also need to decide how to
# store for multiple genres
meta_genre = meta_soup.findAll('li', {'class': 'summary_detail product_genre'})[0].text
print(meta_genre)

################################################
################################################
# This section is where we pull a couple necessary details from pitchfork
pit_url = 'https://pitchfork.com/reviews/albums/jon-hassell-listening-to-pictures-pentimento-volume-one/'

pitfrk_soup = get_site(pit_url)

# grabs the pitchfork contributor (author of the article)
pitfrk_contributor = pitfrk_soup.find_all('a', {'class': 'authors-detail__display-name'})[0].text
print(pitfrk_contributor)

# grabs the genre as reported by pitchfork
pitfrk_genre = pitfrk_soup.find_all('a', {'class': 'genre-list__link'})[0].text
print(pitfrk_genre)

print(1)