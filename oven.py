import os
import time
import json
import webbrowser
from pathlib import Path
from datetime import datetime

import requests

def fresh_token():

  access_token = "0tOiiQJ3poGSs2FwmfoSJo"

  refresh_token = "WHxT8pxqE1iIHPJD4xnA18"

  while True:

    print('Tick! The time is: %s' % datetime.now())

    url = f"https://api.bimsync.com/oauth2/token?grant_type=refresh_token&refresh_token={refresh_token}&client_id=4mqUB2ciGTlCSPd&client_secret=9DgfCIF68tr3DIm&redirect_uri=http://127.0.0.1"

    payload={}
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    fresh_access_token = response.json()["access_token"]
    fresh_refresh_token = response.json()["refresh_token"]

    access_token = fresh_access_token
    refresh_token = fresh_refresh_token

    print("access token:" + access_token)
    print("refresh token:" + refresh_token)

    fresh_token.baked_token = access_token

    #print(fresh_token.baked_token)

    with Path("fresh_baked_access_token.json").open("w", encoding="UTF-8") as json_file: 
        json.dump(response.json()["access_token"], json_file)

    # with Path("fresh_baked_refresh_token.json").open("w", encoding="UTF-8") as refresh_token_json_file: 
    #     json.dump(fresh_refresh_token.json(), refresh_token_json_file)
    
    #time.sleep(3300)
    time.sleep(10)

fresh_token()