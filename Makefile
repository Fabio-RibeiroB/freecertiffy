firsttime:
	docker-compose --profile runonce up -d

build:
	docker-compose build

up:
	docker-compose up -d
	docker logs -f `docker ps --filter name=freecertiffy_flaskapp -q `

down:
	docker-compose down 
stop:
	docker-compose stop
start:
	docker-compose start
destroy:
	docker-compose stop
	docker container ls -a --filter name=freecertiffy_mongo -q |xargs docker container rm -f 
	docker container ls -a --filter name=freecertiffy_redis -q |xargs docker container rm -f 
	docker container ls -a --filter name=freecertiffy_flaskapp -q |xargs docker container rm -f 
	docker container ls -a --filter name=freecertiffy_runonce -q |xargs docker container rm -f 
	docker image  rm bradymd/flaskapp  mongo redis
	docker volume rm freecertiffy_mongo
	
flask:
	docker ps --filter name=freecertiffy_flaskapp -q |xargs docker rm -f 
	docker ps --filter name=freecertiffy_runonce -q |xargs docker rm -f 
	docker image rm  bradymd/flaskapp
	docker-compose build
	docker-compose up -d
	docker logs -f `docker ps --filter name=freecertiffy_flaskapp -q`

mongo::
	docker ps --filter name=freecertiffy_mongo -q |xargs docker rm -f 
	docker image rm mongo 
	docker-compose build
	docker-compose up -d
	docker logs -f `docker ps --filter name=freecertiffy_mongo -q`

init_mongo:
	docker volume create freecertiffy_mongo

push:
	docker push bradymd/flaskapp


