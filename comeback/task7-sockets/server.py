"""
Task 7: Chat Servidor — acepta múltiples clientes con hilos.
Uso: python server.py
"""
import socket
import threading

HOST = socket.gethostname()
PORT = 2026


def handle_client(conn: socket.socket, addr: tuple):
    print(f"[+] Conectado: {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode()
                print(f"\n[{addr[0]}] → {msg}")
                respuesta = input("Tú → ")
                conn.sendall(respuesta.encode())
            except (ConnectionResetError, BrokenPipeError):
                break
    print(f"[-] Desconectado: {addr}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor de chat escuchando en {HOST}:{PORT}\n")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
