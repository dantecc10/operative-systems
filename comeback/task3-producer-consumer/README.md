# Task 3 — Productor y Consumidor con Corrutinas

Simulación del modelo productor-consumidor usando `asyncio`. Los productores generan ítems y los colocan en una cola compartida; los consumidores los extraen y procesan. La zona crítica se protege con un `asyncio.Lock` y cada trabajador imprime en un color diferente.

## Requerimientos

- Python 3.10+
- Sin dependencias externas (`asyncio` es de la librería estándar)

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `producer_consumer.py` | Versión base: 3 productores, 2 consumidores |
| `alt_producer_consumer.py` | Versión extendida: agrega un monitor de cola con barra visual |

## Ejecución

```bash
cd comeback/task3-producer-consumer

# Versión base
python3 producer_consumer.py

# Versión con monitor
python3 alt_producer_consumer.py
```

## Descripción del programa

| Componente | Descripción |
|------------|-------------|
| `asyncio.Queue(maxsize=10)` | Cola compartida con capacidad limitada |
| `asyncio.Lock` | Candado que protege la zona crítica (put/get + print) |
| `productor(id, cola, cerrojo)` | Corrutina que produce 5–7 ítems con retraso aleatorio |
| `consumidor(id, cola, cerrojo)` | Corrutina que consume ítems indefinidamente hasta cancelarse |
| `asyncio.gather(*productores)` | Espera a que todos los productores terminen |
| `cola.join()` | Espera a que todos los ítems sean procesados |
| `tarea.cancel()` | Cancela los consumidores al vaciar la cola |

## Versión extendida (`alt_producer_consumer.py`)

Añade una corrutina `monitor(cola)` que imprime periódicamente el estado de la cola con una barra visual:

```
[MONITOR] Capacidad: [████----] (4/10)
```

Cada trabajador tiene su propio color ANSI único para distinguirlos en la salida.

## Colores en la terminal

| Trabajador | Color |
|------------|-------|
| Productores (0–2) | 🔵 Azul / Cian |
| Consumidores (0–1) | 🟢 Verde |
| Monitor | 🟡 Amarillo |
