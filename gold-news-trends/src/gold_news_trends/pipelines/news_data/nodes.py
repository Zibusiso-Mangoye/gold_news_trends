import requests
import random
import time
import logging
import pandas as pd
from bs4 import BeautifulSoup

def test_proxy(proxy):
    try:
        response = requests.get("https://www.reuters.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

def select_proxy(proxy_list):
    # Randomly select a proxy from the list and test it
    proxy = random.choice(proxy_list)
    while not test_proxy(proxy):
        logging.INFO(f"Proxy {proxy} not working. Removing from list...")
        proxy_list.remove(proxy)
        proxy = random.choice(proxy_list)
        
def __get(url):
    # define proxy_list in parameters and access them via kedro
    # same for headers 
    resp = requests.get(url=url, headers=headers, proxies=proxies)
    if resp.status_code != 200:
        raise Exception(f"Failed to download url {url}.")
    return resp

def process_article(article_link):
    response = __get(article_link)
    with open(response.content) as fs:
        article_soup = BeautifulSoup(fs, 'lxml')
         
        article_title = article_soup.find("h1").text.strip()
        date = article_soup.find("time").text
        time = article_soup.find("time").next_sibling.text
        body = article_soup.find("pre").text
        
        return [date,time,article_title,article_link,body]

def sentiment_analysis(article):
    # send article to third party
    article_body = article['article_body']
    pass

def get_news_data(proxy_list):
    
    df = pd.DataFrame(columns=["article_date","article_time",
                               "article_title","article_link","article_body"])

    for i in range(605):
        page_url = f"https://www.reuters.com/news/archive/goldMktRpt?page={i}"
        
        # Define the proxies and headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    
        proxy = select_proxy(proxy_list)
        proxies = {"http": proxy, "https": proxy}
        response = __get(page_url, proxy, header)
        
        with open(response.content) as fp:
            articles_soup = BeautifulSoup(fp, 'lxml')
            articles =  articles_soup.find_all("article")
            
            for article in articles:
                article_link = article.find("a", href=True).attrs["href"].strip()
                df.loc[len(df)] = process_article(article_link)        
                        
            sleep_time = random.uniform(1, 5)
            logging.info(f"Scraped {i} pages")
            logging.info(f"Sleeping for {sleep_time:.2f} seconds before next request...")
            time.sleep(sleep_time)
    
    df["sentiment_score"] = df['article_body'].apply(sentiment_analysis)

    return df