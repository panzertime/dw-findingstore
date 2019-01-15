# Copyright 2019 The Home Depot, Inc.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from flask import Flask, render_template, request, send_file
from elasticsearch import Elasticsearch
from datetime import datetime
import os
import base64
from zipfile import ZipFile
from io import BytesIO
from yaml import load, dump

app = Flask(__name__)
es = Elasticsearch(os.environ.get("ES_HOST"), port=os.environ.get("ES_PORT"))

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create/submit', methods=['POST'])
def create_submit():
    document={}
    document["url"] = request.form["inputUrl"]
    document["forumname"] = request.form["inputMarket"]
    document["vendorname"] = request.form["inputVendor"]
    document["category"] = request.form["inputCategory"]
    document["keywords"] = request.form["inputKeywords"].split(', ')
    document["summary"] = request.form["inputSummary"]
    document["created"] = datetime.now()
    document["text_evidences"] = []
    document["binary_evidences"] = []

    for filename in request.files:
        source = request.files[filename]
        dest = {}
        dest["filename"] = source.filename
        if source.mimetype.startswith('text'):
            # explicitly use Unicode, otherwise you end up with unparseable bytes
            dest["file"] = source.read().decode("utf-8")
            document["text_evidences"].append(dest)
        else:
            # read bytes, then Base64 encode, then transform the bytestring into a normal string
            dest["file"] = base64.b64encode(source.read()).decode()
            document["binary_evidences"].append(dest)

    es.index(index="findingstore_index", doc_type="finding_card", body=document)
    return render_template('create.html')

@app.route('/import')
def import_finding():
    return render_template('import.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index="findingstore_index", 
        size=20, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "forumname", 
                        "vendorname",
                        "category",
                        "keywords",
                        "summary"
                    ] 
                }
            }
        }
    )
    return render_template('results.html', res=res )

@app.route('/card/display')
def display_card():
    card_id = request.args.get("card_id")
    res = es.get(index="findingstore_index", doc_type="_all", id=card_id)
    return render_template('rendered_card.html', res=res)

@app.route('/card/import', methods=['POST'])
def import_card():
    document = {}
    for filename in request.files:
        with ZipFile(request.files[filename], mode='r') as archive:
            with archive.open('manifest.yml') as manifest:
                mani = load(manifest)
                document["url"] = mani["url"]
                document["forumname"] = mani["forumname"]
                document["vendorname"] = mani["vendorname"]
                document["category"] = mani["category"]
                document["keywords"] = mani["keywords"]
                document["summary"] = mani["summary"]
                document["created"] = datetime.now()
                document["text_evidences"] = []
                document["binary_evidences"] = []
                for evidence in mani["evidences"]:
                    to_add = {}
                    to_add["filename"] = evidence["fileName"]
                    with archive.open(evidence["fileName"]) as ev:
                        if evidence["isBinary"]:
                            to_add["file"] = base64.b64encode(ev.read()).decode()
                            document["binary_evidences"].append(to_add)
                        else:
                            to_add["file"] = ev.read().decode("utf-8")
                            document["text_evidences"].append(to_add)
    es.index(index="findingstore_index", doc_type="finding_card", body=document)
    return render_template('import.html')

@app.route('/card/export')
def export_card():
    card_id = request.args.get("card_id")
    res = es.get(index="findingstore_index", doc_type="_all", id=card_id)["_source"]
    file = BytesIO()
    with ZipFile(file, mode='a') as archive:
        mani = {}
        mani["url"] = res["url"]
        mani["forumname"] = res["forumname"]
        mani["vendorname"] = res["vendorname"]
        mani["category"] = res["category"]
        mani["keywords"] = res["keywords"]
        mani["summary"] = res["summary"]
        mani["evidences"] = []
        for binary in res["binary_evidences"]:
            mani["evidences"].append({"isBinary": True, "fileName": binary["filename"]})
        for text in res["text_evidences"]:
            mani["evidences"].append({"isBinary": False, "fileName": text["filename"]})
        archive.writestr("manifest.yml", dump(mani, default_flow_style=False))
        for evidence in res["binary_evidences"]:
            archive.writestr(evidence["filename"], base64.b64decode(evidence["file"]))
        for evidence in res["text_evidences"]:
            archive.writestr(evidence["filename"], evidence["file"])
    file.seek(0)
    return send_file(file, mimetype='application/zip', as_attachment=True, attachment_filename='card.zip')

@app.route('/artifact/download_text')
def download_text():
    card_id = request.args.get("card_id")
    file_number = int(request.args.get("file_num"))
    res = es.get(index="findingstore_index", doc_type="_all", id=card_id, _source_include="text_evidences")["_source"]["text_evidences"][file_number]
    file = BytesIO(bytes(res["file"], "utf-8"))
    return send_file(file, as_attachment=True, attachment_filename=res["filename"])

@app.route('/artifact/download_binary')
def download_binary():
    card_id = request.args.get("card_id")
    file_number = int(request.args.get("file_num"))
    res = es.get(index="findingstore_index", doc_type="_all", id=card_id, _source_include="binary_evidences")["_source"]["binary_evidences"][file_number]
    file = BytesIO(base64.b64decode(res["file"]))
    return send_file(file, as_attachment=True, attachment_filename=res["filename"])

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=os.environ.get("FRONTEND_PORT"))
