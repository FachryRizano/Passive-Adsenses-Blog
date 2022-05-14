from tqdm import tqdm
import yake
import spacy
import nltk
import cloudscraper
from newspaper import Article
import re
import cloudscraper
import newspaper
import requests
from bs4 import BeautifulSoup

# Subtitle pertama jadi Main Title dan paragraph pertama sebagai introduction


# nltk.download('punkt')
# nlp = spacy.load("en_core_web_md")

def generate_image():
    pass

def get_article(url: str) -> tuple:
    try:
        # print(f"Getting {url}")
        scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
        responses = scraper.get(url)
        html = responses.content
        status = responses.status_code
        article = newspaper.Article(url=" ")
        article.set_html(html)
        article.parse()
        article.nlp()
        return ( status, article.title, nlp(article.text))
    except Exception as error:
        print(error)
        return ("Error","None",nlp("None"))

# SERP API
def search_links(keyword,api="8b72feb161cb7c785e7089b3c46a6367f0075f909e61c6939cdea47054dc28e9"):
  params = {
    "engine":"google",
    "q":keyword,
    "hl": "en",
    "num":"20",
    "start":"0",
    "api_key":api
  }
  responses = requests.get("https://serpapi.com/search.json",params=params)
  return responses.json()['organic_results']

def create_new_article(lst_kw,maximum_length=1500):
    corpus =""
    main_sample_link = []
    for i,kw in tqdm(enumerate(lst_kw)):
        if len(corpus) > maximum_length:
            print("Article is done")
            break
        params = {
            "lan":"en", 
            "n":1,
            "dedupLim":0.9,
            "dedupFunc":"seqm",
            "windowsSize":1, 
            "top":5, 
            "features":None
        }
        custom_kw_extractor = yake.KeywordExtractor(**params)
        serp = search_links(kw)
        lst_link = [ele['link'] for ele in serp]
        
        if i==0:
            main_sample_link = lst_link
        else:
            temp = set(list(main_sample_link) + lst_link)
            lst_link = temp.difference(main_sample_link)
            main_sample_link = temp
        # Get top article based on similarity with keyword
        # Find top head and article
        try:
            top_head, top_article =  sorted([get_article(link) for link in lst_link],key=lambda x: (nlp(kw).similarity(nlp(x[0])),nlp(kw).similarity(x[1])),reverse=True)[0]
            lst_paragraph = list(top_article.sents)[:5]
            top_paragraph = sorted([para for para in lst_paragraph],key=lambda para: nlp(top_head).similarity(para),reverse=True)[:5]
            lst_kw_keywords = custom_kw_extractor.extract_keywords(kw)
            lst_kw_keywords = set([kw[0] for kw in lst_kw_keywords])
            lst_kw_keywords = nlp(' '.join(lst_kw_keywords))
            lst_kw_keywords = set([token.lemma_ for token in lst_kw_keywords])
            print("Subtopic Keyword:", kw)
            add_title = False
            for i,p in enumerate(top_paragraph):
            # If meet question and not get data pass
                if p.text.endswith('?') or p.text.startswith("Try again") or p.text.startswith("Wait a moment") or p.text.startswith("Something went wrong"):
                    pass
                else:
                    if add_title is False:
                        corpus = corpus + "##" + kw + "\n"
                        add_title = True
                    keywords = custom_kw_extractor.extract_keywords(p.text)[:3]
                    keywords = set([kw[0] for kw in keywords])
                    keywords = nlp(' '.join(keywords))
                    keywords = set([token.lemma_ for token in keywords])
                    if len(lst_kw_keywords.intersection(keywords))>0:
                        # print(p.text)
                        # print(f"Extraction from sentences:{keywords}")
                        # Concatenate
                        corpus = corpus + p.text.replace("\n","") + "\n\n" 
                        print(f"Length article : {len(corpus)}")
        except Exception as e:
            print(e)
            pass
    return corpus

def filter_text(corpus,lst_kw):
  clean_duplicate = {text[:-1] for text in corpus.split("#")}.difference(lst_kw)
  return ''.join(["##" + sub + "\n" for sub in clean_duplicate if sub != ''])

def get_article_html(url):
    scraper = cloudscraper.create_scraper()
    html = scraper.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = soup.find_all("article")[0]
    except IndexError:
        res = f"{url} can't be scraped"
    return res
    

if __name__ == '__main__':
    # Sample
    # url = "https://www.indiatoday.in/education-today/jobs-and-careers/story/career-as-a-data-scientist-scope-skills-needed-job-profiles-and-other-details-1781529-2021-03-31"
    url = "https://towardsdatascience.com/is-data-science-still-a-rising-career-in-2021-722281f7074c"
    # scraper = cloudscraper.create_scraper()
    # html = scraper.get(url).content
    # print(html)
    print(get_article(url))
    # print(text_from_html(html))
    