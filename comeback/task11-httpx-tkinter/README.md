# Task 11 — httpx + Semáforos + Interfaz Tkinter

Evolución de la tarea 10: misma lógica de exploración concurrente con `httpx` y `asyncio.Semaphore`, pero con una interfaz gráfica en `tkinter` que muestra el estado de cada URL en tiempo real.

## Requerimientos

- Python 3.10+
- `httpx`
- `tkinter` (incluido en la mayoría de instalaciones de Python)

```bash
pip install httpx
```

## Ejecución

```bash
cd comeback/task11-httpx-tkinter
python3 httpx_tkinter.py
```

## Archivo de URLs

Edita `urls.txt` con las URLs a explorar (una por línea, `#` para comentarios).

## Descripción del programa

| Componente | Descripción |
|------------|-------------|
| `ttk.Treeview` | Tabla que muestra URL, estado visual y código HTTP |
| `asyncio.Semaphore(3)` | Máximo 3 peticiones simultáneas (zona crítica) |
| `threading.Thread` | Hilo separado para correr el loop asyncio sin bloquear la GUI |
| `tree.after(0, ...)` | Actualiza la tabla desde el hilo de red de forma segura |
| Botón "▶ Escanear" | Se desactiva durante el escaneo y se reactiva al terminar |

## Estados visuales en la tabla

| Ícono | Color | Significado |
|-------|-------|-------------|
| ⏸ Pendiente | ⚫ Gris | En espera de ser procesada |
| ⏳ En curso… | 🔵 Azul | Petición activa (dentro del semáforo) |
| ✅ 200 | 🟢 Verde | Respuesta exitosa (HTTP < 400) |
| ⚠️ 404 | 🟠 Naranja | Respuesta con error HTTP (≥ 400) |
| ❌ Error | 🔴 Rojo | Error de red / timeout / DNS |
