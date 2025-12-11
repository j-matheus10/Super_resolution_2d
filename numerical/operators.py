import numpy as np
from scipy.signal import convolve2d

class SuperResolutionOperators:
    """
    Implementa el operador lineal A (degradación) y su adjunto A^T.
    Cumple con las ecuaciones (9) y (10) del PDF.
    """
    def __init__(self, kernel_size=5, sigma=1.0, s_factor=2):
        self.s = int(s_factor)
        self.kernel = self._create_gaussian_kernel(kernel_size, sigma)

    def _create_gaussian_kernel(self, size, sigma):
        # [cite_start]Crea un kernel gaussiano 2D normalizado [cite: 77]
        ax = np.linspace(-(size - 1) / 2., (size - 1) / 2., size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))
        return kernel / np.sum(kernel)

    def forward(self, x):
        """ 
        Operador A: Blur + Submuestreo.
        Ec. (9): (G * x) downsampled
        """
        # 1. Blur (convolución)
        blurred = convolve2d(x, self.kernel, mode='same', boundary='symm')
        # 2. Submuestreo: Tomar 1 pixel cada 's'
        return blurred[::self.s, ::self.s]

    def adjoint(self, y, target_shape):
        """ 
        Operador A^T: Upsample + Blur.
        Ec. (10): G^T * upsample(y)
        """
        # 1. Upsample: Crear matriz vacía y rellenar con píxeles originales
        upsampled = np.zeros(target_shape)
        upsampled[::self.s, ::self.s] = y
        # 2. Convolución (Como G es simétrico, G^T = G)
        return convolve2d(upsampled, self.kernel, mode='same', boundary='symm')