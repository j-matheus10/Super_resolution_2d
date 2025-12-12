````
# Proyecto Super-Resolución de Imágenes 2D

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Status](https://img.shields.io/badge/Status-Finalizado-success)

**Métodos Numéricos - Electivo de Especialidad II - Universidad Alberto Hurtado**

Este proyecto implementa un sistema de **Super-Resolución (SR)** que reconstruye imágenes de alta resolución (HR) a partir de imágenes degradadas de baja resolución (LR). El problema se aborda como un **problema inverso mal condicionado**, resuelto mediante un algoritmo iterativo de **Descenso de Gradiente** con regularización, desplegado sobre una interfaz web con **Flask**.

---

## 1. Descripción Técnica y Formulación Matemática

El objetivo del proyecto es resolver el problema inverso regularizado para reconstruir una imagen de alta resolución ($x$) a partir de una degradada ($b$). Buscamos minimizar la siguiente función de costo:

$$\min_{x} J(x) = \frac{1}{2} ||Ax - b||^2 + \lambda R(x)$$

Donde:
* **$x$**: Imagen HR buscada (incógnita).
* **$b$**: Imagen LR observada (entrada).
* **$A$**: Operador de degradación modelado como **Blur Gaussiano 2D + Submuestreo**.
* **$A^\top$**: Operador adjunto (Upsampling + Blur) utilizado para el cálculo del gradiente.
* **$\lambda$**: Parámetro de regularización ($\lambda > 0$).
* **$R(x)$**: Término de regularización. Se implementaron dos opciones:
    1.  **L2 (Tikhonov):** Penaliza la norma del gradiente ($||\nabla x||^2$). Suaviza la imagen globalmente.
    2.  **Huber (TV Suave):** Combina comportamiento cuadrático (para ruido) y lineal (para bordes), controlado por un parámetro $\delta$.

---

## 2. Requisitos Previos

Antes de comenzar, asegúrese de tener instalado lo siguiente:
* **Python** (Versión 3.8 o superior).
* Un editor de código (VS Code recomendado).
* Y obviamente, la carpeta del proyecto `Super_resolution_2d-main` con todos los archivos actualizados.

---

## 3. Estructura del Repositorio

Para cumplir con los estándares de calidad del código, la carpeta `Super_resolution_2d-main` mantiene la siguiente estructura:

```text
Super_resolution_2d-main/
│
├── app.py                 # Controlador principal de la aplicación Flask
├── utils.py               # Utilidades de carga y procesamiento de imágenes
├── requirements.txt       # Lista de dependencias del proyecto
│
├── numerical/             # Módulo matemático (Núcleo del algoritmo)
│   ├── __init__.py
│   ├── operators.py       # Implementación de operadores A y A^T
│   ├── regularizers.py    # Implementación de gradientes L2 y Huber
│   └── solver.py          # Algoritmo de Descenso de Gradiente
│
├── templates/             # Vistas HTML (Frontend)
│   ├── index.html         # Formulario de configuración
│   └── result.html        # Visualización de resultados
│
├── static/                # Archivos estáticos
│   ├── uploads/           # Imágenes subidas
│   └── results/           # Imágenes generadas
│    
└── examples/              # Algunas imágenes de prueba LR y sus resultados HR
    
````

-----

## 4\. Instalación (Paso a Paso)

Abrir una terminal (consola) dentro de la carpeta `Super_resolution_2d-main` y ejecutar los comandos en el siguiente orden.

### 4.1. Paso A: Entorno Virtual (Recomendado)

Para aislar las librerías del proyecto y evitar conflictos:

**En Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**En Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4.2. Paso B: Instalación de dependencias

Instalar las librerías necesarias (Flask, NumPy, SciPy, Pillow, etc.):

```bash
pip install -r requirements.txt
```

-----

## 5\. Ejecución de la Aplicación Web

Una vez completada la instalación:

1.  En la terminal, ejecutar:

    ```bash
    python app.py
    ```

2.  Si la carga es exitosa, aparecerá un mensaje similar a:

    ```text
    Running on http://127.0.0.1:5000
    ```

3.  Abrir el navegador web e ingresar a la dirección: **http://127.0.0.1:5000**

-----

## 6\. Parámetros para la Demo (Configuración Segura)

Para garantizar una demostración fluida y evitar inestabilidad numérica (error de coste infinito) durante la presentación, se recomienda utilizar la siguiente configuración probada:

  * **Imagen:** Subir una foto pequeña (ej. $200 \times 200$ píxeles) para rapidez.
  * **Regularización:** `Huber` (recomendado para bordes) o `L2`.
  * **Factor ($s$):** `2`.
  * **Lambda ($\lambda$):** `0.05`
  * **Delta ($\delta$):** `0.01` (Solo aplica para Huber).
  * **Iteraciones:** `30` - `50`.
  * **Paso ($\tau$):** `0.5` 

> **Acción:** Presionar el botón **"Ejecutar Reconstrucción"** para ver los resultados.

-----

## 7\. Solución de Problemas Comunes

  * **La imagen resultante está en escala de grises:**

      * Es el comportamiento esperado. El algoritmo trabaja sobre un único canal de intensidad (Luminancia) para optimizar el cálculo matricial numérico, como es estándar en problemas inversos académicos.

  * **El valor del costo $J(x)$ es muy alto:**

      * No es un error crítico. El costo numérico depende de la magnitud de los píxeles y la regularización. Mientras la imagen visualmente se reconstruya (sea nítida), el algoritmo funciona.

  * **La imagen sale negra/blanca o costo infinito:**

      * El paso ($\tau$) es demasiado alto para la configuración dada. Bajar $\tau$ a $0.1$.

  * **Error "Module not found":**

      * No se ejecutó el comando `pip install` o no se activó el entorno virtual.

  * **Error "Address already in use":**

      * Hay otra instancia de la terminal ejecutando Flask. Cerrar todas las terminales y reiniciar.

<!-- end list -->

```
