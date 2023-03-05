#!/usr/bin/env python3
"""
You need an admin user when you first start, or else the program won't let you login.  If you run it twice it overwrites your existing admin users.
"""
from modules.users.readwrite_validusers import update_user_record_db
from passlib.context import CryptContext

ctx = CryptContext(
    schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=14
)

record = {
    "username": "admin",
    "role": "admin",
    "fullname": "Mrs Admin",
    "email": "none@none.com",
    "password": "admin",
}

record["password"] = ctx.hash(record["password"])

if update_user_record_db(record):
    print("OK")
else:
    print("Record not inserted")
