def get_market_data(url, params):
    import requests
    resp = requests.get(url=url, params=params)
    if resp.status_code != 200:
        raise Exception(f"Failed to download url {url}.")
    return resp.content["values"]

def process_market_data(df):
    pass