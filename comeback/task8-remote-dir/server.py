"""
Task 8: Servidor — expone el sistema de archivos local vía sockets.
Uso: python server.py
"""
import os
import socket
import threading

HOST = socket.gethostname()
PORT = 2027


def handle_client(conn: socket.socket, addr: tuple):
    print(f"[+] Conectado: {addr}")
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            ruta = data.decode().strip()
            if not os.path.isdir(ruta):
                respuesta = f"ERROR: '{ruta}' no es un directorio válido.\n"
            else:
                try:
                    entradas = sorted(os.listdir(ruta))
                    lineas = []
                    for e in entradas:
                        full = os.path.join(ruta, e)
                        tipo = "DIR " if os.path.isdir(full) else "FILE"
                        lineas.append(f"  [{tipo}] {e}")
                    respuesta = (
                        "\n".join(lineas) + "\n"
                        if lineas else "(directorio vacío)\n"
                    )
                except PermissionError:
                    respuesta = "ERROR: Sin permisos para leer ese directorio.\n"
            conn.sendall(respuesta.encode())
    print(f"[-] Desconectado: {addr}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor de directorios en {HOST}:{PORT}\n")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
