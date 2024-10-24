import socket
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()

print("Serveur lancé")

while True:
    client, client_addr = sock.accept()    
    while True:
        data = client.recv(1024).decode("utf-8")
        if not data:
            break

        response = ""
        extractGet = re.search(r"(?<=GET\s)\/?\S+", data)
        if extractGet:
            request = extractGet.group(0)
            if request == "/":
                response = "HTTP/1.0 200 OK\n\n<h1>Bienvenue sur la page d'accueil</h1>"
            elif request == "/login":
                response = "HTTP/1.0 200 OK\n\n<p>C'est l'heure de se connecter</p>"
            elif request == "/robots.txt":
                response = "HTTP/1.0 200 OK\n\nbip\nbip\nbip..."
        else:
            response = "HTTP/1.0 404 Not Found\n\n<h1>Page non trouvée</h1>"

        client.send(response.encode())
        break
    client.close()
sock.close()