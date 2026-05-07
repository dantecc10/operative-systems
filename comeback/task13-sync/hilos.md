# Primitivas de Sincronización de Procesos

## 1. Lock — Exclusión mutua básica

Solo un hilo puede estar en la sección crítica a la vez.

```mermaid
flowchart TD
    A([Hilo inicia]) --> B{¿Lock libre?}
    B -- Sí --> C[Adquiere Lock]
    C --> D[/SECCIÓN CRÍTICA/]
    D --> E[Libera Lock]
    E --> F([Hilo termina])
    B -- No --> G[Espera bloqueado]
    G --> B
```

---

## 2. RLock — Lock re-entrante

El mismo hilo puede adquirir el lock múltiples veces sin provocar un deadlock.

```mermaid
flowchart TD
    A([Hilo inicia]) --> B[Adquiere RLock nivel 1]
    B --> C[Llama función interna]
    C --> D[Adquiere RLock nivel 2\nre-entrante — no bloquea]
    D --> E[/Lógica interna/]
    E --> F[Libera nivel 2]
    F --> G[Libera nivel 1]
    G --> H([Hilo termina])
```

---

## 3. Semaphore — Acceso limitado a N hilos

El semáforo mantiene un contador interno. Solo `N` hilos pueden estar en la sección crítica simultáneamente.

```mermaid
flowchart TD
    A([N hilos llegan]) --> B{¿Contador > 0?}
    B -- Sí --> C[Decrementa contador]
    C --> D[/SECCIÓN CRÍTICA/]
    D --> E[Incrementa contador]
    E --> F([Hilo sale])
    B -- No --> G[Hilo espera bloqueado]
    G --> B
```

---

## 4. Event — Señalización entre hilos

Los hilos esperan una señal para continuar. Un hilo disparador llama a `event.set()`.

```mermaid
flowchart TD
    W1([Hilo trabajador]) --> E1{¿Evento activo?}
    E1 -- No --> E2[event.wait\nbloqueado]
    E2 --> E1
    E1 -- Sí --> E3[/Ejecuta tarea/]

    D([Hilo disparador]) --> D1[event.set]
    D1 -.despierta.-> E2
```

---

## 5. Condition — Esperar/notificar con condición compartida

Combina un lock con la capacidad de `wait` y `notify`. Ideal para el patrón productor–consumidor.

```mermaid
flowchart TD
    P([Productor]) --> P1[acquire Condition]
    P1 --> P2[/Produce ítem/]
    P2 --> P3[cond.notify]
    P3 --> P4[release]

    C([Consumidor]) --> C1[acquire Condition]
    C1 --> C2{¿Hay ítems?}
    C2 -- No --> C3[cond.wait\nlibera lock y bloquea]
    C3 --> C2
    C2 -- Sí --> C4[/Consume ítem/]
    C4 --> C5[release]

    P3 -.despierta.-> C3
```

---

## 6. Barrier — Punto de encuentro

Todos los hilos deben llegar a la barrera antes de que cualquiera pueda continuar.

```mermaid
flowchart TD
    H1([Hilo 0]) --> F1[/Fase 1/]
    H2([Hilo 1]) --> F2[/Fase 1/]
    H3([Hilo 2]) --> F3[/Fase 1/]

    F1 --> W[barrier.wait\npunto de encuentro]
    F2 --> W
    F3 --> W

    W --> G[/Fase 2 — todos continúan juntos/]
```

---

## Resumen comparativo

| Primitiva   | Hilos permitidos | Uso principal                         |
|-------------|-----------------|---------------------------------------|
| `Lock`      | 1               | Exclusión mutua simple                |
| `RLock`     | 1 (re-entrante) | Funciones que se llaman recursivamente|
| `Semaphore` | N               | Limitar acceso concurrente            |
| `Event`     | Todos a la vez  | Señal de arranque o notificación      |
| `Condition` | 1 + notificación| Productor–Consumidor                  |
| `Barrier`   | Todos sincronizan| Fases coordinadas entre hilos        |
