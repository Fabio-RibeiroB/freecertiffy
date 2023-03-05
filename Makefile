build:
	docker-compose build
up:
	docker-compose up -d
	sleep 2
	#(cd mongo ; ./mongo_restore.sh )
	docker logs -f `docker ps --filter name=freecertiffy-flaskapp-1 -q `

down:
	docker-compose down 
stop:
	docker-compose stop
start:
	docker-compose start
destroy:
	docker ps --filter name=freecertiffy-mongo-1 -q |xargs docker rm -f 
	docker ps --filter name=freecertiffy-redis-1 -q |xargs docker rm -f 
	docker ps --filter name=freecertiffy-flaskapp-1 -q |xargs docker rm -f 
	docker-compose stop
	docker-compose rm -f
	docker-compose images  -q | xargs docker image rm 
	
flask:
	docker ps --filter name=freecertiffy-flaskapp-1 -q |xargs docker rm -f 
	docker image rm  flaskapp
	docker-compose build
	docker-compose up -d
	docker logs -f `docker ps --filter name=freecertiffy-flaskapp-1 -q`

mongo::
	docker ps --filter name=freecertiffy-mongo-1 -q |xargs docker rm -f 
	docker image rm mongo 
	docker-compose build
	docker-compose up -d
	docker logs -f `docker ps --filter name=freecertiffy-mongo-1 -q`

init_mongo:
	docker volume create freecertiffy_mongo

push:
	docker push bradymd/flaskapp


