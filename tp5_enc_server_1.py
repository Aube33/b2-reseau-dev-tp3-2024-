import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()
client, client_addr = sock.accept()

FOOTER = 0

while True:
    header = client.recv(4)
    if not header:
        break

    msg_len = int.from_bytes(header[0:4], byteorder='big')

    print(f"Lecture des {msg_len} prochains octets")

    chunks = []

    bytes_received = 0
    while bytes_received < msg_len:
        chunk = client.recv(min(msg_len - bytes_received, 1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')

        chunks.append(chunk)

        bytes_received += len(chunk)

    message_received = b"".join(chunks).decode('utf-8')
    footer_msg = client.recv(1)
    footer_data = int.from_bytes(footer_msg, byteorder='big')

    if FOOTER == footer_data:
        print(f"Received from client {message_received}")
    else:
        print("Aucun séquence de fin trouvée")

client.close()
sock.close()