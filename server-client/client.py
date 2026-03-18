import socket
host = socket.gethostname()
port = 2026

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    mensaje = input("Ingrese un mensaje para enviar al servidor: ")
    