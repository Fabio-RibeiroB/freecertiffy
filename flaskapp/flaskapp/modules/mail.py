import sys
import getopt
import re
import os
from datetime import datetime, date, timedelta
from operator import itemgetter
import json

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dns
import dns.resolver
import logging
from flask import Flask, flash

# from modules.cert import read_records_db


import logging

logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logging.captureWarnings(True)
logging.info("mail-contacts.py program startup ")

DEFAULT_CONTACT = os.environ["DEFAULT_CONTACT"]
SMTPHOST = os.environ["SMTPHOST"]

mail = True


def my_dns(trial, quiet):
    message = "Examining DNS for " + trial + ":</br>"
    try:
        # ip = dns.resolver.query(trial,'A')
        ip = dns.resolver.resolve(trial, "A")
        for i in ip:
            message = message + "&emsp;" + i.to_text() + "</br>"
    except dns.resolver.NoAnswer:
        if not quiet:
            print("\t[-] No cname ")
    except dns.exception.Timeout:
        if not quiet:
            print("\t[-] Timeout")
    except dns.resolver.NXDOMAIN:
        if not quiet:
            print("[.] Resolved but no entry ")
    try:
        # cname = dns.resolver.query(trial,'CNAME')
        cname = dns.resolver.resolve(trial, "CNAME")
        for cn in cname:
            message = message + "&emsp;" + str(cn.target) + "</br>"
    except dns.resolver.NoAnswer:
        if not quiet:
            print("\t[-] No cname ")
    except dns.exception.Timeout:
        if not quiet:
            print("\t[-] Timeout")
    except dns.resolver.NXDOMAIN:
        if not quiet:
            print("[.] Resolved but no entry ")
    return message


def mail_warning(contact, url, daystogo, expiry_date, port):
    logging.getLogger().setLevel(logging.WARN)
    global DEFAULT_CONTACT
    global SMTPHOST
    logging.debug(f"hello from mail_warning the  expiry_date is {expiry_date}")
    try:
        expiry_date = expiry_date.isoformat()
    except:
        # It can be set to -1
        expiry_date = "NaN"
    if mail == False:
        print(
            "not mailing %s about %s port %s daystogo %s  "
            % (contact, url, port, daystogo)
        )
        return
    sender_email = DEFAULT_CONTACT
    receiver_email = contact
    logging.debug("mailing %s about %s %s" % (contact, url, daystogo))
    message = MIMEMultipart("alternative")
    message["Subject"] = "TLS Cert expires " + str(daystogo) + """ days """ + url
    message["From"] = sender_email
    receivers = receiver_email.replace("+", ",")  # allow for multiple people
    message["To"] = receivers
    dnsmessage = my_dns(url, True)
    # Create the plain-text and HTML version of your message
    text = (
        """\
Hi,

the website """
        + url
        + """ will expire in  """
        + str(daystogo)
        + """ days. \
Please can you renew it or ask for this check to be removed.

Thank-you

"""
    )
    if expiry_date == "NaN":
        tip = (
            "<p><b>This service may in fact be unavailable and needs checking.</b></p>"
        )
    else:
        tip = ""
    html = (
        """\
<html>
  <body>
    <p>Hi,<br>
    This is a message from <a href=https://"""
        + os.environ["DEFAULT_HOST"]
        + """>https://"""
        + os.environ["DEFAULT_HOST"]
        + """</a> certificate expiry checker.<br>
    The tls certificate on - https://"""
        + url
        + """:"""
        + port
        + """ will expire in <b> """
        + str(daystogo)
        + """</b> days.  <br>
    <br>"""
        + tip
        + """
    That date is quoted as <b>"""
        + expiry_date
        + """</b> on port """
        + port
        + """ </br>
    Please can you work to renew or ask for it to be removed from the checker.<br>
    </p>"""
        + dnsmessage
        + """
    <p>Thank-you!</p>
  </body>
</html>
"""
    )
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(SMTPHOST)
    except: 
        flash(f"Problem connecting to {SMTPHOST}","warning")
        return False
    server.set_debuglevel(0)
    returncode = server.sendmail(sender_email, receivers.split(","), message.as_string())
    server.quit()
    if returncode == {}:
        flash(f"Mail successfully sent")
        return True
    else:
        flash(f"Failed to email {returncode}")
        return False

websites = []
sorted_websites = []


def check_it_runs(cmd):
    try:
        if subprocess.run(
            cmd.split(),
            timeout=3,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
        ):
            return True
    except:
        return False


"""
This is preparing for when it is to mail a large number

records=modules.cert.read_records_db()
for website in records:
    if website['daystogo'] < 9 and website['daystogo'] > 5:
      if website['contact'].find("+") != -1:
        #contact = str(website['contact']).replace("m.brady@herts.ac.uk+","")
        contact = str(website['contact']).replace( DEFAULT_CONTACT + "+", "")
        contact = str(website['contact']).replace( DEFAULT_CONTACT + ",", "")
        print("Have emailed additional contact %s"  % contact )
        mail_warning(contact, website['url'], website['daystogo'], website['expiry_date'], website['port'])
      else:
        contact=website['contact']
        mail_warning(contact, website['url'], website['daystogo'], website['expiry_date'], website['port'])
    # mail everyone if less than 5
    if website['daystogo'] <= 5:
        print('this point reached %s' % website['contact'])
        mail_warning(website['contact'], website['url'], website['daystogo'], website['expiry_date'], website['port'])

"""
