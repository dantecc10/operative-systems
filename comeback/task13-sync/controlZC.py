"""
Task 13: Primitivas de Sincronización de Procesos
Ejemplos de: Lock, RLock, Semaphore, Event, Condition, Barrier.
Cada función imprime claramente la sección crítica y el flujo de control.
"""
import threading
import time

SEP = "─" * 52


# ──────────────────────────────────────────────────────
# 1. Lock — exclusión mutua básica
# ──────────────────────────────────────────────────────
def demo_lock():
    print(f"\n{SEP}\n[Lock] Exclusión mutua básica\n{SEP}")
    lock = threading.Lock()
    contador = [0]

    def tarea(id):
        for _ in range(3):
            print(f"  Hilo-{id}: intentando entrar a la SECCIÓN CRÍTICA…")
            with lock:                          # adquiere el lock
                print(f"  Hilo-{id}: ──► DENTRO  contador={contador[0]}")
                contador[0] += 1
                time.sleep(0.05)
                print(f"  Hilo-{id}: ◄── SALIENDO contador={contador[0]}")

    hilos = [threading.Thread(target=tarea, args=(i,)) for i in range(2)]
    for h in hilos: h.start()
    for h in hilos: h.join()


# ──────────────────────────────────────────────────────
# 2. RLock — Lock re-entrante (mismo hilo puede re-adquirir)
# ──────────────────────────────────────────────────────
def demo_rlock():
    print(f"\n{SEP}\n[RLock] Lock re-entrante\n{SEP}")
    rlock = threading.RLock()

    def externa(id):
        with rlock:
            print(f"  Hilo-{id}: SECCIÓN CRÍTICA nivel 1")
            interna(id)             # mismo hilo vuelve a adquirir sin deadlock

    def interna(id):
        with rlock:
            print(f"  Hilo-{id}: SECCIÓN CRÍTICA nivel 2 (re-entrante)")
            time.sleep(0.05)

    hilos = [threading.Thread(target=externa, args=(i,)) for i in range(2)]
    for h in hilos: h.start()
    for h in hilos: h.join()


# ──────────────────────────────────────────────────────
# 3. Semaphore — máximo N hilos en la sección crítica
# ──────────────────────────────────────────────────────
def demo_semaphore():
    print(f"\n{SEP}\n[Semaphore] Máx. 2 hilos simultáneos en sección crítica\n{SEP}")
    sem = threading.Semaphore(2)

    def tarea(id):
        print(f"  Hilo-{id}: esperando permiso del semáforo…")
        with sem:
            print(f"  Hilo-{id}: ──► DENTRO (zona crítica, máx 2 concurrentes)")
            time.sleep(0.2)
        print(f"  Hilo-{id}: ◄── salió")

    hilos = [threading.Thread(target=tarea, args=(i,)) for i in range(5)]
    for h in hilos: h.start()
    for h in hilos: h.join()


# ──────────────────────────────────────────────────────
# 4. Event — señalización entre hilos
# ──────────────────────────────────────────────────────
def demo_event():
    print(f"\n{SEP}\n[Event] Señalización entre hilos\n{SEP}")
    evento = threading.Event()

    def trabajador(id):
        print(f"  Hilo-{id}: bloqueado — esperando la señal…")
        evento.wait()               # bloquea hasta event.set()
        print(f"  Hilo-{id}: ¡señal recibida! ejecutando tarea")

    def disparador():
        time.sleep(0.3)
        print("  [Disparador]: ¡Enviando señal a todos los hilos!")
        evento.set()

    hilos = [threading.Thread(target=trabajador, args=(i,)) for i in range(3)]
    for h in hilos: h.start()
    threading.Thread(target=disparador).start()
    for h in hilos: h.join()


# ──────────────────────────────────────────────────────
# 5. Condition — esperar/notificar con condición compartida
# ──────────────────────────────────────────────────────
def demo_condition():
    print(f"\n{SEP}\n[Condition] Productor–Consumidor con notificación\n{SEP}")
    cond  = threading.Condition()
    items: list[int] = []

    def productor():
        for i in range(3):
            time.sleep(0.2)
            with cond:
                items.append(i)
                print(f"  [Productor] Produjo ítem {i}  →  notificando al consumidor…")
                cond.notify()

    def consumidor():
        for _ in range(3):
            with cond:
                while not items:
                    print("  [Consumidor] Cola vacía — esperando…")
                    cond.wait()     # libera el lock y bloquea hasta notify()
                item = items.pop(0)
                print(f"  [Consumidor] Consumió ítem {item}")

    p = threading.Thread(target=productor)
    c = threading.Thread(target=consumidor)
    p.start(); c.start()
    p.join();  c.join()


# ──────────────────────────────────────────────────────
# 6. Barrier — punto de encuentro: todos esperan antes de continuar
# ──────────────────────────────────────────────────────
def demo_barrier():
    print(f"\n{SEP}\n[Barrier] Punto de sincronización entre hilos\n{SEP}")
    barrera = threading.Barrier(3)

    def fase(id):
        print(f"  Hilo-{id}: completando fase 1…")
        time.sleep(0.1 * id)
        print(f"  Hilo-{id}: llegué a la barrera — esperando a los demás")
        barrera.wait()              # bloquea hasta que los 3 hilos lleguen
        print(f"  Hilo-{id}: ¡barrera cruzada! iniciando fase 2")

    hilos = [threading.Thread(target=fase, args=(i,)) for i in range(3)]
    for h in hilos: h.start()
    for h in hilos: h.join()


if __name__ == "__main__":
    demo_lock()
    demo_rlock()
    demo_semaphore()
    demo_event()
    demo_condition()
    demo_barrier()
    print(f"\n{SEP}\nTodas las primitivas ejecutadas correctamente.\n{SEP}")
