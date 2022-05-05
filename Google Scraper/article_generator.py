from tqdm import tqdm
import yake
import spacy
import nltk
import cloudscraper

nlp = spacy.load("en_core_web_md")
nltk.download('punkt')

def create_new_article(lst_kw):
    corpus =""
    main_sample_link = []
    for i,kw in tqdm(enumerate(lst_kw)):
    # if len(corpus) > 1000:
    #   print("Article is done")
    #   break

        language = "en"
        max_ngram_size = 1
        deduplication_thresold = 0.9
        deduplication_algo = 'seqm'
        windowSize = 1
        numOfKeywords = 5
        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
        
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
        # print(f"Link:{lst_link}")
        try:
            top_head, top_article =  sorted([get_article(link) for link in lst_link],key=lambda x: (nlp(kw).similarity(nlp(x[0])),nlp(kw).similarity(x[1])),reverse=True)[0]
            # print("Sort Article")
            # lst_paragraph = list(top_article.sents)[:len(top_article.sents)//2]
            lst_paragraph = list(top_article.sents)[:10]
            # lst_paragraph = top_article.split("\n\n")[:5]
            # print("Sort Paragraph")
            top_paragraph = sorted([para for para in lst_paragraph],key=lambda para: nlp(top_head).similarity(para),reverse=True)[:5]
            lst_kw_keywords = custom_kw_extractor.extract_keywords(kw)
            lst_kw_keywords = set([kw[0] for kw in lst_kw_keywords])
            lst_kw_keywords = nlp(' '.join(lst_kw_keywords))
            lst_kw_keywords = set([token.lemma_ for token in lst_kw_keywords])
            print("Main Keyword:", kw)
            print("Main Keyword Extraction: ",lst_kw_keywords)
            add_title = False
            for i,p in enumerate(top_paragraph):
                # If meet question and not get data pass
                if p.text.endswith('?') or p.text.startswith("Try again") or p.text.startswith("Wait a moment") or p.text.startswith("Something went wrong"):
                    pass
                else:
                    if add_title is False:
                        corpus = corpus + "##" + kw + "\n\n"
                        add_title = True
                        keywords = custom_kw_extractor.extract_keywords(p.text)[:3]
                        keywords = set([kw[0] for kw in keywords])
                        keywords = nlp(' '.join(keywords))
                        keywords = set([token.lemma_ for token in keywords])
                    if len(lst_kw_keywords.intersection(keywords))>0:
                        print(p.text)
                        print(f"Extraction from sentences:{keywords}")
                        print("\n\n")
                        # template = '^##.*?$'
                        # text = re.sub(template,'',p.text)
                        corpus = corpus + p.text.split("##")[0] + "\n" 
                        print(f"Length article : {len(corpus)}")
        except:
            pass
    return corpus

def filter():
# - Remove duplicate text. 
# - Remove 'For all other types of cookies, we need your permission. This site uses different types of cookies'
# - Remove only title
# - Propering article structure
# - Set limit word to 1500
    pass
if __name__ == '__main__':
    # Sample
    # https://www.indiatoday.in/education-today/jobs-and-careers/story/career-as-a-data-scientist-scope-skills-needed-job-profiles-and-other-details-1781529-2021-03-31
    url = "https://towardsdatascience.com/is-data-science-still-a-rising-career-in-2021-722281f7074c"
    scraper = cloudscraper.create_scraper()
    html = scraper.get(url).content
    print(html)