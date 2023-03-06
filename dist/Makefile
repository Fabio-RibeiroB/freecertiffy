
destroy::
	docker-compose -f docker-compose-dist.yaml down
	docker container ls -q
	docker image ls -q |xargs  -I{}  docker image rm -f {}
	docker volume ls -q |xargs  -I{}  docker volume rm -f {}
