import itertools
import random as r

import requests
from bs4 import BeautifulSoup

# quote sources-
# https://www.keepinspiring.me/100-most-inspirational-sports-quotes-of-all-time/
# https://www.keepinspiring.me/harry-potter-quotes/


URL1 = "https://www.keepinspiring.me/100-most-inspirational-sports-quotes-of-all-time/"
URL2 = "https://www.keepinspiring.me/harry-potter-quotes/"

QUOTE_LIST = []

file = open('quotes.txt', 'r')
QUOTE_LIST.extend(file.readlines())
file.close()


def get_inspiration():
    """Return list of quotes"""

    quotelist = []
    page1 = requests.get(URL1)
    soup1 = BeautifulSoup(page1.content, 'html.parser')

    page2 = requests.get(URL2)
    soup2 = BeautifulSoup(page2.content, 'html.parser')

    result1 = soup1.find_all("div", class_="author-quotes")
    result2 = soup2.find_all("div", class_="author-quotes")

    quotelist.extend([quote.text for quote in result1[-2::-1]])  # Ignore the last quote because it contains a message from the post author
    quotelist.extend([quote.text for quote in result2])

    return quotelist


def get_quote():
    """Get a random quote"""

    return next(QUOTES)


get_inspiration()
r.shuffle(QUOTE_LIST)
QUOTES = itertools.cycle(QUOTE_LIST)
