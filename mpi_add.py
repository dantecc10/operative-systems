from mpi4py import MPI
import numpy as np

def main():
    # Inicio la comunicación
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # ID del proceso
    size = comm.Get_size()  # Número de procesos

    n_total = 10000
    n_por_proceso = n_total // size

    datos = None

    # El proceso 0 crea los datos
    if rank == 0:
        if size != 4:
            print(f"Error: Este programa está diseñado para 4 procesos, detectados: {size}")
            comm.Abort()
        
        # Se generan los números aleatorios
        datos = np.random.randint(1, 101, size=n_total, dtype='i')
        print(f"Proceso 0: Generados {n_total} números.")

    # Se crea un buffer en cada proceso para recibir los datos
    buffer_local = np.empty(n_por_proceso, dtype='i')

    # Se distribuyen lo datos
    comm.Scatter(datos, buffer_local, root=0)

    # Se realiza la suma en cada proceso
    suma_local = np.sum(buffer_local)
    print(f"Proceso {rank}: Suma parcial calculada.")

    # El proceso 0 suma las umas de los procesos
    suma_total = comm.reduce(suma_local, op=MPI.SUM, root=0)

    # El proceso 0 muestra el resultado final
    if rank == 0:
        print("-" * 30)
        print(f"RESULTADO FINAL")
        print(f"La suma total de los {n_total} números es: {suma_total}")
        print("-" * 30)

if __name__ == "__main__":
    main()
