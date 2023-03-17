import requests, json, sys, socket, time, logging, re
from modules.cert.readwrite import  read_records_db,update_record_db , read_record_db
from flask import Flask, flash

def grade_ssllabs(hostname):
  debug=True
  logging.basicConfig(level=logging.WARNING)
  logging.debug('/grade_ssllabs')
  cert = { 'url' : hostname, 'port' : '443'}
  # ssllabs can only scan port 443
  try:
    ipAddress = socket.gethostbyname(hostname)   
  except:
    flash(f"Problem with hostname {hostname}","warning")
    logging.debug('host %s gethostyname error' % (hostname ))
    return 
  result=read_record_db(cert)
  if len(result) >0:
    if result[0]['status'] == 'down':
       flash(f"Host might be down, run Check first on {hostname}:443", "warning")
       return
  url = 'https://api.ssllabs.com/api/v3/analyze?host=' + hostname + '&s=' + ipAddress + '&startNew=on&ignoreMismatch=on&all=done&hideResults=on'
  response=requests.get(url,verify=False)
  j = response.json()
  count=1
  sleep_count= [ 60, 60, 30, 10, 10 ]
  while j['status'] == "IN_PROGRESS" or j['status'] == "DNS":
    if count < 5:
      sleep=sleep_count[count]
    else:
      sleep=10
    logging.debug('host %s, status %s, sleep %s, count %d' % (hostname, j['status'],sleep, count))
    time.sleep(sleep)
    count=count+1
    url = 'https://api.ssllabs.com/api/v3/analyze?host=' + hostname + '&s=' + ipAddress + '&fromCache=on&ignoreMismatch=on&all=done'
    response=requests.get(url,verify=False)
    j = response.json()

  #logging.debug('host %s : %s' % (hostname, j ))
  try:
    j['statusMessage']
    if j['statusMessage']  == "Unable to connect to the server" or j['statusMessage']  == "Unable to resolve domain name" or \
             j['statusMessage']  == "No secure protocols supported":
      logging.debug('host %s, is not public ' %  hostname )
      records = read_records_db()
      for r in records:
        if r['url'] == hostname:
          r['exposed'] = False 
          hold=r
          update_record_db(hold)
      #write_records(records)
      return(hold)
  except:
     pass

  try:
    e=j['endpoints']
    endpoints= e[0]
    if endpoints['statusMessage']  == "Unable to connect to the server" or endpoints['statusMessage']  == "Unable to resolve domain name" or \
             endpoints['statusMessage']  == "No secure protocols supported":
      logging.debug('host %s, is not public ' %  hostname )
      records = read_records_db()
      for r in records:
        if r['url'] == hostname:
          r['exposed'] = False 
          hold=r
          update_record_db(hold)
      #write_records(records)
      return(hold)
  except:
    pass
    
  
  if j['status'] == 'ERROR':
    logging.debug(('host %s, status %s ') % ( hostname, j))
    sys.exit()
    
  logging.debug(('host %s, response %s, : ') % ( hostname, j))
  v = { 'hostname': "",  
          'ipAddress': "", 
          'grade': "",  
          'hasWarnings': "",  
          'isExceptional': "", 
  	'heartbleed': "",
          'vulnBeast': "",
  	'poodle': "",
  	'freak': "",
           "logjam": "",
  	"supportsRc4": "",
  	"TLS" : "",
  	"serverName": hostname } 
  
  # Maybe I will find a better way of parsing this lot
  v['hostname'] = j['host']
  e = j['endpoints']
  endpoints= e[0]
  v['grade'] = endpoints['grade']
  # Why does this serverName sometimes not appear?
  try:
    endpoints['serverName']
  except:
    endpoints['serverName'] = ""
  v['serverName'] = endpoints['serverName']
  v['ipAddress']  =  endpoints['ipAddress']
  v[ 'hasWarnings' ] = endpoints['hasWarnings']
  v['isExceptional' ]  = endpoints[ "isExceptional" ]
  details=endpoints['details']
  protocols = (details['protocols'])
  TLS  =  [ ]
  for t in protocols:
    TLS.append(t['version'])
  v['TLS'] = TLS
  v['heartbleed'] = details['heartbleed']
  v['vulnBeast'] = details['vulnBeast']
  v['poodle'] = details['poodle']
  v['freak'] = details['freak']
  v['logjam'] = details['logjam']
  v['supportsRc4'] = details['supportsRc4']
  # Merges the information
  #records = read_records_db()
  records = read_record_db({'url': hostname , 'port' : '443'})
  for r in records:
    if r['url'] == v['hostname']:
        r['exposed'] = True
        r['status'] = "up"
        r['ssllabs'] = v
        hold=r
        if update_record_db(hold):
            pass
        else:
            flash("Failed to update_record_db for  %s", r['url'])
            return render_template("flash.html", header="Grading Attempt")
  return

