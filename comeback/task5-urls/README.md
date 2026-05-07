# Task 5 — Visualización de URLs en Tiempo Real

Similar a la tarea 4 pero orientado a **hostnames/URLs**. El programa resuelve cada IP foránea a su nombre de dominio usando DNS inverso y verifica si el dominio aparece en una blacklist. Los dominios bloqueados se muestran en rojo.

## Requerimientos

- Python 3.10+
- `tkinter` (incluido en la mayoría de instalaciones de Python)
- `netstat` disponible en el sistema

```bash
# En caso de no tener netstat (Linux):
sudo apt install net-tools
```

> **Nota:** La blacklist integrada es un subconjunto representativo. Para usar la lista completa referenciada en la tarea, descarga los dominios de [fabriziosalmi/blacklists](https://github.com/fabriziosalmi/blacklists) y agrégalos al set `BLACKLIST` en el código.

## Ejecución

```bash
cd comeback/task5-urls
python3 url_monitor.py
```

## Descripción del programa

| Componente | Descripción |
|------------|-------------|
| `resolve_ip()` | Convierte IP → hostname con `socket.gethostbyaddr()` |
| `is_blocked()` | Comprueba si el hostname o algún subdominio está en `BLACKLIST` |
| `_cache` | Diccionario en memoria para no resolver la misma IP dos veces |
| `App` (tkinter) | Tabla con refresco cada 3 segundos mediante hilo daemon |

### Colores de la tabla
| Color | Significado |
|-------|-------------|
| 🟢 Verde | Dominio no bloqueado |
| 🔴 Rojo | Dominio en blacklist |
| ⚫ Gris | Sin IP identificable |
