#!/bin/bash
# get cmd line arg default to hataraki-backend-container if none
CONTAINER_NAME=${1:-hataraki-backend-container}

# stop and remove old container
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
docker build -t hataraki-backend .
docker run -d --name $CONTAINER_NAME -p 8001:8001 --env-file .env hataraki-backend
