#!/bin/bash

# Set the container ID
container_id=$(docker ps | grep app | awk '{print $1}')

# Check if container ID is found
if [ -z "$container_id" ]; then
    echo "Container not found. Exiting."
    exit 1
fi

# Print the container ID
echo "Using container ID: $container_id"

# Execute Python commands in Django shell
echo "from djangoProject.models.load_query_data import load_offline_query_data
load_offline_query_data()" | docker exec -i $container_id python3 manage.py shell

# Optional: Add a command to exit if needed. Most shells will exit automatically after the script execution.