FROM ubuntu:latest
RUN apt update -y                                                                                            
RUN apt upgrade -y
RUN apt install python3 python3-pip -y 
RUN apt-get install iputils-ping -y   
RUN apt install vim -y               
WORKDIR /app                        
COPY flaskapp/  /app         
RUN python3 -m pip install  --no-cache-dir -r requirements.txt               
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]

