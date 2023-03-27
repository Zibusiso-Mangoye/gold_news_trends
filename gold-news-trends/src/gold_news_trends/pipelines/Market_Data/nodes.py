def __get(url, params):
    import requests
    resp = requests.get(url=url, params=params)
    if resp.status_code != 200:
        raise Exception(f"Failed to download url {url}.")
    return resp.content

def get_news_data():
    params = {}
    for i in range(605):
        page_url = f"https://www.reuters.com/news/archive/goldMktRpt?page={i}"
        response = __get(page_url, params)
        
        # In response look for div class="news-headline-list  "
        # Then get all a tags in the list and create urls stored in a list
        # visit each url and get content
    article_links = []
    response = __get(url, params)
    
    # scrape an article and wait 10 sec before scraping next article
    # (10*10*604)
    
    # goto page
    # get list of article links 
    # visit each link and get article info 
    # Store article info in dict
    # export to csv
