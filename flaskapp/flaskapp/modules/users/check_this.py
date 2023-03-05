#!/usr/bin/env python3
from passlib.context import CryptContext
import sys

def validate_password(password, encrypted_p) -> bool:
    ctx = CryptContext(
        schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=14
    )
    if ctx.verify(password, encrypted_p):
        return True
    else:
        return False


if len(sys.argv) == 3:
    password = sys.argv[1]
    encrypted_p = sys.argv[2]
else:
    myinput: str = sys.stdin.readline()
    password, encrypted_p = myinput.split()

print ( f'validating {password} {encrypted_p}')

if validate_password(password, encrypted_p):
    print("yes they match")
else:
    print("No Match")

sys.exit()
