import json
from pymongo import MongoClient, ReturnDocument
from flask import flash, render_template
from dotenv import dotenv_values
import logging

import os
logging.basicConfig(level=logging.DEBUG)
logging.debug("program readwrite_validusers")
logging.captureWarnings(True)
logging.getLogger().setLevel(logging.DEBUG)
import re

#config_data = dotenv_values(".env")
MONGO_INITDB_ROOT_USERNAME=os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD=os.environ["MONGO_INITDB_ROOT_PASSWORD"]
if os.environ['ENVIRONMENT'] == 'DEVELOPMENT':
    CONNECTSTRING=os.environ['CONNECTSTRING_DEVELOPMENT']
else:
    CONNECTSTRING=os.environ['CONNECTSTRING_PRODUCTION']
CONNECTSTRING=re.sub("//.*@","//" + MONGO_INITDB_ROOT_USERNAME + ":" + MONGO_INITDB_ROOT_PASSWORD + "@", CONNECTSTRING)
logging.debug(f"modules/users/readwrite_validusers.py CONNECTSTRING={CONNECTSTRING}")

client = MongoClient( CONNECTSTRING )
db = client.freecertiffy
collection = db.users


def read_user_records_db() -> list:
    result = collection.find({})
    return_list = []
    for x in result:
        return_list.append(x)
    return return_list

def read_user_record_db(username):
    logging.getLogger().setLevel(logging.DEBUG)
    count = collection.count_documents({"username": username})
    result = collection.find({"username": username})
    return_list = []
    for x in result:
        return_list.append(x)
        if count == 1:
            return [return_list[0]]
    logging.warn("read_record_db %d %s" % (count, str(username)))
    return return_list


def read_user_record_db_ext(username):
    logging.getLogger().setLevel(logging.WARN)
    count = collection.count_documents({"username": username})
    result = collection.find({"username": username})
    return_list = []
    logging.debug("read_record_db %d", count)
    for x in result:
        return_list.append(x)
    logging.debug("read_record_db %d %s" % (count, str(username)))
    return return_list, count


# We used to rewrite the whole list of records, now its just one dict record
def insert_user_record_db(record):
    logging.getLogger().setLevel(logging.DEBUG)
    count = collection.count_documents({"username": record["username"]})
    result = collection.find({"username": record["username"]})
    if count == 0:
        collection.insert_one(record)
        logging.debug("insert_record_db success: {}".format(record))
        return True
    else:
        logging.warning("insert_record_db failed: {}".format(record))
        return False


def delete_user_record_db(record):
    logging.getLogger().setLevel(logging.DEBUG)
    count = collection.count_documents({"username": record["username"]})
    result = collection.find({"username": record["username"]})
    if count >= 1:
        collection.delete_one(record)
        logging.debug("deleted_record_db success: {}".format(record))
        return True
    else:
        logging.warning("deleted_record_db failed: {}".format(record))
        return False


def update_user_record_db(record):
    logging.getLogger().setLevel(logging.WARN)
    count = collection.count_documents({"username": record["username"]})
    result = collection.find({"username": record["username"]})
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
        flash("Failed to update this record")
        flash("record is %s", record)
        return render_template("flash.html", header="function: update_record_db")


def update_user_record_db_ext(record):
    logging.getLogger().setLevel(logging.WARN)
    count = collection.count_documents({"username": record["username"]})
    result = collection.find({"username": record["url"]})
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
