# Proyecto Super-Resolución de Imágenes 2D
**Métodos Numéricos - Electivo de Especialidad II - Universidad Alberto Hurtado**

## 1. Introducción
Este documento detalla los pasos exactos para instalar el entorno y ejecutar nuestro proyecto de Super-Resolución localmente. Sigan estas instrucciones para garantizar que la demostración en vivo funcione sin errores.

### Formulación Matemática del Problema
El objetivo del proyecto es resolver el problema inverso regularizado para reconstruir una imagen de alta resolución ($x$) a partir de una degradada ($b$):

$$\min_{x} J(x) = \frac{1}{2} ||Ax - b||^2 + \lambda R(x)$$

Donde:
* **$A$**: Operador de degradación (Blur Gaussiano + Submuestreo).
* **$b$**: Imagen LR observada.
* **$x$**: Imagen HR buscada.
* **$R(x)$**: Término de regularización (L2 o Huber).
* **$λ$**: λ > 0 es un parámetro de regularización.
---

## 2. Requisitos Previos
Antes de comenzar, asegúrense de tener instalado:
* Python (Versión 3.8 o superior).
* Un editor de código (VS Code recomendado).
* La carpeta del proyecto `proyecto_sr` con todos los archivos actualizados.

## 3. Verificación de Estructura
La carpeta raíz `proyecto_sr` debe contener exactamente la siguiente estructura:

* `app.py` (Controlador principal)
* `utils.py` (Utilidades de imagen)
* `requirements.txt` (Lista de dependencias)
* Carpeta `numerical/`:
    * `__init__.py`
    * `operators.py`
    * `regularizers.py`
    * `solver.py`
* Carpeta `templates/`:
    * `index.html`
    * `result.html`
* Carpeta `static/`:
    * `uploads/` (Carpeta vacía)
    * `results/` (Carpeta vacía)

---

## 4. Instalación (Paso a Paso)
Abrir una terminal (consola) dentro de la carpeta `proyecto_sr` y ejecutar los comandos en orden.

### 4.1. Paso A: Entorno Virtual (Recomendado)
Para aislar las librerías del proyecto:

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
## 5. Ejecución de la Aplicación Web
Una vez completada la instalación 

1. En la terminal, ejecutar:

```bash
python app.py
```
2. Si la carga es exitosa, aparecerá un mensaje similar a:
   
Running  on  http://127.0.0.1:5000

3. Abrir el navegador web e ingresar a la dirección: http://127.0.0.1:5000

## 6. Parámetros para la Demo (Configuración Segura)

Para evitar errores de inestabilidad numérica (costos infinitos) durante la presentación, utilizar la siguiente configuración probada:

* `Imagen:` Subir una foto pequeña (ej. 200 × 200 píxeles) para rapidez.
* `Regularización:` Huber (recomendado) o L2.
* `Factor (s):` 2.
* `Lambda (λ):` 0,05 (Nota: Si se usa s = 5, bajar a 0,001).
* `Delta (δ):` 0,01.
* `Iteraciones:` 30.
* `Paso (τ ):` 0,5 (Nota: Si se usa s = 5, bajar a 0,1).
* `Presionar el botón "Ejecutar Reconstrucción" para ver los resultados.`

## 7. Solución de problemas comunes

* `La imagen resultante está en escala de grises:`Es el comportamiento esperado. El algoritmo trabaja sobre un único canal (Luminancia) para optimizar el cálculo.
* `El valor del costo $J(x)$ es muy alto:`No es un error crítico. El costo numérico puede ser alto, pero la reconstrucción de la imagen sigue siendo válida y nítida.
* `Error "Module not found":`No se ejecutó el comando pip  install.
* `Error "Address already in use":`Hay otra instancia de la terminal ejecutando Flask. Cerrar todas las terminales y reiniciar.
