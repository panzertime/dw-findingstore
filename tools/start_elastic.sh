#!/bin/bash

#docker run --name elasticsearch-dev -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.5.3
docker run --name elasticsearch-dev --rm -p 9200:9200 -p 9300:9300 elasticsearch:6.5.2 &
