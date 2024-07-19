#!/bin/sh

sudo kill -9 `sudo lsof -t -i:9000`
sleep 2

#pip3 install clickhouse-driver

docker pull clickhouse/clickhouse-server

# Run the ClickHouse container
docker run -d --name clickhouse-container --restart unless-stopped -p 8123:8123 -p 9000:9000 -v $(pwd)/clickhouse-config.xml:/etc/clickhouse-server/config.xml -v $(pwd)/clickhouse-data:/var/lib/clickhouse clickhouse/clickhouse-server
docker exec -it clickhouse-container chown -R clickhouse:clickhouse /var/lib/clickhouse

#sleep 5
#sudo docker stop clickhouse-container