import os
import time
from flask import Flask, render_template, request, url_for
from utils import load_image_as_array, save_array_as_image
# Importamos NUESTROS módulos numéricos
from numerical.operators import SuperResolutionOperators
from numerical.regularizers import Regularizers
from numerical.solver import SuperResolutionSolver

app = Flask(__name__)

# [cite_start]Configuración de carpetas [cite: 115]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static/uploads')
app.config['RESULT_FOLDER'] = os.path.join(BASE_DIR, 'static/results')

# Asegurar que existan las carpetas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    # 1. Definir valores por defecto (para la primera vez que entras)
    defaults = {
        'reg_type': 'L2',
        's_factor': 2,
        'lambd': 0.05,
        'delta': 0.01,
        'max_iter': 30,
        'tau': 0.5
    }

    # 2. Si vienen datos en la URL (request.args), sobrescribir los defaults
    # Esto ocurre cuando vuelves desde la página de resultados
    params = {}
    for key, default_val in defaults.items():
        # Intentamos obtener el valor de la URL, si no existe, usamos el default
        params[key] = request.args.get(key, default_val)

    # 3. Enviar estos parámetros al HTML para que rellene los inputs
    return render_template('index.html', p=params)

@app.route('/superresolution', methods=['POST'])
def superresolution():
    # [cite_start]1. Recibir imagen y parámetros [cite: 111]
    if 'image' not in request.files: return "No image", 400
    file = request.files['image']
    if file.filename == '': return "No file", 400

    # Guardar LR
    filename = f"{int(time.time())}_{file.filename}"
    path_lr = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path_lr)

    # Leer parámetros del form
    reg_type = request.form.get('reg_type')
    s_factor = int(request.form.get('s_factor'))
    lambd = float(request.form.get('lambd'))
    delta = float(request.form.get('delta'))
    max_iter = int(request.form.get('max_iter'))
    tau = float(request.form.get('tau'))

    # [cite_start]2. Ejecutar Algoritmo [cite: 114]
    img_lr = load_image_as_array(path_lr)
    
    ops = SuperResolutionOperators(s_factor=s_factor)
    regs = Regularizers(delta=delta)
    solver = SuperResolutionSolver(ops, regs)

    img_hr, costs = solver.fit(img_lr, reg_type, lambd, tau, max_iter)

    # [cite_start]3. Guardar HR [cite: 115]
    filename_res = f"result_{filename}"
    path_hr = os.path.join(app.config['RESULT_FOLDER'], filename_res)
    save_array_as_image(img_hr, path_hr)

    # [cite_start]4. Mostrar Resultados [cite: 116]
    return render_template('result.html', 
                           original=filename, 
                           result=filename_res,
                           cost=round(costs[-1], 5),
                           params=request.form)

if __name__ == '__main__':
    app.run(debug=True)