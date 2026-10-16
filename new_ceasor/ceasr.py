import string

ALPHABET = string.ascii_lowercase[:16]

def unshift(c, k):
    t1 = ord(c) - ord('a')
    t2 = ord(k) - ord('a')
    return ALPHABET[(t1 - t2) % 16]

def b16_decode(enc):
    res = ""
    for i in range(0, len(enc), 2):
        high = ALPHABET.index(enc[i])
        low = ALPHABET.index(enc[i+1])
        byte = (high << 4) | low
        res += chr(byte)
    return res

cipher = "fegdeogdgecoeocgcgchcfcffccfca"

for k in ALPHABET:
    shifted = "".join(unshift(c, k) for c in cipher)
    try:
        decoded = b16_decode(shifted)
        if "picoCTF" in decoded:
            print("KEY:", k)
            print("FLAG:", decoded)
    except:
        pass
