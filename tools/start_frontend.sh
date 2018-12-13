#!/bin/bash

source ../virtualenv/bin/activate

# set ES_HOST and ES_PORT
export ES_HOST="localhost"
export ES_PORT="9200"

# set FRONTEND_PORT
export FRONTEND_PORT="5000"

python ../frontend/app.py