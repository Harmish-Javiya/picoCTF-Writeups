from pwn import *
from pathlib import Path
import sys

HOST = "chatelaine.cylabacademy.net"  # Your authorized test server
PORT = 10097
CREDS_FILE = Path(__file__).resolve().parent / "creds-dump.txt"
FAIL_STRING = b"Invalid username or password"

def load_credentials():
    if not CREDS_FILE.is_file():
        raise FileNotFoundError(
            f"Credential file not found: {CREDS_FILE}"
        )

    credentials = []
    skipped = 0

    with CREDS_FILE.open(
        "r", encoding="utf-8", errors="replace"
    ) as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or ";" not in line:
                skipped += 1
                continue

            username, password = line.split(";", 1)
            username = username.strip()
            password = password.strip()

            if username and password:
                credentials.append((username, password))
            else:
                skipped += 1

    return credentials, skipped


def main():
    try:
        credentials, skipped = load_credentials()
    except OSError as exc:
        print(f"Error reading credentials: {exc}")
        sys.exit(1)

    print(f"Credential file: {CREDS_FILE}")
    print(f"Loaded pairs: {len(credentials)}")
    print(f"Skipped lines: {skipped}")

    if credentials:
        print("\nFirst pair format check: passed")
        print("Credentials hidden for safety.")


if __name__ == "__main__":
    main()

