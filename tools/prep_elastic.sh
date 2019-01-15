#!/bin/bash

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
