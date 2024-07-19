#!/bin/sh

docker run --name mongodb -d -p 27017:27017 -v ~/mongodb_data:/data/db mongo:latest


pip3 install pymongo

docker stop mongodb
docker restart mongodb