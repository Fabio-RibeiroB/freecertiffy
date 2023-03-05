# FreeCertiffy

# docker-compose.yaml here is to build two containers:
  - flaskapp is the main program freecertiffy
  - mongo container for the database
  - with the container volume mongodb

# Fun Facts about the database admin passwords:
  - There has to be an admin user and password to protect the mongo database.
  - You  set these in **myenv.env**

# Mongo Database essentials
  - The mongo database is called "freecertiffy" and has two collections: "users" and "certificates"
  - The "users" collection needs a default entry using this  __insert_user_record_to_freecertiffy.py__ once the containers are up
    (This is explained below as the sequence of bringing up the containers is outlined.)

# From the top Maestro
## Edit __myenv.env__
  - prepare your user "admin" password for the mongo database in __myenv.env__
## Make your volume
  ```
        docker volume make freecertiffy_mongo
  ```
## Build the container images
Now lets run __docker-compose build__ to  make the three images.
## Bring the containers  up
Now run __docker-compose up -d__ to run the containers.

## List the containers:
```
 docker container ps

CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS              PORTS                      NAMES
037e630c3f95   redis              "docker-entrypoint.s…"   About a minute ago   Up About a minute   6379/tcp                   freecertiffy-freecertiffy_redis-1
a39453821858   bradymd/flaskapp   "gunicorn -b 0.0.0.0…"   About a minute ago   Up About a minute   0.0.0.0:90->5000/tcp       freecertiffy-flaskapp-1
e76cc1acf1bc   mongo              "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:27017->27017/tcp   freecertiffy-mongo-1
```

## Initialise the user collection 
So now we need a record in the mongo database for an initial user.
Find your container ID and run this
```
    docker exec -it a39453821858  ./insert_user_record_to_freecertiffy.py
```
## Now login
  - Now login to http://localhost:90, the default login is admin/admin.
  - Go into user management and change it.

# Preserving your data
As long as you don't delete the volume the data should be ok even if you destroy the containers. 
From the docker host you can still contact the database with mongosh  and monoexport and mongodump.

# Test it by deleting everything except the volume
```
	docker ps --filter name=freecertiffy-mongo-1 -q |xargs docker rm -f 
	docker ps --filter name=freecertiffy-redis-1 -q |xargs docker rm -f 
	docker ps --filter name=freecertiffy-flaskapp-1 -q |xargs docker rm -f 
	docker-compose stop
	docker-compose rm -f
	docker-compose images  -q | xargs docker image rm 
```

# And Build the images and containers and bring them up
```
	docker-compose build
	docker-compose up -d
```

And as configured you can login to http://loaclhost:90 your data is still there.



