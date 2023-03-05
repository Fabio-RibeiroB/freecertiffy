import ssl
import socket
import datetime


import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("module readwrite")
logging.captureWarnings(True)

# this clever snippet from Melissa Gibson
# https://towardsaws.com/use-python-to-check-ssl-tls-certificate-expiration-and-notify-with-aws-ses-1ce17ed25616
def checkcert(cert):
    host = cert["url"]
    port = cert["port"]
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port),timeout=3.0) as sock:
            sock.settimeout(3)
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                certificate = ssock.getpeercert()
                certExpires = datetime.datetime.strptime(
                    certificate["notAfter"], "%b %d %H:%M:%S %Y %Z"
                )
                daysToExpiration = (certExpires - datetime.datetime.now()).days
                logging.debug(f"Expires on: {certExpires} in {daysToExpiration} days")
                return(daysToExpiration,certExpires)
    except:
        logging.debug(f"error connecting to Server, {host}")
    return(-1,-1)

