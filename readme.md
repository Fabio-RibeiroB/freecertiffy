# FreeCertiffy
## Running this program
All you need to try this out is the dist directory which has the docker-compose-dist.yaml and my-env.env file.

Everything else in this repository is if you want access to the flaskapp code or want to work out what it's doing.

## docker-compose.yaml here is to build two containers:
  - freecertiffy_flaskapp is the flaskapp container
  - freecertiffy_mongo is the database with volume freecertiffy_mongo

## Fun Facts about the database admin passwords:
  - There has to be an admin user and password to protect the mongo database.
  - These are set in **myenv.env**

## Mongo Database essentials
  - The mongo database is called "freecertiffy" and has two collections: "users" and "certificates"

## From the top Maestro
### Edit __myenv.env__
  - prepare your user "admin" password for the mongo database in __myenv.env__

## Run docker-compose with the runonce profile
The runonce profile will do run the initialisation of the mongo user database.
```
    docker-compose --profile runonce up -d
```
This runonce profile is to run certiffy_flaskkapp witha insert program to initialise the user colllection - so you can login.

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

## Preserving your data
As long as you don't delete the volume the data should be ok even if you destroy the containers. 
From the docker host you can still contact the database with mongosh  and monoexport and mongodump.

## Test it by deleting everything except the volume
```
        docker-compose stop
        docker container ls -a --filter name=freecertiffy_mongo -q |xargs docker container rm -f 
        docker container ls -a --filter name=freecertiffy_redis -q |xargs docker container rm -f 
        docker container ls -a --filter name=freecertiffy_flaskapp -q |xargs docker container rm -f 
        docker container ls -a --filter name=freecertiffy_runonce -q |xargs docker container rm -f 
        docker image  rm bradymd/flaskapp  mongo redis
        #docker volume rm freecertiffy_mongo
```
Have a look at Makefile for further examples. eg
``
        make destroy
        make build
```

## Now for Developing it
### You need the Source Code
```
    git clone git@github.com:bradymd/freecertiffy.git
```

## establish python environment
So one time:
```
    cd flaskapp/flaskapp
    python3 -m venv ~/.venv/freecertiffy
    python3 -m pip ~/.venv/freecertiffy/bin/activate
    pip install -r requirements.txt
```
From now on 
```
.   ./source_me
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
