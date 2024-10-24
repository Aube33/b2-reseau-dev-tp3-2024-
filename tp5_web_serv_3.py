import socket
import re
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()

HTML_MODELS = "./htdocs/"

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

            # Petite route de base pour faire joli
            if request == "/":
                request = "/index"

            if not ".html" in request:
                request+=".html"

            request = request[1:]
            if os.path.isfile(f'{HTML_MODELS}/{request}'):
                file = open(f'{HTML_MODELS}/{request}')
                html_content = file.read()
                file.close()

                response = "HTTP/1.0 200 OK\n\n" + html_content
            else:
                response = "HTTP/1.0 404 Not Found\n\n<h1>Page non trouvée</h1>"
        else:
            response = "HTTP/1.0 400 Bad Request\n\n<h1>Mauvaise requête</h1>"

        client.send(response.encode("UTF-8"))
        break
    client.close()
sock.close()