from newspaper import Article
import re
from bs4 import BeautifulSoup
import cloudscraper
import newspaper
import requests


def get_article(url: str) -> tuple:
    try:
        # print(f"Getting {url}")
        scraper = cloudscraper.create_scraper()
        html = scraper.get(url).content
        article = newspaper.Article(url=" ")
        article.set_html(html)
        article.parse()
        article.nlp()
        return ( article.title, nlp(article.text))
    except Exception as error:
        return ("None",nlp("None"))

def search_links(keyword):
  # SERP API
  params = {
    "engine":"google",
    "q":keyword,
    "hl": "en",
    "num":"20",
    "start":"0",
    "api_key":"8b72feb161cb7c785e7089b3c46a6367f0075f909e61c6939cdea47054dc28e9"
  }
  responses = requests.get("https://serpapi.com/search.json",params=params)
  return responses.json()['organic_results']



lst_kw = get_kw("data science jobs",20)

for kw in lst_kw:
  print(kw)

