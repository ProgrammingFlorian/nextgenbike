#!/bin/bash
docker prune -f
docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)