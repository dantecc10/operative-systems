"""
Task 12: Tutorial — Programación de Tarjetas de Vídeo
Ejemplos comentados para cuatro plataformas de aceleración por hardware:
  0. NumPy     — baseline CPU
  1. OpenCL    — genérico (NVIDIA / AMD / Intel / Apple)
  2. CuPy      — NVIDIA CUDA
  3. PyTorch   — NVIDIA CUDA / AMD ROCm / Apple MPS
"""
import numpy as np

# ===========================================================
# 0. BASELINE — CPU con NumPy
# ===========================================================
def demo_numpy():
    """Suma de dos vectores en CPU (sin GPU)."""
    a = np.ones(1_000_000, dtype=np.float32)
    b = np.ones(1_000_000, dtype=np.float32)
    c = a + b
    print(f"[NumPy / CPU]       c[0] = {c[0]:.1f}  ✓")

demo_numpy()


# ===========================================================
# 1. OpenCL — GENÉRICO (cualquier GPU o CPU con driver OpenCL)
# ===========================================================
try:
    import pyopencl as cl

    def demo_opencl():
        ctx   = cl.create_some_context(interactive=False)
        queue = cl.CommandQueue(ctx)

        a_np = np.random.rand(50_000).astype(np.float32)
        b_np = np.random.rand(50_000).astype(np.float32)

        mf = cl.mem_flags
        # Copiar arrays al dispositivo (GPU/CPU OpenCL)
        a_g = cl.Buffer(ctx, mf.READ_ONLY  | mf.COPY_HOST_PTR, hostbuf=a_np)
        b_g = cl.Buffer(ctx, mf.READ_ONLY  | mf.COPY_HOST_PTR, hostbuf=b_np)
        c_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)

        # Kernel: programa que corre en cada hilo de la GPU
        kernel_src = """
        __kernel void suma(__global const float *a,
                           __global const float *b,
                           __global       float *c) {
            int gid = get_global_id(0);   // índice global del hilo
            c[gid] = a[gid] + b[gid];
        }
        """
        prg = cl.Program(ctx, kernel_src).build()
        prg.suma(queue, a_np.shape, None, a_g, b_g, c_g)

        c_np = np.empty_like(a_np)
        cl.enqueue_copy(queue, c_np, c_g)
        queue.finish()

        esperado = a_np[0] + b_np[0]
        print(f"[OpenCL / GPU]      c[0] = {c_np[0]:.4f}  (esperado {esperado:.4f})  ✓")

    demo_opencl()

except ImportError:
    print("[OpenCL]  ⚠ No instalado — ejecuta: pip install pyopencl")
except Exception as e:
    print(f"[OpenCL]  ✗ Error: {e}")


# ===========================================================
# 2. NVIDIA CUDA — vía CuPy  (requiere CUDA toolkit instalado)
# ===========================================================
try:
    import cupy as cp

    def demo_cupy():
        a = cp.ones(1_000_000, dtype=cp.float32)   # array en VRAM
        b = cp.ones(1_000_000, dtype=cp.float32)
        c = a + b                                   # operación en GPU
        print(f"[CuPy / CUDA]       c[0] = {c[0].item():.1f}  ✓")

    demo_cupy()

except ImportError:
    print("[NVIDIA/CuPy]  ⚠ No instalado — ejecuta: pip install cupy-cuda12x")
except Exception as e:
    print(f"[NVIDIA/CuPy]  ✗ Error: {e}")


# ===========================================================
# 3. PyTorch — NVIDIA CUDA / AMD ROCm / Apple MPS
# ===========================================================
try:
    import torch

    def demo_torch():
        # Selección automática del dispositivo disponible
        if torch.backends.mps.is_available():
            device, label = torch.device("mps"),  "Apple MPS"
        elif torch.cuda.is_available():
            device, label = torch.device("cuda"), "NVIDIA CUDA (torch)"
        else:
            device, label = torch.device("cpu"),  "CPU (sin GPU torch)"

        a = torch.ones(1_000_000, dtype=torch.float32, device=device)
        b = torch.ones(1_000_000, dtype=torch.float32, device=device)
        c = a + b
        print(f"[{label:<22}]  c[0] = {c[0].item():.1f}  ✓")

    demo_torch()

except ImportError:
    print("[PyTorch]  ⚠ No instalado — ejecuta: pip install torch")
except Exception as e:
    print(f"[PyTorch]  ✗ Error: {e}")
