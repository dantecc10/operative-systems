# Task 8 — Lectura Remota de Directorios con Sockets

Par cliente/servidor que permite explorar el sistema de archivos de una máquina remota. El cliente envía una ruta absoluta y el servidor responde con el contenido del directorio indicando si cada entrada es un archivo o carpeta.

## Requerimientos

- Python 3.10+
- Sin dependencias externas (`socket`, `os`, `threading` son de la librería estándar)

## Ejecución

Abre **dos terminales**:

```bash
# Terminal 1 — Servidor
cd comeback/task8-remote-dir
python3 server.py
```

```bash
# Terminal 2 — Cliente
cd comeback/task8-remote-dir
python3 client.py
```

Una vez conectado, escribe rutas absolutas para explorarlas:

```
Ruta → /home
Ruta → /tmp
Ruta → /etc
```

> Para conectarte desde otra máquina, cambia `HOST` por la IP del servidor en `client.py`.

## Descripción del programa

### `server.py`
| Componente | Descripción |
|------------|-------------|
| Puerto `2027` | Puerto TCP diferente al del chat (tarea 7) |
| `handle_client()` | Recibe ruta → valida con `os.path.isdir()` → lista con `os.listdir()` |
| Formato respuesta | `[DIR ] nombre` o `[FILE] nombre` por cada entrada |
| Manejo de errores | Responde con mensaje si la ruta no existe o no hay permisos |

### `client.py`
| Componente | Descripción |
|------------|-------------|
| Bucle principal | Solicita rutas al usuario e imprime la respuesta del servidor |
| Buffer de recepción | `65536` bytes para soportar directorios con muchas entradas |

## Puerto utilizado
`2027` (TCP)
