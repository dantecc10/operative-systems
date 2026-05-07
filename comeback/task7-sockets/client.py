"""
Task 7: Chat Cliente
Uso: python client.py
"""
import socket

HOST = socket.gethostname()
PORT = 2026

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Conectado a {HOST}:{PORT}. Escribe tus mensajes (CTRL+C para salir).\n")
    while True:
        try:
            mensaje = input("Tú → ")
            s.sendall(mensaje.encode())
            respuesta = s.recv(1024).decode()
            print(f"Servidor → {respuesta}\n")
        except (KeyboardInterrupt, BrokenPipeError):
            print("\nDesconectado.")
            break
