#!/usr/bin/env python3
from passlib.context import CryptContext
import sys

ctx = CryptContext(
    schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=14
)
if len(sys.argv) == 2:
    password = sys.argv[1]
else:
    print("enter a password string :", end="", flush=True)
    password = sys.stdin.readline()
print(ctx.hash(password))
sys.exit()
