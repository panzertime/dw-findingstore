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

source ../virtualenv/bin/activate

# set ES_HOST and ES_PORT
export ES_HOST="localhost"
export ES_PORT="9200"

# set FRONTEND_PORT
export FRONTEND_PORT="5000"

python ../frontend/app.py