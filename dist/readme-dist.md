# FreeCertiffy
## Description
FreeCertiffy is a containerised python flask application to manage certificates.
At the moment it just emails contacts as certificates are to expire but will do more in the future.
Most of this is about learning - flask, docker, mongo etc

## MANIFEST
  - docker-compose-dist.yaml   
  - myenv-dist.env		 

## docker-compose-dist.yaml 
These instructions to pull and configure three images mongo, bradymd/flaskapp, and redis.
The file defines the ports they will use and network.

## myenv-dist.env
Allows us to set other settings, including the admin password for the mongo database.
It can run as-is or as a minimum  - setting a unique admin password.

## pull the images
```
	docker-compose -f docker-compose-dist.yaml pull
```

## create the containers, volume, network, bring up, run the initialise container
```
	docker-compose --profile runonce  -f docker-compose-dist.yaml up  -d
```

The profile "runonce" will trigger the first user account to go on. 

## Now Login as admin/admin
```
	http://localhost:90
```

Add users with roles. Add url and ports.

## down the containers

```
	docker-compose --f docker-compose-dist.yaml down
```

## The code for flaskapp
```
  git clone github.com/bradymd/freecertiffy.git
```
