import os
import socket

def serve_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def serve_image(filename):
    with open(filename, 'rb') as file:
        content = file.read()
    return content

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 80))
    server_socket.listen(1)

    print("Server is running ")

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode() # client requesting

        if data:#used for continous listening from client request
            if data.startswith('GET /'):# translate from the client request in the search bar like http://127.0.0.1/index.html
                filename = data.split()[1][1:] # get the filename NAME in this one its the index.html
                if filename.endswith('.html'):
                    if os.path.isfile(filename):#check if file exist or not
                        content = serve_file(filename)
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{content}"
                    else:
                        response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>File not found</h1>"
                elif filename.endswith('.jpg'):
                    if os.path.isfile(filename):
                        content = serve_image(filename)
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n"
                        client_socket.sendall(response.encode() + content)
                    else:
                        response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>File not found</h1>"
                else:
                    response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>File not found</h1>"

                client_socket.sendall(response.encode())

        client_socket.close()

if __name__ == "__main__":
    run_server()
