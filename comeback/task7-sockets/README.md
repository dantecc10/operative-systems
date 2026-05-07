# Task 7 — Chat Cliente-Servidor con Sockets

Sistema de chat bidireccional entre dos computadoras usando sockets TCP. El servidor acepta múltiples clientes mediante hilos y permite una conversación de turno a turno.

## Requerimientos

- Python 3.10+
- Sin dependencias externas (`socket` y `threading` son de la librería estándar)

## Ejecución

Abre **dos terminales**:

```bash
# Terminal 1 — Servidor
cd comeback/task7-sockets
python3 server.py
```

```bash
# Terminal 2 — Cliente
cd comeback/task7-sockets
python3 client.py
```

> Para conectarte desde otra computadora, cambia `HOST = socket.gethostname()` por la IP de la máquina servidora en ambos archivos.

## Descripción del programa

### `server.py`
| Componente | Descripción |
|------------|-------------|
| `socket.bind()` | Escucha en el hostname de la máquina, puerto `2026` |
| `handle_client()` | Hilo dedicado por cliente: recibe mensaje → imprime → responde |
| `SO_REUSEADDR` | Permite reutilizar el puerto inmediatamente tras cerrar el servidor |

### `client.py`
| Componente | Descripción |
|------------|-------------|
| `socket.connect()` | Se conecta al servidor en el mismo host y puerto `2026` |
| Bucle principal | Lee input del usuario → envía → espera respuesta del servidor |

## Puerto utilizado
`2026` (TCP)
