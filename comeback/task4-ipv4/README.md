# Task 4 — Visualización de IPv4 en Tiempo Real

Lee las conexiones de red activas usando `netstat` y las muestra en una tabla gráfica con `tkinter`, actualizándose cada 2 segundos. Las IPs privadas se muestran en gris, las públicas válidas en verde y las no reconocibles en rojo.

## Requerimientos

- Python 3.10+
- `tkinter` (incluido en la mayoría de instalaciones de Python)
- `netstat` disponible en el sistema

```bash
# En caso de no tener netstat (Linux):
sudo apt install net-tools
```

## Ejecución

```bash
cd comeback/task4-ipv4
python3 ipv4_monitor.py
```

## Descripción del programa

| Componente | Descripción |
|------------|-------------|
| `parse_netstat()` | Ejecuta `netstat -n` y extrae filas de conexiones TCP/UDP |
| `extract_ip()` | Obtiene la IP de la columna *foreign address* |
| `is_private()` | Verifica si la IP pertenece a rangos privados/reservados |
| `App` (tkinter) | Ventana con tabla `ttk.Treeview` que se refresca con un hilo daemon |

### Rangos marcados como privados
`10.x.x.x` · `172.16–31.x.x` · `192.168.x.x` · `127.x.x.x` · `169.254.x.x` · `0.0.0.0`

### Colores de la tabla
| Color | Significado |
|-------|-------------|
| 🟢 Verde | IP pública válida |
| ⚫ Gris | IP privada / reservada |
| 🔴 Rojo | IP con formato inválido |
