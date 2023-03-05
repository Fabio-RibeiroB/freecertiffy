import json
from pymongo import MongoClient, ReturnDocument
from flask import flash, render_template
import datetime
import re
import os

import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("module readwrite")
logging.captureWarnings(True)

#from dotenv import dotenv_values
#config_data = dotenv_values(".env")
MONGO_INITDB_ROOT_USERNAME=os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD=os.environ["MONGO_INITDB_ROOT_PASSWORD"]
if os.environ['ENVIRONMENT'] == 'DEVELOPMENT':
    CONNECTSTRING=os.environ['CONNECTSTRING_DEVELOPMENT']
else:
    CONNECTSTRING=os.environ['CONNECTSTRING_PRODUCTION']
CONNECTSTRING=re.sub("//.*@","//"+ MONGO_INITDB_ROOT_USERNAME + ":" + MONGO_INITDB_ROOT_PASSWORD + "@", CONNECTSTRING)
logging.debug(f'modules/cert/readwrite.py CONNECTSTRING = {CONNECTSTRING}')

client = MongoClient(CONNECTSTRING)
db = client.freecertiffy
collection = db.certificates



def read_records_db():
    result = collection.find({})
    return_list = []
    for x in result:
        return_list.append(x)
    return_list = sorted(return_list, key=lambda d: d['daysToGo'])
    return return_list


def read_record_db(record):
    logging.getLogger().setLevel(logging.DEBUG)
    count = collection.count_documents(record)
    if record['port'] == "*":
        record['port'] = record['port'].replace('*','.*')
    if re.search("\*",record['url']):
        record['url'] = record['url'].replace('*','.*')
        querystring = { '$and' : [ { "url" :  { "$regex" : record['url'] }},
                         { "port" : { "$regex" : record['port']} } ] }
        logging.debug(f"searching {querystring}")
        result = collection.find(querystring)
    else:
        result = collection.find(record)
    return_list = []
    for x in result:
        return_list.append(x)
        if count == 1:
            return [return_list[0]]
    logging.warn("read_record_db %d %s" % (count, str(record)))
    return return_list


def read_record_db_ext(record):
    logging.getLogger().setLevel(logging.WARN)
    count = collection.count_documents({"url": record["url"]})
    result = collection.find({"url": record["url"]})
    return_list = []
    logging.debug("read_record_db %d", count)
    for x in result:
        return_list.append(x)
    logging.debug("read_record_db %d %s" % (count, str(record)))
    return return_list, count


# We used to rewrite the whole list of records, now its just one dict record
def insert_record_db(record):
    logging.getLogger().setLevel(logging.DEBUG)
    count = collection.count_documents({"url": record["url"], "port": record["port"] })
    result = collection.find({"url": record["url"], "port": record["port"] })
    if count == 0:
        collection.insert_one(record)
        logging.debug("insert_record_db success: {}".format(record))
        return True
    else:
        logging.warning("insert_record_db failed: {}".format(record))
        logging.warning("result =  : {}".format(result))
        return False


def delete_record_db(record):
    logging.getLogger().setLevel(logging.DEBUG)
    count = collection.count_documents({"url": record["url"]})
    result = collection.find({"url": record["url"]})
    if count >= 1:
        collection.delete_one(record)
        logging.debug("deleted_record_db success: {}".format(record))
        return True
    else:
        logging.warning("deleted_record_db failed: {}".format(record))
        return False


def update_record_db(record):
    logging.getLogger().setLevel(logging.WARN)
    count = collection.count_documents({"url": record["url"]})
    result = collection.find({"url": record["url"]})
    if count == 1:
        mongo_id = result[0]["_id"]
        logging.debug(
            "update_record_db: %s",
            collection.find_one_and_update(
                {"_id": mongo_id},
                {"$set": record},
                return_document=ReturnDocument.AFTER,
            ),
        )
        return True
    else:
        flash("Failed to update this record", "error")
        flash(f"record is %s" % record, "info")
        return render_template("flash.html", header="function: update_record_db")


def update_record_db_ext(record):
    logging.getLogger().setLevel(logging.WARN)
    search_term ={ "url": record["url"],"port": record["port"] } 
    count = collection.count_documents( search_term )
    result = collection.find( search_term )
    if count == 1:
        mongo_id = result[0]["_id"]
        logging.debug(
            "update_record_db: %s",
            collection.find_one_and_update(
                {"_id": mongo_id},
                {"$set": record},
                return_document=ReturnDocument.AFTER,
            ),
        )
        return True
    else:
        return False

def recalculateAll():
    logging.getLogger().setLevel(logging.DEBUG)
    certs = read_records_db()
    for cert in certs:
        try: 
             cert['expiryDate']
             newDaysToGo = ( (cert['expiryDate'] - datetime.datetime.now()).days)
             if cert['daysToGo'] != ((cert['expiryDate']- datetime.datetime.now()).days):
                 cert['daysToGo'] = (cert['expiryDate'] - datetime.datetime.now()).days
                 mongo_id = cert["_id"]
                 logging.debug(
                    "update_record_db: %s",
                    collection.find_one_and_update(
                        {"_id": mongo_id},
                        {"$set": {'daysToGo': cert['daysToGo']}},
                        return_document=ReturnDocument.AFTER,
                     ),
                 )
             else:
                 logging.debug(f"Didn't process {cert['url']}")
        except:
            logging.debug(f"Couldnt process {cert['url']} expiryDate={cert['expiryDate']} daysToGo={cert['daysToGo']}")
            pass
    return True
