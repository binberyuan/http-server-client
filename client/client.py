import socket

SERVER_ADDRESS = ('localhost', 8000)

def request_profile_picture():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDRESS)
        request = b"GET /profile.jpg HTTP/1.1\r\nHost: localhost:8000\r\n\r\n"
        client_socket.sendall(request)
        response = client_socket.recv(1024)
        status_line, headers, *body = response.split(b"\r\n")
        if status_line.startswith(b"HTTP/1.1 200"):
            with open("profile.jpg", "wb") as f:
                f.write(b"\r\n".join(body))
            print("Profile picture saved to profile.jpg")
        else:
            print(f"Error: {status_line}")

if __name__ == "__main__":
    request_profile_picture()
