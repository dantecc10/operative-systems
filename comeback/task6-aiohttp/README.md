# Task 6 — Ejecución de Comandos Bash vía aiohttp

Servidor web asíncrono construido con `aiohttp` que expone una interfaz HTML para ejecutar comandos de bash de forma remota. Utiliza `subprocess` (equivalente a `os.system`) para correr los comandos y devuelve la salida en el navegador.

## Requerimientos

- Python 3.10+
- `aiohttp`

```bash
pip install aiohttp
```

## Ejecución

```bash
cd comeback/task6-aiohttp
python3 aiohttp_bash.py
```

Luego abre en tu navegador:

```
http://127.0.0.1:8080
```

## Rutas del servidor

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET`  | `/`      | Formulario para ingresar un comando |
| `POST` | `/run`   | Ejecuta el comando y devuelve la salida |

## Descripción del programa

| Componente | Descripción |
|------------|-------------|
| `index()` | Sirve el formulario HTML con estilo tipo terminal |
| `run_command()` | Recibe el comando vía POST, lo ejecuta con `subprocess.run(shell=True)` y devuelve stdout/stderr |
| Timeout | Los comandos tienen un límite de **10 segundos** de ejecución |

> ⚠️ **Advertencia de seguridad:** Este servidor ejecuta comandos arbitrarios. Úsalo únicamente en entornos locales/controlados.
