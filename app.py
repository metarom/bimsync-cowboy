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


        url = "https://binsyncfunction.azurewebsites.net/api/manager/users/9670ecae-aaff-44dc-960c-6e03abea8a79"

        binsync_response = requests.request("GET", url)

        bearer_token = binsync_response.json()["AccessToken"]["access_token"]

        url2 = f"https://opencde.bimsync.com/bcf/{version_id}/projects/{project_id_issueboard}/topics?$top=500&$select=title,description,index,labels,due_date,stage,creation_author,creation_date,modified_date,modified_author,assigned_to,topic_status,topic_type,topic_priority,bim_snippet,bimsync_requester"

        payload={}
        headers = {
        'Authorization': 'Bearer ' + bearer_token
        }

        response = requests.request("GET", url2, headers=headers, data=payload)
                
        with Path("BCF_VTM_Issueboard_Prosjektering.json").open("w", encoding="UTF-8") as json_file: 
            json.dump(response.json(), json_file)
                               

    file = "BCF_VTM_Issueboard_Prosjektering.json"
    return send_file(file,as_attachment=True)


if __name__ == '__main__':
   app.run(debug=True, threaded=True, use_reloader=False)
   
