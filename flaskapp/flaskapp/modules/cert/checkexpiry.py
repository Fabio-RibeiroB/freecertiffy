
import time
from datetime import datetime, timezone
import OpenSSL
import ssl
import socket
from flask import Flask, flash

import logging
logging.basicConfig(level=logging.WARN)
logging.debug("module readwrite")
logging.captureWarnings(True)

def checkcert(cert):
    url=cert['url']
    port=cert['port']
    socket.setdefaulttimeout(2)
    try:
        cert=ssl.get_server_certificate((url, port))
    except Exception  as err:
        flash(f"Failed to connect to {url}:{port}", "warning")
        logging.debug( "No connection: {0}".format(err))
        return(-1,-1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    bytes=x509.get_notAfter()
    timestamp = bytes.decode('utf-8')
    certExpires =  datetime.strptime(timestamp, '%Y%m%d%H%M%S%z').replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    daysToExpiration = (certExpires - now).days 
    logging.debug(f"url = {url}:{port} days2Go = {daysToExpiration}")
    return (daysToExpiration,certExpires)

'''
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

'''