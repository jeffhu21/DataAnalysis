import os
import requests, json
from dotenv import load_dotenv
from requests import HTTPError
from requests_oauthlib import OAuth1

url = 'https://api.discogs.com/'

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
CALLBACK = os.getenv("CALLBACK")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.getenv("OAUTH_TOKEN_SECRET")
OAUTH_VERIFIER = os.getenv("OAUTH_VERIFIER")

def get_data():
    resultsList=[]
    pageNo=1
    hasMorePages=True
    endpoint = url+"database/search"
    header = {'Content_Type': 'application/json',
              'Accept': 'application/json',
              'Accept-Encoding': 'gzip, deflate'
             }
    auth = OAuth1(CONSUMER_KEY,CONSUMER_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
    while (pageNo<6):
        param = {"type":"release","per_page":100,"page":pageNo}
        try:
            res = requests.get(endpoint, headers=header, auth=auth, params=param)
            res.raise_for_status()
            resultsList.extend(res.json()['results'])
            pages=res.json()["pagination"]["pages"]
            if pageNo<pages:
                pageNo+=1
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        #print(res.json())
    return resultsList


