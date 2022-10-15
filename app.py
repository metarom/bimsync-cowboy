import os
import time
import json
import webbrowser
from pathlib import Path
from datetime import datetime
from _thread import start_new_thread

import requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response, send_file, jsonify

app = Flask(__name__)

project_id_issueboard = "0c2f0638-45fd-4fe7-bca9-3dfadfabc902" #Issueboard VTM_Prosjektering

project_id = "b2eb276ae9b34f76a7e64bed0491d8e8" #VTM2

version_id = 2.1

def oven():

  refresh_token = "KcIkW7VI4skwyaxOISUcOF" #if app stops change this to a fresh token

  #x = 1

  #while x == 1:

  while True:

    print('Tick! The time is: %s' % datetime.now())

    url = f"https://api.bimsync.com/oauth2/token?grant_type=refresh_token&refresh_token={refresh_token}&client_id=4mqUB2ciGTlCSPd&client_secret=9DgfCIF68tr3DIm&redirect_uri=http://127.0.0.1"

    payload={}
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    fresh_tokens = requests.request("POST", url, headers=headers, data=payload)

    print(fresh_tokens.json())

    with Path("tokens.json").open("w", encoding="UTF-8") as tokens_json_file: 
         json.dump(fresh_tokens.json(), tokens_json_file)

    #x = 2

    with open('tokens.json') as f:
        refresh_token = json.load(f)["refresh_token"]

    #time.sleep(3300)
    time.sleep(4)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('print-issues.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


#Downloads file

@app.route('/download', methods=['GET', 'POST'])
def download():

    if request.method == 'POST':
    
        with open('tokens.json') as f:
                bearer = json.load(f)["access_token"]

                url = f"https://opencde.bimsync.com/bcf/{version_id}/projects/{project_id_issueboard}/topics?$top=500&$select=title,description,index,labels,due_date,stage,creation_author,creation_date,modified_date,modified_author,assigned_to,topic_status,topic_type,topic_priority,bim_snippet,bimsync_requester"

                payload={}
                headers = {
                'Authorization': 'Bearer ' + bearer
                }

                response = requests.request("GET", url, headers=headers, data=payload)
                
                with Path("BCF_VTM_Issueboard_Prosjektering.json").open("w", encoding="UTF-8") as json_file: 
                    json.dump(response.json(), json_file)
                               

    file = "BCF_VTM_Issueboard_Prosjektering.json"
    return send_file(file,as_attachment=True)


if __name__ == '__main__':
   start_new_thread(oven, ())
   app.run(debug=True, threaded=True, use_reloader=False)
   