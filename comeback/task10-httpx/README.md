# Task 10 — Exploración Concurrente de URLs con httpx y Semáforos

Programa de línea de comandos que lee una lista de URLs desde `urls.txt` y las consulta de forma concurrente usando `httpx` asíncrono. La concurrencia máxima se controla mediante `asyncio.Semaphore`.

## Requerimientos

- Python 3.10+
- `httpx`

```bash
pip install httpx
```

## Ejecución

```bash
cd comeback/task10-httpx
python3 httpx_semaphores.py
```

## Archivo de URLs

Edita `urls.txt` para agregar las URLs que quieras explorar (una por línea). Las líneas que empiecen con `#` se ignoran.

```
https://example.com
https://python.org
# Esta línea es un comentario
https://github.com
```

## Descripción del programa

| Componente | Descripción |
|------------|-------------|
| `asyncio.Semaphore(3)` | Zona crítica: máximo 3 peticiones simultáneas |
| `fetch()` | Corrutina que adquiere el semáforo, realiza la petición y libera |
| `asyncio.gather()` | Lanza todas las tareas concurrentemente respetando el semáforo |
| Timeout | 10 segundos por petición |

## Salida esperada

```
[200] https://example.com
[200] https://python.org
[ERR] https://nonexistent.invalid — ...
[404] https://httpbin.org/status/404
```

| Color | Significado |
|-------|-------------|
| 🟢 Verde | Código HTTP < 400 |
| 🟡 Amarillo | Código HTTP ≥ 400 |
| 🔴 Rojo | Error de conexión / timeout |
