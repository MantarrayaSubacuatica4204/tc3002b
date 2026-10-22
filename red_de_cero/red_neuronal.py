import math
from random import shuffle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# ==========================================
# 1. DEFINICIÓN DE LA CLASE CAPA
# ==========================================


class capa:

  def __init__(self, n_neuronas_capa_anterior, n_neuronas, funcion_act):
    self.funcion_act = funcion_act
    self.b = np.round(
        stats.truncnorm.rvs(-1, 1, loc=0, scale=1, size=n_neuronas).reshape(
            1, n_neuronas
        ),
        3,
    )
    self.W = np.round(
        stats.truncnorm.rvs(
            -1, 1, loc=0, scale=1, size=n_neuronas * n_neuronas_capa_anterior
        ).reshape(n_neuronas_capa_anterior, n_neuronas),
        3,
    )


# ==========================================
# 2. FUNCIONES DE ACTIVACIÓN Y DERIVADAS
# ==========================================

# Función Sigmoide
sigmoid = (
    lambda x: 1 / (1 + np.exp(-x)),
    lambda x: x * (1 - x),
)

# Función ReLu y su derivada
def derivada_relu(x):
  x[x <= 0] = 0
  x[x > 0] = 1
  return x


relu = (lambda x: x * (x > 0), lambda x: derivada_relu(x))

# ==========================================
# 3. FUNCIÓN DE COSTE (MSE)
# ==========================================


def mse(Ypredich, Yreal):
  x = (np.array(Ypredich) - np.array(Yreal)) ** 2
  x = np.mean(x)
  y = np.array(Ypredich) - np.array(Yreal)
  return (x, y)


# ==========================================
# 4. FUNCIÓN DE ENTRENAMIENTO
# ==========================================


def entrenamiento(X, Y, red_neuronal, lr=0.01):
  # Propagación hacia adelante (Feedforward)
  output = [X]
  for num_capa in range(len(red_neuronal)):
    z = (
        output[-1] @ red_neuronal[num_capa].W
        + red_neuronal[num_capa].b
    )
    a = red_neuronal[num_capa].funcion_act[0](z)
    output.append(a)

  # Propagación hacia atrás (Backpropagation y Gradient Descent)
  back = list(range(len(output) - 1))
  back.reverse()

  delta = []
  for capa_idx in back:
    a = output[capa_idx + 1]
    if capa_idx == back[0]:
      x = mse(a, Y)[1] * red_neuronal[capa_idx].funcion_act[1](a)
      delta.append(x)
    else:
      x = delta[-1] @ W_temp * red_neuronal[capa_idx].funcion_act[1](a)
      delta.append(x)

    W_temp = red_neuronal[capa_idx].W.transpose()

    # Gradient Descent (Optimización de parámetros)
    red_neuronal[capa_idx].b = (
        red_neuronal[capa_idx].b
        - np.mean(delta[-1], axis=0, keepdims=True) * lr
    )
    red_neuronal[capa_idx].W = (
        red_neuronal[capa_idx].W
        - output[capa_idx].transpose() @ delta[-1] * lr
    )

  return output[-1]


# ==========================================
# 5. CASO PRÁCTICO: CLASIFICACIÓN DE PUNTOS
# ==========================================


def circulo(num_datos=100, R=1, minimo=0, maximo=1):
  pi = math.pi
  r = (
      R
      * np.sqrt(stats.truncnorm.rvs(minimo, maximo, size=num_datos))
      * 10
  )
  theta = (
      stats.truncnorm.rvs(minimo, maximo, size=num_datos) * 2 * pi * 10
  )
  x = np.cos(theta) * r
  y = np.sin(theta) * r
  y = y.reshape((num_datos, 1))
  x = x.reshape((num_datos, 1))
  x = np.round(x, 3)
  y = np.round(y, 3)
  df = np.column_stack([x, y])
  return df


def guardar_pesos_excel(red_neuronal, filename='pesos_red_neuronal.xlsx'):
  """Exporta los pesos (W) y sesgos (b) de cada capa a un archivo Excel."""
  registros_planos = []

  with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    for idx, c in enumerate(red_neuronal):
      num_capa = idx + 1
      n_in, n_out = c.W.shape

      cols = [f'Neurona_{j+1}' for j in range(n_out)]
      idx_w = [f'Entrada_{i+1}' for i in range(n_in)]

      # Pesos W y Sesgos b organizados
      df_w = pd.DataFrame(c.W, index=idx_w, columns=cols)
      df_b = pd.DataFrame(c.b, index=['Sesgo (b)'], columns=cols)

      # Hoja individual por cada capa con su matriz completa
      df_capa = pd.concat([df_w, df_b])
      df_capa.to_excel(writer, sheet_name=f'Capa_{num_capa}')

      # Registros para hoja resumen consolidada
      for i in range(n_in):
        for j in range(n_out):
          registros_planos.append({
              'Capa': f'Capa {num_capa}',
              'Tipo': 'Peso (W)',
              'Origen': f'Entrada {i+1}',
              'Destino': f'Neurona {j+1}',
              'Valor': c.W[i, j],
          })
      for j in range(n_out):
        registros_planos.append({
            'Capa': f'Capa {num_capa}',
            'Tipo': 'Sesgo (b)',
            'Origen': 'N/A',
            'Destino': f'Neurona {j+1}',
            'Valor': c.b[0, j],
        })

    # Hoja tabular consolidada
    df_resumen = pd.DataFrame(registros_planos)
    df_resumen.to_excel(writer, sheet_name='Todos_los_Pesos', index=False)

  print(f'Pesos guardados exitosamente en: {filename}')


if __name__ == '__main__':
  # Generación de datos de prueba
  datos_1 = circulo(num_datos=150, R=2)
  datos_2 = circulo(num_datos=150, R=0.5)
  X = np.concatenate([datos_1, datos_2])
  X = np.round(X, 3)
  Y = [0] * 150 + [1] * 150
  Y = np.array(Y).reshape(len(Y), 1)

  # Configuración de la red neuronal
  # 2 neuronas de entrada, capas ocultas de 4 y 8, y 1 neurona de salida.
  neuronas = [2, 4, 8, 1]
  funciones_activacion = [relu, relu, sigmoid]

  red_neuronal = []
  for paso in range(len(neuronas) - 1):
    x_capa = capa(neuronas[paso], neuronas[paso + 1], funciones_activacion[paso])
    red_neuronal.append(x_capa)

  # Entrenamiento durante 1000 épocas
  error = []
  predicciones = []
  for epoch in range(0, 1000):
    ronda = entrenamiento(X=X, Y=Y, red_neuronal=red_neuronal, lr=0.001)
    predicciones.append(ronda)
    temp = mse(np.round(predicciones[-1]), Y)[0]
    error.append(temp)

  print(f'Error final en la última época: {error[-1]}')

  # Visualización de la evolución del error
  epoch_list = list(range(0, 1000))
  plt.plot(epoch_list, error)
  plt.title('Evolución del error de la red neuronal')
  plt.xlabel('Época')
  plt.ylabel('Error Cuadrático Medio (MSE)')
  plt.savefig('evolucion_error.png')

  # Exportar pesos generados a Excel
  guardar_pesos_excel(red_neuronal)

