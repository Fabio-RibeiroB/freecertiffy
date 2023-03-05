
A generic app for distributiuon has to NOT take utilise an __.env__  file 
in the app but has to use variables.

docker run --env-file ./.env   image .

```
import os
username = os.environ['MY_USER']
```

We currently use load_dotenv which loads variables in to the environment from a file
```
load_dotenv(path.join(basedir, ".env"))
```
It's really good but with docker but the .env file is in the container and so not so accessible.

If we include 
```
  env_file:
        - myenv.env
```
in docker-compose.yaml these variables can be put in the environment as the container is run up.
```
  import os
  username = os.environ['MY_USER']
```

