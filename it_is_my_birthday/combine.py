with open("shattered-2.pdf", "rb") as f:
    pdf_data = f.read()

with open("invite-bytes", "rb") as f:
    payload = f.read()

with open("sha1-B.pdf", "wb") as f:
    f.write(pdf_data + payload)
