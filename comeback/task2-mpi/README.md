# Task 2 — MPI Suma (Mecanismos de Comunicación entre Procesos)

El proceso 0 genera 10,000 números aleatorios, los distribuye equitativamente entre 4 procesos usando `Scatter`, cada proceso calcula la suma de su parte, y el proceso 0 recoge y muestra el resultado total con `reduce`.

## Requerimientos

- Python 3.10+
- OpenMPI o MPICH instalado en el sistema
- `mpi4py`
- `numpy`

```bash
# 1. Instalar OpenMPI (Linux)
sudo apt install openmpi-bin libopenmpi-dev

# 2. Instalar las librerías Python
pip install mpi4py numpy
```

> En caso de usar un entorno virtual, actívalo antes de instalar.

## Ejecución

El programa **requiere exactamente 4 procesos**:

```bash
cd comeback/task2-mpi
mpirun -n 4 python3 mpi_add.py
```

## Descripción del programa

| Componente | Descripción |
|------------|-------------|
| `MPI.COMM_WORLD` | Comunicador global que agrupa los 4 procesos |
| `comm.Get_rank()` | Obtiene el ID del proceso actual (0–3) |
| `comm.Get_size()` | Número total de procesos activos |
| `np.random.randint()` | Proceso 0 genera 10,000 enteros aleatorios (1–100) |
| `comm.Scatter()` | Divide y distribuye el array en bloques iguales (2,500 por proceso) |
| `np.sum()` | Cada proceso suma su bloque local |
| `comm.reduce(..., MPI.SUM)` | Proceso 0 recibe y suma los 4 resultados parciales |

## Flujo de ejecución

```
Proceso 0: genera 10,000 números
      │
      ├──── 2,500 números ──→ Proceso 0  →  suma parcial 0
      ├──── 2,500 números ──→ Proceso 1  →  suma parcial 1
      ├──── 2,500 números ──→ Proceso 2  →  suma parcial 2
      └──── 2,500 números ──→ Proceso 3  →  suma parcial 3
                                               │
Proceso 0 ←────── reduce (MPI.SUM) ───────────┘
      │
      └──→ Imprime suma total
```

## Salida esperada

```
Proceso 0: Generados 10000 números.
Proceso 0: Suma parcial calculada.
Proceso 1: Suma parcial calculada.
Proceso 2: Suma parcial calculada.
Proceso 3: Suma parcial calculada.
──────────────────────────────
RESULTADO FINAL
La suma total de los 10000 números es: 505432
──────────────────────────────
```

> El valor de la suma varía en cada ejecución porque los números son aleatorios.
