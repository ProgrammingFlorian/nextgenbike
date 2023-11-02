#!/bin/bash
echo "Building the image via docker-compose"
docker-compose build
echo "tagging backend-app to backend"
docker tag backend-app backend
echo "running the server with exposed port 80 on localhost"
docker run -d -p 80:80 backend -it --mount type=bind,src="$(pwd)"/backend/server/etc/data_db,target=/app/server/etc/data_db
