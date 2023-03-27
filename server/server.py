import socket

PORT = 8000
SERVER_ADDRESS = ('localhost', PORT)


def serve_forever():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen(1)
        print(f"Server is listening on port {PORT}...")
        while True:
            client_socket, client_address = server_socket.accept()
            request = client_socket.recv(1024)
            response = handle_request(request)
            client_socket.sendall(response)
            client_socket.close()


def handle_request(request):
    # Parse the request method, path, and headers
    method, path, *headers = request.split(b"\r\n")

    # Only respond to GET requests for the root path "/"
    if method != b"GET" or path != b"/":
        return generate_response(404, b"Not Found", b"")

    # Load the HTML file and the images
    with open("index.html", "rb") as f:
        html = f.read()
    with open("profile.jpg", "rb") as f:
        profile_image = f.read()
    with open("image1.jpg", "rb") as f:
        image1 = f.read()
    with open("image2.jpg", "rb") as f:
        image2 = f.read()

    # Generate the response headers and body
    headers = [
        b"HTTP/1.1 200 OK",
        b"Content-Type: text/html",
        f"Content-Length: {len(html) + len(profile_image) + len(image1) + len(image2)}".encode(),
        b""
    ]
    body = html + profile_image + image1 + image2

    return b"\r\n".join(headers) + body


def generate_response(status_code, status_text, body):
    headers = [
        f"HTTP/1.1 {status_code} {status_text}",
        b"Content-Type: text/plain",
        f"Content-Length: {len(body)}".encode(),
        b""
    ]
    return b"\r\n".join(headers) + body


if __name__ == "__main__":
    serve_forever()
