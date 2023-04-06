import requests
import random
import time
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
        print(f"Proxy {proxy} not working. Removing from list...")
        proxy_list.remove(proxy)
        proxy = random.choice(proxy_list)
        
def __get(url):
    
    # Define the proxies and headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    # get list from file 
    proxy_list = [
        "http://proxy1.example.com:1234",
        "http://proxy2.example.com:5678",
        "http://proxy3.example.com:9101"
    ]
    
    proxy = select_proxy(proxy_list)
    # Make the request using the selected proxy and headers
    proxies = {"http": proxy, "https": proxy}
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
    

def get_news_data():
    
    df = pd.DataFrame(columns=["article_date","article_time",
                               "article_title","article_link","article_body"])

    for i in range(605):
        page_url = f"https://www.reuters.com/news/archive/goldMktRpt?page={i}"
        response = __get(page_url)
        
        with open(response.content) as fp:
            articles_soup = BeautifulSoup(fp, 'lxml')
            articles =  articles_soup.find_all("article")
            
            for article in articles:
                article_link = article.find("a", href=True).attrs["href"].strip()
                df.loc[len(df)] = process_article(article_link)        
            
            df.to_csv("gold_articles.csv", mode="a", index=False, header=False)
            
            sleep_time = random.uniform(1, 5)
            print(f"Scraped {i} pages")
            print(f"Sleeping for {sleep_time:.2f} seconds before next request...")
            time.sleep(sleep_time)
            
    