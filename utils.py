import numpy as np
from PIL import Image

def load_image_as_array(filepath):
    """Carga imagen y la convierte a matriz numpy [0, 1] en escala de grises"""
    img = Image.open(filepath).convert('L')
    return np.array(img, dtype=np.float32) / 255.0

def save_array_as_image(array, filepath):
    """Convierte matriz numpy [0, 1] a imagen y la guarda"""
    array = np.clip(array, 0, 1) # Asegurar rango válido
    img_uint8 = (array * 255).astype(np.uint8)
    img = Image.fromarray(img_uint8)
    img.save(filepath)