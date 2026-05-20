# Guía de Problemas y Tareas de Programación

Este documento contiene la recopilación de instrucciones para diversos problemas técnicos, abarcando desde comandos de sistema hasta comunicación entre procesos y sockets.

## 1. Comandos Básicos del MS-DOS

**Fechas:** 13 de enero de 2026 - 14 de enero de 2026
**Instrucciones:**
Estudiar los siguientes comandos y sus posibles variantes:

* Red: `ipconfig`, `netstat`, `ping`, `routert`
* Sistema de archivos: `dir`, `mkdir`, `cd`, `rmdir`, `del`, `type`
* Utilidades: `notepad`, `date`, `find`, `findstr`
* Tuberías: `|`, `>`, `<`

**Entregable:** Realizar una libreta (.ipynb) en VS Code instalando el complemento Jupyter.

---

## 2. MPI Suma (Mecanismos de Comunicación entre Procesos)

**Fechas:** 4 de marzo de 2026 - 11 de marzo de 2026
**Instrucciones:**
Realizar un programa donde:

1. El proceso 0 genera 10,000 números.
2. Los reparte equitativamente entre cuatro procesos.
3. Cada proceso realiza la suma de su parte.
4. El proceso 0 recibe los resultados y muestra la suma total.

**Tecnología:** MPI y `mpi4py`.

---

## 3. Productor y Consumidor con Corrutinas

**Fechas:** 4 de marzo de 2026 - 11 de marzo de 2026
**Instrucciones:**
Simulación del modelo productor-consumidor.

* Utilizar corrutinas (`async`).
* Librerías: `queue`, `asyncio`.
* Implementar bloqueo de zona crítica mediante candados (locks).
* Salida visual: Imprimir con colores diferentes para cada trabajador.

---

## 4. Visualización de IPv4 en Tiempo Real (netstat)

**Fechas:** 4 de marzo de 2026 - 15 de marzo de 2026
**Instrucciones:**
Programa que lea en tiempo real las direcciones IPv4 enlazadas a la computadora usando `netstat`.

* Utilizar tuberías del sistema y `os.system`.
* Interfaz gráfica con `tkinter`.
* Validación: Mostrar en color rojo aquellas IPs que no sean válidas (referencia: [ipblocklist](https://github.com/bitwire-it/ipblocklist)).
* **Reporte:** Incluir portada, documentación, código comentado, capturas de corridas y conclusión.

---

## 5. Visualización de URLs en Tiempo Real (netstat)

**Fechas:** 4 de marzo de 2026 - 23 de marzo de 2026
**Instrucciones:**
Similar al proyecto de IPs, pero enfocado en URLs.

* Extraer URLs de `netstat` en tiempo real.
* Interfaz con `tkinter`.
* Validación: Resaltar en rojo URLs no válidas (referencia: [blacklists](https://github.com/fabriziosalmi/blacklists)).
* **Reporte:** Incluir portada, documentación, código comentado, corridas y conclusión.

---

## 6. Ejecución de Comandos Bash vía aiohttp

**Fechas:** 4 de marzo de 2026 - 30 de marzo de 2026
**Instrucciones:**
Utilizando el framework `aiohttp`, desarrollar una aplicación web que permita ejecutar comandos de bash remotamente.

* Librería base: `os` (específicamente `system`).

---

## 7. Comunicación Cliente-Servidor (Sockets)

**Fechas:** 18 de marzo de 2026 - 22 de marzo de 2026
**Instrucciones:**
Establecer una comunicación básica entre dos computadoras para crear un sistema de chat pequeño.

---

## 8. Lectura Remota de Directorios (Sockets)

**Fechas:** 18 de marzo de 2026 - 29 de marzo de 2026
**Instrucciones:**
Desarrollar dos programas (cliente/servidor) que permitan leer el contenido de un directorio en una máquina remota mediante sockets.

---

## 9. Módulos en Linux

**Fechas:** 15 de abril de 2026 - 22 de abril de 2026
**Instrucciones:**
Trabajar en un entorno Linux nativo o Live (no WSL/VM dentro de Windows).

* Seguir los pasos técnicos del vídeo proporcionado sobre módulos del kernel.
* Entregable: Capturas de pantalla de los procedimientos realizados.

---

## 10. Hilos con Semáforos (httpx)

**Fechas:** 22 de abril de 2026 - 24 de abril de 2026
**Instrucciones:**
Programa en Python que:

1. Lea una lista de URLs desde un archivo.
2. Las explore de forma concurrente usando la librería `httpx`.
3. Controle la concurrencia mediante semáforos de `asyncio`.

---

## 11. Hilos con Semáforos y Tkinter

**Fechas:** 22 de abril de 2026 - 28 de abril de 2026
**Instrucciones:**
Evolución del problema anterior integrando una interfaz gráfica con `tkinter` para visualizar el proceso de exploración de las URLs.

---

## 12. Programación de Tarjetas de Vídeo (Tutorial)

**Fechas:** 24 de abril de 2026 - 1 de mayo de 2026
**Instrucciones:**
Crear un tutorial con ejemplos explicados sobre el uso de aceleración por hardware en:

* NVIDIA
* AMD
* Apple
* Genérico (OpenCL)

---

## 13. Primitivas de Sincronización de Procesos

**Fechas:** 29 de abril de 2026 - 4 de mayo de 2026
**Instrucciones:**
Implementar ejemplos de sincronización (excepto `BoundedSemaphore`).

* Requisito: Ejemplo simple con `prints` para identificar las áreas (sección crítica, etc.).
* Documentación: Dibujar diagrama de flujo usando sintaxis **Mermaid**.
* Archivos relacionados: `controlZC.py`, `hilos.md`.

## 14. Puerto UDP 123

**Fechas:** 13 de mayo de 2026 - 20 de mayo de 2026

**Instrucciones:** 
Realizar una investigación del puerto udp 123:

* documentación general del funcionamiento del puerto 123
* mecanismos de protección en diferentes dispositivos:
  * router
  * laptop
  * celular
  * etc.
