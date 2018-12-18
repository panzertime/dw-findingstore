#!/bin/bash

# set variables
export ELASTIC_HOST="localhost"
export ELASTIC_PORT="9200"

curl -X PUT "$ELASTIC_HOST:$ELASTIC_PORT/findingstore_index" -H 'Content-Type: application/json' -d'
{
    "mappings": {
        "finding_card": {
            "properties": {
                "url": {
                    "type": "text"
                },
                "forumname": {
                    "type": "text"
                },
                "vendorname": {
                    "type": "text"
                },
                "category": {
                    "type": "text"
                },
                "keywords": {
                    "type": "keyword"
                },
                "summary": {
                    "type": "text"
                },
                "text_evidences": {
                    "type": "nested",
                    "properties": {
                        "file": {
                            "type": "text"
                        },
                        "filename": {
                            "type": "text"
                        }
                    }
                },
                "binary_evidences": {
                    "type": "nested",
                    "properties": {
                        "file": {
                            "type": "binary",
                            "store": true
                        },
                        "filename": {
                            "type": "text"
                        }
                    }
                },
                "created": {
                    "type": "date"
                }
            }
        }
    }
}
'
