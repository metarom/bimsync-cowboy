import os
import requests
import json
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response, send_file, jsonify
from pathlib import Path

app = Flask(__name__)

project_id_issueboard = "0c2f0638-45fd-4fe7-bca9-3dfadfabc902" #Issueboard VTM_Prosjektering

project_id = "b2eb276ae9b34f76a7e64bed0491d8e8" #VTM2

version_id = 2.1

authorization_code = 0


def GetAuthorized():	
	auth_url = 'https://api.bimsync.com/oauth2/authorize?response_type=code&prompt=none&client_id=4mqUB2ciGTlCSPd&redirect_uri=http://127.0.0.1'
	print(auth_url) 
	print(webbrowser.open(auth_url))


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/authenticate', methods=['POST'])
def authorize():
    if request.method == 'POST':
        if request.form['button'] == 'authenticate':
            GetAuthorized()
            return render_template('paste-code.html')


@app.route('/bimsync-retriever', methods=['POST'])
def bimsync_retriever():

   code = request.form.get('code', None)

   if request.method == 'POST':
        if request.form['button_man'] == 'update':
            if code:
                
                url = f"https://api.bimsync.com/oauth2/token?grant_type=authorization_code&code={code}&client_id=4mqUB2ciGTlCSPd&client_secret=9DgfCIF68tr3DIm&redirect_uri=http://127.0.0.1"

                payload={}
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                access_token = response.json()["access_token"]

                url = f"https://opencde.bimsync.com/bcf/{version_id}/projects/{project_id_issueboard}/topics?$top=500&$select=title,description,index,labels,due_date,stage,creation_author,creation_date,modified_date,modified_author,assigned_to,topic_status,topic_type,topic_priority,bim_snippet,bimsync_requester"

                payload={}
                headers = {
                'Authorization': 'Bearer ' + access_token
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                
                with Path("BCF_VTM_Issueboard_Prosjektering.json").open("w", encoding="UTF-8") as json_file: 
                    json.dump(response.json(), json_file)
                               
                print('Request for hello page received with name=%s' % code)
                return render_template('print-issues.html', code = code)

            elif code=="":
                return render_template('print-issues.html', code = "blank, try again")

            else:
                return render_template('print-issues.html')

#Downloads file

@app.route('/download', methods=['GET', 'POST'])
def download():
    file = "BCF_VTM_Issueboard_Prosjektering.json"
    return send_file(file,as_attachment=True)


if __name__ == '__main__':
   app.run(debug=True)