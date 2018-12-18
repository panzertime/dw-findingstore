from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from datetime import datetime
import os

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
    # take the form and send it to elastic
    document={}
    document["url"] = request.form["inputUrl"]
    document["forumname"] = request.form["inputMarket"]
    document["vendorname"] = request.form["inputVendor"]
    document["category"] = request.form["inputCategory"]
    document["keywords"] = request.form["inputKeywords"].split(', ')
    document["summary"] = request.form["inputSummary"]
    document["created"] = datetime.now()

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

@app.route('/card/import')
def import_card():
    # unzip the card and add to ES
    pass

@app.route('/card/export')
def export_card():
    # zip the card and return it to user
    pass

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=os.environ.get("FRONTEND_PORT"))
