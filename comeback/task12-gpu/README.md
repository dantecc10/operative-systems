# Task 12 — Programación de Tarjetas de Vídeo (Tutorial)

Tutorial con ejemplos comentados sobre el uso de aceleración por hardware en cuatro plataformas. Cada sección es independiente y tiene manejo de errores para ejecutarse aunque no esté instalada la librería correspondiente.

## Requerimientos por plataforma

### 0. NumPy — CPU baseline (siempre disponible)
```bash
pip install numpy
```

### 1. OpenCL — Genérico (NVIDIA / AMD / Intel / Apple)
```bash
pip install pyopencl
```
> Requiere tener instalados los drivers OpenCL de tu GPU. En Linux:
> ```bash
> # NVIDIA
> sudo apt install nvidia-opencl-dev
> # AMD
> sudo apt install rocm-opencl-runtime
> # Intel / CPU genérico
> sudo apt install intel-opencl-icd
> ```

### 2. NVIDIA CUDA — CuPy
```bash
# Ajusta el número de versión a tu instalación de CUDA (nvidia-smi para verlo)
pip install cupy-cuda12x
```
> Requiere [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) instalado.

### 3. AMD / Apple / NVIDIA — PyTorch
```bash
pip install torch
# Para AMD ROCm:
pip install torch --index-url https://download.pytorch.org/whl/rocm6.0
```

## Ejecución

```bash
cd comeback/task12-gpu
python3 gpu_tutorial.py
```

Las secciones cuya librería no esté instalada imprimirán un aviso y continuarán sin errores.

## Descripción del programa

| Sección | Plataforma | Operación demostrada |
|---------|------------|----------------------|
| 0. NumPy | CPU | Suma de vectores (1 M elementos) |
| 1. OpenCL | Genérico | Kernel C personalizado ejecutado en GPU |
| 2. CuPy | NVIDIA CUDA | Suma de vectores en VRAM |
| 3. PyTorch | NVIDIA / AMD / Apple | Selección automática de dispositivo + suma |

## Salida esperada (con todas las librerías)

```
[NumPy / CPU]             c[0] = 2.0  ✓
[OpenCL / GPU]            c[0] = 1.2345  (esperado 1.2345)  ✓
[CuPy / CUDA]             c[0] = 2.0  ✓
[NVIDIA CUDA (torch)]     c[0] = 2.0  ✓
```
