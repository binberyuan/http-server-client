from socket import *
import re
import os

def get_html(server_name, server_port):
    """
    Get HTML content from a server.

    Args:
        server_name (str): Server hostname or IP address.
        server_port (int): Server port number.

    Returns:
        str: HTML content.
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    request = f'GET /index.html HTTP/1.0\r\nHost: {server_name}\r\n\r\n'
    client_socket.send(request.encode())
    response = client_socket.recv(4096)
    html = response.decode()
    client_socket.close()
    return html

def extract_imgs(html):
    """
    Extract image path from HTML content.

    Args:
        html (str): HTML content.

    Returns:
       Lists of image paths.
    """
    img_regex = re.compile(r'<a.*?href=["\']?(.*?)["\']?>')
    img_names = re.findall(img_regex, html)

    return img_names

def download_files(paths, server_port):
    """
    Download files from given links.

    Args:
        paths (list): List of file URLs.
        server_port (int): Server port number.
    """
    print(paths)
    for path in paths:
        if path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.png'):

            hostname = '127.0.0.1'

            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((hostname, server_port))
            request = f'GET /{path} HTTP/1.0\r\nHost: {hostname}\r\n\r\n'
            client_socket.send(request.encode())

            response = b''
            headers_received = False
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                if not headers_received:
                    # Get rid of the Headers
                    data = data.split(b'\r\n\r\n', 1)[1]
                    headers_received = True
                response += data

            filename = os.path.basename(path)
            with open(filename, 'wb') as f:
                f.write(response)
            print(f'Saved {filename} successfully.')

            client_socket.close()

server_name = 'localhost'
server_port = 6617

html = get_html(server_name, server_port)
img_links = extract_imgs(html)

download_files(img_links , server_port)

print('Request successful.')
