#!/usr/bin/env python3
from passlib.context import CryptContext
import sys
import json
from pymongo import MongoClient, ReturnDocument
from modules.users.readwrite_validusers  import insert_user_record_db
'''
def insert_user_record_db(record):
    count = collection.count_documents({"username": record["username"]})
    result = collection.find({"username": record["username"]})
    if count == 0:
        collection.insert_one(record)
        return True
    else:
        return False
'''

password="admin"
ctx = CryptContext(
    schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=14
)
enc_pw=ctx.hash(password)

record=  {
    'username': "admin",
    'role': "admin",
    'fullname': "Mr test",
    'email': "",
    'password': enc_pw
  }
insert_user_record_db(record)

