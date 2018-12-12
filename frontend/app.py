from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
es = Elasticsearch(os.environ.get("ES_HOST"), port=os.environ.get("ES_PORT"))

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index="scrape-sysadmins", 
        size=20, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "title", 
                        "tags"
                    ] 
                }
            }
        }
    )
    return render_template('results.html', res=res )

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=os.environ.get("FRONTEND_PORT"))
