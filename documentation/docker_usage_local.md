# Docker Usage
## Build
Make sure you are in the nextgenbike folder  
To build:  
$ docker-compose build

## Local Test
Tag:  
$ docker tag backend-app backend

Run: 
$ docker run -d -p 80:80 backend

Test:  
$ curl localhost:80

Stop: 
$ docker stop backend

### Delete
delete all containers  
$ docker rm -vf $(docker ps -aq)  
delete all images  
$ docker rmi -f $(docker images -aq)

## Push to Digitalocean:
from local Laptop
Login  
$ docker login -u $PASSKEY$ registry.digitalocean.com
$ doctl registry login

Tag:  
$ docker tag backend-app registry.digitalocean.com/nextgenbike-backend/backend:763a396

Push:  
$ docker push registry.digitalocean.com/nextgenbike-backend/backend:763a396

Run:  
$ docker rm backend
$ docker run -d -p 80:80 --restart always --name backend registry.digitalocean.com/nextgenbike-backend/backend:763a396

Test:  
$ curl 68.183.226.91:80

Stop:  
$ docker stop backend

Logout:  
$ docker logout registry.digitalocean.com
