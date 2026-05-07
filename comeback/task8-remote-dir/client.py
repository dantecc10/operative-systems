"""
Task 8: Cliente — solicita listado de directorio al servidor remoto.
Uso: python client.py
"""
import socket

HOST = socket.gethostname()
PORT = 2027

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Conectado a {HOST}:{PORT}")
    print("Ingresa una ruta absoluta del servidor para listar su contenido.\n")
    while True:
        try:
            ruta = input("Ruta → ").strip()
            if not ruta:
                continue
            s.sendall(ruta.encode())
            respuesta = s.recv(65536).decode()
            print("─" * 40)
            print(respuesta)
        except KeyboardInterrupt:
            print("\nDesconectado.")
            break
