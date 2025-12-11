import numpy as np

class SuperResolutionSolver:
    """
    Ejecuta el algoritmo de optimización iterativo.
    Cumple con la sección 2 del PDF.
    """
    def __init__(self, operators, regularizers):
        self.ops = operators
        self.regs = regularizers

    def fit(self, b_img, type_reg='L2', lambd=0.1, tau=0.1, max_iter=50):
        # b_img: Imagen LR (entrada)
        
        # Calcular dimensiones HR deseadas
        H_lr, W_lr = b_img.shape
        H_hr, W_hr = H_lr * self.ops.s, W_lr * self.ops.s
        target_shape = (H_hr, W_hr)

        # 1. Inicialización (Ec. 7): x0 = upsample(b)
        x_k = self.ops.adjoint(b_img, target_shape)
        
        cost_history = []

        # 2. Iteraciones (Ec. 8)
        for k in range(max_iter):
            # A. Gradiente de Fidelidad: A^T * (Ax - b)
            Ax = self.ops.forward(x_k)
            residual = Ax - b_img
            grad_fidelity = self.ops.adjoint(residual, target_shape)

            # B. Gradiente de Regularización
            if type_reg == 'L2':
                grad_reg = self.regs.get_L2_gradient(x_k)
            elif type_reg == 'Huber':
                grad_reg = self.regs.get_Huber_gradient(x_k)
            else:
                raise ValueError("Regularizador no válido")

            # C. Actualización del Descenso
            # x = x - tau * (grad_fidelidad + lambda * grad_reg)
            total_grad = grad_fidelity + (lambd * grad_reg)
            x_k = x_k - (tau * total_grad)

            # Guardar costo para graficar (opcional)
            cost_history.append(0.5 * np.sum(residual**2))

        return x_k, cost_history