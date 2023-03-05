#bind = "localhost:8000"
#workers = 1
pidfile = "gunicorn.pid"
##certfile='/etc/pki/tls/certs/certiffy2022.ca-bundle'
##keyfile='/etc/pki/tls/private/certiffy2022.key'
# Ubuntu local certificates
#certfile="ssl/localhost.crt"
#keyfile="ssl/localhost.key"
loglevel = 'debug'
#accesslog='logs/gunicorn-access.log'
#errorlog='logs/gunicorn-error.log'
timeout = 240000
# Put the output into error.log
capture_output=True
