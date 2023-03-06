# FreeCertiffy
## Running this program
All you need is the instructions in the dist directory.

Everything else in this repository is for the code for the flaskapp itself.

You can use this to also run the containers and have access to the code.


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

## Run docker-compose with the runonce profile
The runonce profile will do run the initialisation of the mongo user database.
```
    docker-compose --profile runonce up -d
```

## List the containers:
```
docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS          PORTS                      NAMES
cfcf8da62250   mongo              "docker-entrypoint.s…"   About a minute ago   Up 57 seconds   0.0.0.0:27017->27017/tcp   freecertiffy_mongo
4bc53bb04bda   bradymd/flaskapp   "gunicorn -b 0.0.0.0…"   About a minute ago   Up 57 seconds   0.0.0.0:90->8000/tcp       freecertiffy_flaskapp
```

## Now login
  - login to http://localhost:90 with the default login is admin/admin.
  - Go into user management and change it.

# Preserving your data
As long as you don't delete the volume the data should be ok even if you destroy the containers. 
From the docker host you can still contact the database with mongosh  and monoexport and mongodump.

# Test it by deleting everything except the volume
```
        docker-compose stop
        docker container ls -a --filter name=freecertiffy_mongo -q |xargs docker container rm -f 
        docker container ls -a --filter name=freecertiffy_redis -q |xargs docker container rm -f 
        docker container ls -a --filter name=freecertiffy_flaskapp -q |xargs docker container rm -f 
        docker container ls -a --filter name=freecertiffy_runonce -q |xargs docker container rm -f 
        docker image  rm bradymd/flaskapp  mongo redis
        #docker volume rm freecertiffy_mongo
```

# And re-build the flaskapp image and bring them up
```
	docker-compose build
	docker-compose up -d
```

And as configured you can login to http://loaclhost:90 your data is still there.


# Now for Developing it
## You need the Source Code
```
    git clone git@github.com:bradymd/freecertiffy.git
```

## python environment
So one time:
```
    cd flaskapp/flaskapp
    python3 -m venv ~/.venv/freecertiffy
    python3 -m pip ~/.venv/freecertiffy/bin/activate
    pip install -r requirements.txt
```
From now on 
```
. ./source_me
```
or
```
.   ~/.venv/freecertiffy/bin/activate
```

## Edit your myenv.env
Make sure these are variables are set:
```
ENVIRONMENT="DEVELOPMENT"
FLASK_DEBUG=1
LEVEL=DEBUG
```
Run up the mongo container, stop the flaskapp
```
    docker container  start freecertiffy_mongo
    docker container  stop freedcertiffy_flaskapp
```
Now run flask on the command line:
```
    cd flaskapp/flaskapp
    flask --env-file ../../myenv.env run
```
Thats a way to debug and develop this flaskapp. It restarts if you edit a file.
```
    http://localhost:5000
```
