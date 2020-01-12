import requests
from bs4 import BeautifulSoup

URL = 'https://www.reddit.com/r/PewdiepieSubmissions/top/?t=day'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
