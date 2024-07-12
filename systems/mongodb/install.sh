#!/bin/sh
docker pull mongodb/mongodb-community-server

docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server:latest

pip3 install pymongo

docker stop mongodb

docker start mongodb
docker stop mongodb
docker restart mongodb