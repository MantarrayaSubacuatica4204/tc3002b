import os

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        # Inicializamos los pesos en 0
        self.weights = [[0.0 for _ in range(size)] for _ in range(size)]
    
    def train(self, patterns):
        """Entrena la red con una lista de patrones usando la regla de Hebb."""
        for p in patterns:
            if len(p) != self.size:
                raise ValueError(f"El tamaño del patrón debe ser {self.size}")
            
            for i in range(self.size):
                for j in range(self.size):
                    if i != j:
                        self.weights[i][j] += p[i] * p[j]

        # Normalizamos los pesos
        for i in range(self.size):
            for j in range(self.size):
                self.weights[i][j] /= self.size

    def predict(self, pattern, steps=10):
        """Intenta recuperar un patrón a partir de una versión con ruido."""
        if len(pattern) != self.size:
             raise ValueError(f"El tamaño del patrón debe ser {self.size}")
        
        current_state = list(pattern)
        
        for step in range(steps):
            previous_state = list(current_state)
            
            for i in range(self.size):
                activation = 0
                for j in range(self.size):
                    activation += self.weights[i][j] * previous_state[j]
                
                if activation > 0:
                    current_state[i] = 1
                elif activation < 0:
                    current_state[i] = -1
                
            if current_state == previous_state:
                print(f"Convergencia alcanzada en el paso {step + 1}")
                break
                
        return current_state


def print_pattern(pattern, width=8):
    """Imprime el patrón en consola."""
    for i in range(0, len(pattern), width):
        row = pattern[i:i+width]
        print(" ".join(["#" if x == 1 else "." for x in row]))
    print()

def parse_shape(shape_str):
    """Convierte una lista de strings a una lista de valores 1 y -1."""
    pattern = []
    for row in shape_str:
        for char in row.replace(" ", ""):
            if char == '#':
                pattern.append(1)
            elif char == '.':
                pattern.append(-1)
    return pattern

def load_patterns_from_file(filepath):
    """Carga patrones desde un archivo de texto.
    
    El archivo debe contener el nombre del patrón seguido de sus líneas.
    """
    patterns = {}
    current_name = None
    current_shape = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Si la línea no contiene '#' ni '.', asumimos que es el nombre del patrón
            if '#' not in line and '.' not in line:
                if current_name and current_shape:
                    patterns[current_name] = parse_shape(current_shape)
                current_name = line
                current_shape = []
            else:
                current_shape.append(line)
                
        if current_name and current_shape:
            patterns[current_name] = parse_shape(current_shape)
            
    return patterns

if __name__ == "__main__":
    # Red para imágenes de 8x8 píxeles
    red = HopfieldNetwork(size=64)
    
    # Cargar patrones desde el archivo
    archivo_patrones = "patrones.txt"
    if not os.path.exists(archivo_patrones):
        print(f"Error: No se encontró el archivo '{archivo_patrones}'.")
        print("Crea un archivo 'patrones.txt' con los patrones a utilizar.")
        exit(1)
        
    patrones = load_patterns_from_file(archivo_patrones)
    
    # Extraer patrones de entrenamiento
    nombres_entrenamiento = ["CUADRADO", "CIRCULO", "TRIANGULO"]
    patrones_entrenamiento = []
    
    print("--- Figuras Originales a Memorizar ---")
    for nombre in nombres_entrenamiento:
        if nombre in patrones:
            print(f"{nombre}:")
            print_pattern(patrones[nombre])
            patrones_entrenamiento.append(patrones[nombre])
        else:
            print(f"Advertencia: Patrón {nombre} no encontrado en el archivo.")
            
    print("Enseñando las imágenes a la red...\n")
    if patrones_entrenamiento:
        red.train(patrones_entrenamiento)
    
    # Pruebas con patrones ruidosos
    nombres_prueba = ["CUADRADO_RUIDOSO", "TRIANGULO_RUIDOSO"]
    print("--- Prueba de Recuperación de Figuras ---")
    
    for nombre in nombres_prueba:
        if nombre in patrones:
            print(f"Mostrando a la red: {nombre}")
            print_pattern(patrones[nombre])
            
            recuperado = red.predict(patrones[nombre])
            print("Figura reconstruida:")
            print_pattern(recuperado)
        else:
            print(f"Advertencia: Patrón de prueba {nombre} no encontrado en el archivo.")
