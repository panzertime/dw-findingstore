#!/bin/bash

# set ES_HOST and ES_PORT
export ES_HOST=localhost
export ES_PORT=9200

../virtualenv/bin/activate
python ../frontend/app.py