import asyncio
import random

# Diccionario de colores para identificar a cada trabajador de forma única
COLORES = {
    "P0": "\033[94m", "P1": "\033[34m", "P2": "\033[36m",  # Azules/Cian
    "C0": "\033[92m", "C1": "\033[32m",                  # Verdes
    "MON": "\033[93m",                                   # Amarillo (Monitor)
    "RESET": "\033[0m"
}

async def monitor(cola):
    """Corrutina que observa el estado de la cola periódicamente."""
    while True:
        size = cola.qsize()
        # Creamos una "barra de carga" visual para la cola
        barra = "█" * size + "-" * (cola.maxsize - size)
        print(f"{COLORES['MON']}[MONITOR] Capacidad: [{barra}] ({size}/{cola.maxsize}){COLORES['RESET']}")
        await asyncio.sleep(0.8)

async def productor(id, cola, cerrojo):
    color = COLORES.get(f"P{id}", COLORES["RESET"])
    for i in range(7): # Producen 7 items cada uno
        await asyncio.sleep(random.uniform(0.1, 0.4))
        item = f"Dato-{id}-{i}"
        
        # Bloqueamos la zona crítica para asegurar consistencia en el print y el put
        async with cerrojo:
            await cola.put(item)
            print(f"{color}Productor {id}: [+] Agregué {item} {COLORES['RESET']}")

async def consumidor(id, cola, cerrojo):
    color = COLORES.get(f"C{id}", COLORES["RESET"])
    while True:
        await asyncio.sleep(random.uniform(0.6, 1.2)) # Consumen más lento
        
        async with cerrojo:
            item = await cola.get()
            print(f"{color}Consumidor {id}: [-] Procesé {item} {COLORES['RESET']}")
            cola.task_done()

async def main():
    cola = asyncio.Queue(maxsize=10)
    cerrojo = asyncio.Lock()

    # Lanzar el monitor como tarea de fondo (daemon-like)
    tarea_monitor = asyncio.create_task(monitor(cola))

    # Crear trabajadores
    productores = [asyncio.create_task(productor(i, cola, cerrojo)) for i in range(3)]
    consumidores = [asyncio.create_task(consumidor(i, cola, cerrojo)) for i in range(2)]

    # Esperar a que la producción termine y la cola se vacíe
    await asyncio.gather(*productores)
    await cola.join()

    # Limpieza: Cancelamos las tareas que corren indefinidamente
    tarea_monitor.cancel()
    for c in consumidores:
        c.cancel()

    print(f"\n{COLORES['MON']}--- Simulación completada con éxito ---{COLORES['RESET']}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
