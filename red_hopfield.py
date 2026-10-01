class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        # Inicializamos la matriz de pesos con ceros (tamaño: size x size)
        self.weights = [[0.0 for _ in range(size)] for _ in range(size)]
    
    def train(self, patterns):
        """
        Entrena la red usando la regla de aprendizaje de Hebb.
        patterns: Lista de listas, donde cada lista es un patrón compuesto por 1s y -1s.
        """
        for p in patterns:
            if len(p) != self.size:
                raise ValueError(f"El tamaño del patrón debe ser {self.size}")
            
            for i in range(self.size):
                for j in range(self.size):
                    # No hay auto-conexiones (la diagonal principal es 0)
                    if i != j:
                        self.weights[i][j] += p[i] * p[j]

    def predict(self, pattern, steps=10):
        """
        Intenta recordar un patrón dado un input posiblemente ruidoso.
        """
        if len(pattern) != self.size:
             raise ValueError(f"El tamaño del patrón debe ser {self.size}")
        
        # Copiamos el patrón inicial para no modificar el original
        current_state = list(pattern)
        
        for step in range(steps):
            previous_state = list(current_state)
            
            # Actualizamos cada neurona
            for i in range(self.size):
                activation = 0
                for j in range(self.size):
                    activation += self.weights[i][j] * previous_state[j]
                
                # Función de activación (signo)
                if activation > 0:
                    current_state[i] = 1
                elif activation < 0:
                    current_state[i] = -1
                # Si es 0, mantiene su estado anterior
                
            # Comprobamos si la red ha convergido (ya no cambia)
            if current_state == previous_state:
                print(f"Convergencia alcanzada en el paso {step + 1}")
                break
                
        return current_state

# --- Ejemplo de Uso ---
def print_pattern(pattern, width=5):
    """Función auxiliar para imprimir el patrón 1D como una matriz 2D"""
    for i in range(0, len(pattern), width):
        row = pattern[i:i+width]
        # Usamos # para 1 (dibujo) y . para -1 (fondo)
        print(" ".join(["#" if x == 1 else "." for x in row]))
    print()

if __name__ == "__main__":
    # Creamos una red de 25 neuronas (para una cuadrícula de 5x5 píxeles)
    red = HopfieldNetwork(size=25)
    
    # Representación del número 1 (5x5)
    # ..██..
    # .███..
    # ..██..
    # ..██..
    # .████.
    patron_1 = [
        -1, -1,  1, -1, -1,
        -1,  1,  1, -1, -1,
        -1, -1,  1, -1, -1,
        -1, -1,  1, -1, -1,
        -1,  1,  1,  1, -1
    ]
    
    # Representación del número 2 (5x5)
    # ████..
    # ....██
    # ..██..
    # ██....
    # ██████
    patron_2 = [
         1,  1,  1,  1, -1,
        -1, -1, -1,  1, -1,
        -1,  1,  1, -1, -1,
         1, -1, -1, -1, -1,
         1,  1,  1,  1,  1
    ]
    
    print("Patrón a memorizar: Número 1")
    print_pattern(patron_1)
    
    print("Patrón a memorizar: Número 2")
    print_pattern(patron_2)
    
    print("Entrenando la red...\n")
    red.train([patron_1, patron_2])

    # Cambiamos intencionalmente algunos píxeles (ruido)
    patron_ruidoso_1 = [
        -1,  1,  1, -1, -1, 
        -1,  1, -1, -1, -1,
        -1, -1,  1, -1, -1,
        -1, -1,  1,  1, -1, 
        -1,  1,  1,  1, -1
    ]
    
    print("Introduciendo Número 1 con ruido:")
    print_pattern(patron_ruidoso_1)
    
    patron_recuperado_1 = red.predict(patron_ruidoso_1)
    print("Patrón recuperado (Debería ser el Número 1):")
    print_pattern(patron_recuperado_1)
    patron_ruidoso_2 = [
         1,  1, -1,  1, -1,
        -1, -1, -1,  1, -1,
        -1,  1, -1, -1, -1,
         1,  1, -1, -1, -1,
         1,  1,  1, -1,  1
    ]

    print("Introduciendo Número 2 con ruido:")
    print_pattern(patron_ruidoso_2)
    
    patron_recuperado_2 = red.predict(patron_ruidoso_2)
    print("Patrón recuperado (Debería ser el Número 2):")
    print_pattern(patron_recuperado_2)
