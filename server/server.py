import socket

# Define the host and port for the server
HOST = 'localhost'
PORT = 6617 # port number

# Define the file paths for index.html, pic1.jpg, pic2.jpg, and favicon.ico
HTML_FILE_PATH = 'index.html'
JPG_FILE_PATHS = ['profile.jpg','pic1.jpeg', 'pic2.jpeg']
FAVICON_FILE_PATH = 'favicon.ico'

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f'Server is running on http://{HOST}:{PORT}/')
print(f'Server is listening on {HOST}:{PORT}...')
while True:
    # Accept incoming connection from a client
    connection, address = server_socket.accept()

    # Receive the HTTP request from the client
    request = connection.recv(1024).decode('utf-8')
    print(f'Received request from {address}: {request}')
    # print(request)
    if request:
        # Parse the requested object name from the HTTP request
        requested_object = request.split()[1]
        # print("requested_object: ", requested_object)
        # Serve the requested object based on its file extension
        if requested_object == '/':
            # Serve the index.html file
            with open(HTML_FILE_PATH, 'r') as file:
                response = file.read()
            # Send the HTTP response with proper headers
            headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
            connection.sendall((headers + response).encode('utf-8'))
        elif requested_object == '/index.html':
            # Serve the index.html file
            with open(HTML_FILE_PATH, 'r') as file:
                response = file.read()
            # Send the HTTP response with proper headers
            headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
            connection.sendall((headers + response).encode('utf-8'))
        elif requested_object.endswith('.jpeg') or requested_object.endswith('.jpg'):
            # Serve the requested images file
            if requested_object[1:] in JPG_FILE_PATHS:
                with open(requested_object[1:], 'rb') as file:
                    response = file.read()
                headers = 'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n'
                # print("len of response: ", len(response))
                connection.sendall(headers.encode('utf-8') + response)
            else:
                # Send a 404 response if the requested JPG file is not found
                response = 'HTTP/1.1 404 Not Found\r\n\r\n'
                connection.sendall(response.encode('utf-8'))
        elif requested_object == '/favicon.ico':
            # Serve the dummy favicon.ico file
            with open(FAVICON_FILE_PATH, 'rb') as file:
                response = file.read()
            headers = 'HTTP/1.1 200 OK\r\nContent-Type: image/x-icon\r\n\r\n'
            connection.sendall(headers.encode('utf-8') + response)
        else:
            # Send a 404 response for any other requested object
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            connection.sendall(response.encode('utf-8'))
    else:
        response = 'HTTP/1.1 400 Bad Request\r\n\r\nBad Request'
        connection.sendall(response.encode('utf-8'))

    # Close the connection
    connection.close()

