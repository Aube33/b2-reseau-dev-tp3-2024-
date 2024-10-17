import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

def is_calcul(value: str):
    return re.search(r'^(-?\d+)\s*[\+\-\*]\s*(-?\d+)$', value)

def check_under_4bytes(l:list):
    return 0==len([int(x) for x in l if int(x) >= 4294967295])

msg = input("Calcul à envoyer: ")
if not is_calcul(msg):
    raise ValueError("Mauvais calcul")

values = re.split(r"\s*[\+\-\*]\s*", msg)
if not check_under_4bytes(values):
    raise ValueError("Valeur trop grande")

msg += "<clafin>"
encoded_msg = msg.encode('utf-8')

msg_len = len(encoded_msg)
header = msg_len.to_bytes(4, byteorder='big')
payload = header + encoded_msg

print(payload)

s.send(payload)

s_data = s.recv(1024)
print(s_data.decode())
s.close()
