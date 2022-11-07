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

project_id_issueboard_2 = "fbc59d26-2625-41a3-b992-68a08ec4c233" #Issueboard VTM_Tverrfaglig

project_id = "b2eb276ae9b34f76a7e64bed0491d8e8" #VTM2

version_id = 2.1

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('print-issues.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# This is where the magic happens

@app.route('/download', methods=['GET', 'POST'])
def download():

    if request.method == 'POST':

# Get fresh access token

        url = "https://binsyncfunction.azurewebsites.net/api/manager/users/9670ecae-aaff-44dc-960c-6e03abea8a79"

        binsync_response = requests.request("GET", url)

        bearer_token = binsync_response.json()["AccessToken"]["access_token"]

# Get topics from VTM_Prosjektering

        url2 = f"https://opencde.bimsync.com/bcf/{version_id}/projects/{project_id_issueboard}/topics?$top=500&$select=title,description,index,labels,due_date,stage,creation_author,creation_date,modified_date,modified_author,assigned_to,topic_status,topic_type,topic_priority,bim_snippet,bimsync_requester"

        payload={}
        headers = {
        'Authorization': 'Bearer ' + bearer_token
        }

        response_prosjektering = requests.request("GET", url2, headers=headers, data=payload)
                
        with Path("BCF_VTM_Issueboard_Prosjektering_dedicated.json").open("w", encoding="UTF-8") as json_file: 
            json.dump(response_prosjektering.json(), json_file)
        
# Get topics from VTM_Tverrfaglig

        url3 = f"https://opencde.bimsync.com/bcf/{version_id}/projects/{project_id_issueboard_2}/topics?$top=500&$select=title,description,index,labels,due_date,stage,creation_author,creation_date,modified_date,modified_author,assigned_to,topic_status,topic_type,topic_priority,bim_snippet,bimsync_requester"

        payload={}
        headers = {
        'Authorization': 'Bearer ' + bearer_token
        }

        response_tverrfaglig = requests.request("GET", url3, headers=headers, data=payload)
                
        with Path("BCF_VTM_Issueboard_Tverrfaglig.json").open("w", encoding="UTF-8") as json_file: 
            json.dump(response_tverrfaglig.json(), json_file)

        
# Join the two json files into one

        f1data = f2data = "" 
 
        with open('BCF_VTM_Issueboard_Prosjektering_dedicated.json') as f1: 
            f1data = f1.read() 
        with open('BCF_VTM_Issueboard_Tverrfaglig.json') as f2: 
            f2data = f2.read() 
        
        f1data += "\n"
        f1data += f2data

        with open ('BCF_VTM_Issueboard_Prosjektering.json', 'a') as f3: 
            f3.write(f1data)

# Return file to user
        
    file = "BCF_VTM_Issueboard_Prosjektering.json"
    return send_file(file,as_attachment=True)

# Start the app

if __name__ == '__main__':
   app.run(debug=True, threaded=True, use_reloader=False)
   
   
