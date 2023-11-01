#!/bin/bash
docker-compose build
docker tag backend-app backend
docker run -d -p 80:80 backend
curl localhost:80