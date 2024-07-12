#!/bin/sh
echo "init seer"

container_id=$(docker ps | grep app | awk '{print $1}') #or find id of "app" using docker ps

echo "$container_id"

docker exec -it $container_id  python3 manage.py collectstatic --noinput

docker exec -it $container_id  python3 manage.py makemigrations

docker exec -it $container_id  python3 manage.py migrate

# optional
# docker exec -it $container_id  python3 manage.py createsuperuser