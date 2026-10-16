ecode = "235a201d702015483b1d412b265d3313501f0c072d135f0d2002302d07466656764b06422e"
decode = bytes.fromhex(ecode)

decoded = ""
secret = "S3Cr3t"

for i in range(len(decode)):
	key = ord(secret[i % 6])
	a = key ^ decode[i]
	decoded += chr(a) 

print(decoded)



