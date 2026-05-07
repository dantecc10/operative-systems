# Task 13 — Primitivas de Sincronización de Procesos

Implementación y demostración de las principales primitivas de sincronización del módulo `threading` de Python. Cada primitiva incluye prints que identifican claramente la sección crítica y el flujo de ejecución.

## Requerimientos

- Python 3.10+
- Sin dependencias externas (`threading` es de la librería estándar)
- Para visualizar los diagramas Mermaid en `hilos.md`: VS Code con la extensión [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)

## Ejecución

```bash
cd comeback/task13-sync
python3 controlZC.py
```

## Primitivas implementadas

| # | Primitiva | Clase Python | Descripción |
|---|-----------|--------------|-------------|
| 1 | **Lock** | `threading.Lock` | Exclusión mutua — solo 1 hilo a la vez en la sección crítica |
| 2 | **RLock** | `threading.RLock` | Lock re-entrante — el mismo hilo puede adquirirlo múltiples veces |
| 3 | **Semaphore** | `threading.Semaphore` | Permite hasta N hilos simultáneos en la sección crítica |
| 4 | **Event** | `threading.Event` | Señal de arranque: hilos esperan hasta que otro llame `event.set()` |
| 5 | **Condition** | `threading.Condition` | Combina lock + `wait`/`notify` para el patrón productor-consumidor |
| 6 | **Barrier** | `threading.Barrier` | Punto de encuentro: todos los hilos esperan antes de continuar |

> `BoundedSemaphore` fue omitido según las instrucciones de la tarea.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `controlZC.py` | Código con las 6 demos ejecutables |
| `hilos.md` | Documentación con diagramas de flujo en sintaxis **Mermaid** para cada primitiva |

## Estructura de cada demo

```
[Nombre primitiva] descripción
─────────────────────────────────────────────
  Hilo-N: intentando entrar a la SECCIÓN CRÍTICA…
  Hilo-N: ──► DENTRO  (datos relevantes)
  Hilo-N: ◄── SALIENDO
```
