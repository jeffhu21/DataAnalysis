import json
import time
import webbrowser
from datetime import datetime
from urllib.parse import urlencode

import dotenv
from dotenv import load_dotenv

import os
import requests
from requests.exceptions import HTTPError
#import MyServer


url = 'https://api.discogs.com/'

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
#load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
CALLBACK = os.getenv("CALLBACK")
#SIGNATURE_METHOD = os.getenv("SIGNATURE_METHOD")

def request_token():
    request_token_endpoint = url+"oauth/request_token"
    authorize_endpoint = "https://discogs.com/oauth/authorize?oauth_token="
    access_token_endpoint = url+"oauth/access_token"
    # Step 1: Get request token
    header = {'Content_Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json',
              'Accept-Encoding': 'gzip, deflate',
              'User_Agent': 'linnworksDiscogs/0.1 +https://www.example.com'}
    request_token_param = {"oauth_consumer_key": CONSUMER_KEY, "oauth_callback": CALLBACK, "oauth_signature_method": "PLAINTEXT",
            "oauth_nonce": "discogs_"+datetime.now().strftime("%Y%m%d%H%M%S"), "oauth_signature": CONSUMER_SECRET+"&",
            "oauth_timestamp": datetime.now().strftime("%Y%m%d%H%M%S")}
    try:
        request_token_response = requests.get(request_token_endpoint, headers=header, params=request_token_param, stream=True)
        request_token_response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    data=request_token_response.text.split("&")
    oauth_token=data[0].split("=")[1]
    oauth_token_secret=data[1].split("=")[1]
    print(f"Oauth Token = {oauth_token} & Oauth Token Secret = {oauth_token_secret}")

    #Step 2: Authorize
    authorize_response = webbrowser.open(authorize_endpoint+oauth_token)
    #print(authorize_response)
    """
    try:
        callback_response = requests.get(CALLBACK, stream=True)
        callback_response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    #print(callback_response.url)
    """


    """
    try:
        authorize_response = requests.get(authorize_endpoint+oauth_token, headers=header, params=param, stream=True)
        authorize_response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    """
    # Step 3: Get access token
    print("Enter oauth verifier:")
    oauth_verifier = input()
    #print("Oauth Verifier: " + oauth_verifier)
    os.environ["OAUTH_VERIFIER"] = oauth_verifier
    dotenv.set_key(dotenv_file, "OAUTH_VERIFIER", os.environ["OAUTH_VERIFIER"])
    access_token_param = {"oauth_consumer_key": CONSUMER_KEY, "oauth_verifier": oauth_verifier,
                           "oauth_signature_method": "PLAINTEXT",
                           "oauth_nonce": "discogs_" + datetime.now().strftime("%Y%m%d%H%M%S"),
                           "oauth_signature": CONSUMER_SECRET + "&" + oauth_token_secret,
                           "oauth_timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
                           "oauth_token": oauth_token
                           #"oauth_token_secret": oauth_token_secret
                            }
    try:
        access_token_response = requests.post(access_token_endpoint, headers=header, params=access_token_param, stream=True)
        access_token_response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return access_token_response.text

def save_token(token):
    data = token.split("&")
    oauth_token = data[0].split("=")[1]
    oauth_token_secret = data[1].split("=")[1]
    os.environ["OAUTH_TOKEN"] = oauth_token
    os.environ["OAUTH_TOKEN_SECRET"] = oauth_token_secret
    dotenv.set_key(dotenv_file,"OAUTH_TOKEN",os.environ["OAUTH_TOKEN"])
    dotenv.set_key(dotenv_file, "OAUTH_TOKEN_SECRET", os.environ["OAUTH_TOKEN_SECRET"])


"""
if __name__ == "__main__":
    access_token = request_token()
"""

access_token = request_token()
#print(access_token)
save_token(access_token)


