import numpy as np

class Regularizers:
    """
    Calcula los gradientes de regularización R(x).
    Cumple con las secciones 1.1 (L2) y 1.2 (Huber) del PDF.
    """
    def __init__(self, delta=0.01):
        self.delta = delta

    def _gradient_operator(self, x):
        # [cite_start]Calcula diferencias finitas (Dx, Dy) [cite: 29]
        grad_x = np.roll(x, -1, axis=1) - x
        grad_y = np.roll(x, -1, axis=0) - x
        # Corregir bordes para evitar efecto cíclico
        grad_x[:, -1] = 0
        grad_y[-1, :] = 0
        return grad_x, grad_y

    def _divergence_operator(self, p1, p2):
        # Divergencia discreta (Adjoint del gradiente negativo)
        div_x = p1 - np.roll(p1, 1, axis=1)
        div_y = p2 - np.roll(p2, 1, axis=0)
        div_x[:, 0] = p1[:, 0]
        div_y[0, :] = p2[0, :]
        return div_x + div_y

    def get_L2_gradient(self, x):
        """ 
        Gradiente L2: -2 * Laplaciano. 
        Ec. (3) del PDF.
        """
        dx, dy = self._gradient_operator(x)
        return -2 * self._divergence_operator(dx, dy)

    def get_Huber_gradient(self, x):
        """ 
        Gradiente Huber (TV suave).
        Ec. (6) del PDF.
        """
        dx, dy = self._gradient_operator(x)
        
        # Derivada de Huber condicionada por delta
        def phi_prime(z, delta):
            condition = np.abs(z) <= delta
            # Si es pequeño (ruido) -> z/delta
            # Si es grande (borde) -> sign(z)
            return np.where(condition, z / delta, np.sign(z))

        w_dx = phi_prime(dx, self.delta)
        w_dy = phi_prime(dy, self.delta)
        
        return -self._divergence_operator(w_dx, w_dy)