import socket
import re

#creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("mysterious-sea.picoctf.net", 58773))

buffer = b""
rounds = 0

while rounds < 20:
	chunk = s.recv(4096)
	
	if not chunk:
		break
	
	buffer += chunk
	
	text = buffer.decode(errors = "ignore")
	
	lines = text.split("\n")

	for line in lines:
		if re.fullmatch(r"\d+",line) and len(line) < 11:
			print(f"[Round {rounds + 1}] Number:",line)
			
			s.send((line + "\n").encode())
			
			rounds += 1
			buffer = b""
			break


while True:
	data = s.recv(4096)
	
	if not data:
		break

	print(data.decode(errors="ignore"),end = "")

s.close()


