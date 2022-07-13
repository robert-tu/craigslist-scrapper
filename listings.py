# loop listings
from time import sleep
from random import randint
from warnings import warn
from time import time
import math
from IPython.display import clear_output, display
import numpy as np

from cgitb import html
from requests import get
# get first page of car listings
response = get('https://sfbay.craigslist.org/search/cta?purveyor=owner&min_price=&max_price=30000&condition=10&condition=20&condition=30&condition=40&auto_title_status=1')

from bs4 import BeautifulSoup

html_soup = BeautifulSoup(response.text, 'html.parser')

# find total posts
results_total = int(html_soup.find('span', class_ = 'totalcount').text)
results_top = int(results_total / 15)
print("today's total listings: " + str(results_top))

def get_listings():
    # loop through available listings
    pages = np.arange(0, results_top + 1, 120)

    i = 0
    total_pages = math.ceil(int(results_top / 120))

    # arrays to hold listings
    post_times = []
    post_hoods = []
    post_titles= []
    post_prices = []
    post_urls = []

    for page in pages:
        response = get("https://sfbay.craigslist.org/search/cta?"
                        + "s=" # parameter for page number
                        + str(page) # page number in array
                        + "purveyor=owner"  # by owners
                        + "&min_price=&max_price=30000" # < $30,000
                        + "&condition=10&condition=20&condition=30&condition=40" # new, like new, excellent, good
                        + "&auto_title_status=1") # clean titles
        sleep(randint(1, 5))

        # warning if not 200
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
        
        # define html
        page = BeautifulSoup(response.text, 'html.parser')

        # define posts
        posts = html_soup.find_all('li', class_ = 'result-row')

        # extract data
        for post in posts:
            if post.find('span', class_ = 'result-hood') is not None:
                # date
                post_datetime = post.find('time', class_ = 'result-date')['datetime']
                post_times.append(post_datetime)
                # neighborhood
                post_hood = post.find('span', class_ = 'result-hood').text
                post_hoods.append(post_hood)
                # title
                post_title = post.find('a', class_ = 'result-title hdrlnk')
                post_title_text = post_title.text
                post_titles.append(post_title_text)
                # price
                post_price = post.a.text.strip().replace("$", "")
                post_prices.append(post_price)
                # url
                post_url = post_title['href']
                post_urls.append(post_url)
        i += 1
        print("Page " + str(i) + "/" + str(total_pages) + " scraped successfully")

    print("Scrape complete\n")

    # dataframe for listings
    import pandas as pd

    listing_dict = {'posted': post_times,
                    'neighborhood': post_hoods,
                    'title': post_titles,
                    'price': post_prices,
                    'url': post_urls}

    sf_bay_cars = pd.DataFrame(listing_dict)
    # set dataframe to display full column
    pd.set_option('display.max_colwidth', None)

    return sf_bay_cars