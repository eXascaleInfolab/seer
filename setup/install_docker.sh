#!/bin/sh
# Docker isntalation
sudo apt-get update

sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

sudo apt install -y curl

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

current_user=$(whoami)
sudo usermod -aG docker "$current_user"
newgrp docker
sudo chmod 666 /var/run/docker.sock