#!/bin/bash

source ../virtualenv/bin/activate

# set ES_HOST and ES_PORT
set ES_HOST="localhost"
set ES_PORT="9200"

# set FRONTEND_PORT
set FRONTEND_PORT="5000"

python ../frontend/app.py