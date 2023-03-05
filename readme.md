# FreeCertiffy

# docker-compose.yaml here is to build two containers:
  - flaskapp is the main program freecertiffy
  - mongo container for the database
  - with the container volume mongodb

# Fun Facts about the database admin passwords:
  - There has to be an admin user set to protect mongodatabase.
  - These are set in the docker-compose.yaml to initialise the database, and in flaskapp/flaskapp/,env for the app to refer to it.
  - It's easiest to change these BEFORE you run it up obviously.

# Mongo Database essentials
  - The mongo database is called "freecertiffy" and has two collections: "users" and "certificates"
  - The "users" database needs a default entry using this  __insert_user_record_to_freecertiffy.py__ once the containers are up


# So from the beginning:
   - prepare your user "admin" password for the mongo database in docker-compose.yaml and flaskapp/flaskapp/.env
   - prepare the script "utility_insert_admin_user.py" in this directory for your initial admin login

# Manually make the docker volume once:
   - docker volume make freecertiffy_mongo

# build
Now lets run __docker-compose build__ to  make the three images.

# up
Now run __docker-compose up -d__ to run the containers.

# ps
List the containers:
```
 docker container ps

CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS              PORTS                      NAMES
037e630c3f95   redis              "docker-entrypoint.s…"   About a minute ago   Up About a minute   6379/tcp                   freecertiffy-freecertiffy_redis-1
a39453821858   bradymd/flaskapp   "gunicorn -b 0.0.0.0…"   About a minute ago   Up About a minute   0.0.0.0:90->5000/tcp       freecertiffy-flaskapp-1
e76cc1acf1bc   mongo              "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:27017->27017/tcp   freecertiffy-mongo-1
```

# Set the user password in freecertiffy
So now we need a record in the mongo database for an initial user.
So this problem here is you have to run it on the freecertiffy container
``
    docker exec -it a39453821858  ./insert_user_record_to_freecertiffy.py
```
# Now login

Now login to http://localhost:90

# Preserving your data

As long as you don't delete the volume the data should be ok even if you destroy the containers. 

# Delete everything except the volume
```
	docker ps --filter name=freecertiffy-mongo-1 -q |xargs docker rm -f 
	docker ps --filter name=freecertiffy-redis-1 -q |xargs docker rm -f 
	docker ps --filter name=freecertiffy-flaskapp-1 -q |xargs docker rm -f 
	docker-compose stop
	docker-compose rm -f
	docker-compose images  -q | xargs docker image rm 
```

# Build and up everything
```
	docker-compose build
	docker-compose up -d
```

and you can login and your data is still there.



