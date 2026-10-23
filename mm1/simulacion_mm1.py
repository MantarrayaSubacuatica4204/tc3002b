"""
Simulación de una Línea de Espera M/M/1 usando SimPy
Jaime Trujillo Ruiz
A01276139
===================================================
Caso: Ventanilla única de atención bancaria.

Notación de Kendall M/M/1:
- M: Proceso de llegadas Poisson (tiempos entre llegadas Exponenciales con tasa lambda).
- M: Tiempos de servicio Exponenciales con tasa mu.
- 1: Un único servidor (capacidad = 1).
- Capacidad de cola infinita y disciplina FIFO.
"""

import random
import simpy

# --- Parámetros de la simulación ---
LAMBDA = 4.0      # Tasa de llegadas (clientes por unidad de tiempo, ej. 4 clientes/hora)
MU = 5.0          # Tasa de servicio (clientes atendidos por unidad de tiempo, ej. 5 clientes/hora)
TIEMPO_SIM = 1000.0  # Duración total de la simulación (horas)
SEMILLA = 42      # Semilla para reproducibilidad


def cliente(env, nombre, servidor, tiempos_espera, tiempos_sistema):
    """Proceso que modela el ciclo de vida de un cliente en el sistema."""
    t_llegada = env.now

    # Solicitar el servidor (recurso con capacidad 1)
    with servidor.request() as peticion:
        # Espera en la cola hasta que el servidor esté disponible
        yield peticion

        # Tiempo en el que inicia la atención
        t_inicio_atencion = env.now
        espera_cola = t_inicio_atencion - t_llegada
        tiempos_espera.append(espera_cola)

        # Tiempo de servicio exponencial (media = 1 / MU)
        tiempo_servicio = random.expovariate(MU)
        yield env.timeout(tiempo_servicio)

        # Tiempo al salir del sistema
        t_salida = env.now
        tiempo_sistema = t_salida - t_llegada
        tiempos_sistema.append(tiempo_sistema)


def generador_clientes(env, servidor, tiempos_espera, tiempos_sistema):
    """Proceso que genera llegadas de clientes siguiendo un proceso de Poisson."""
    i = 0
    while True:
        # Tiempo entre llegadas exponencial (media = 1 / LAMBDA)
        tiempo_entre_llegadas = random.expovariate(LAMBDA)
        yield env.timeout(tiempo_entre_llegadas)

        i += 1
        env.process(cliente(env, f"Cliente_{i}", servidor, tiempos_espera, tiempos_sistema))


def main():
    random.seed(SEMILLA)

    # Verificación de estabilidad del sistema
    rho = LAMBDA / MU
    print("=" * 60)
    print("        SIMULACIÓN DE COLA M/M/1 CON EVENTOS DISCRETOS")
    print("=" * 60)
    print(f"Tasa de llegada (lambda)  : {LAMBDA:.2f} clientes/hora")
    print(f"Tasa de servicio (mu)      : {MU:.2f} clientes/hora")
    print(f"Factor de utilización (rho): {rho:.2f} ({rho * 100:.1f}%)")

    if rho >= 1.0:
        print("[AVISO] rho >= 1: El sistema es inestable (la cola crecerá al infinito).")
        return

    # Entorno SimPy y recurso (servidor único)
    env = simpy.Environment()
    servidor = simpy.Resource(env, capacity=1)

    # Contenedores para métricas
    tiempos_espera = []
    tiempos_sistema = []

    # Iniciar generador y correr simulación
    env.process(generador_clientes(env, servidor, tiempos_espera, tiempos_sistema))
    env.run(until=TIEMPO_SIM)

    # Métricas empíricas (obtenidas de la simulación)
    n_atendidos = len(tiempos_espera)
    w_q_sim = sum(tiempos_espera) / n_atendidos
    w_sim = sum(tiempos_sistema) / n_atendidos
    l_q_sim = LAMBDA * w_q_sim  # Ley de Little: Lq = lambda * Wq
    l_sim = LAMBDA * w_sim      # Ley de Little: L = lambda * W

    # Métricas teóricas analíticas (fórmulas cerradas M/M/1)
    w_q_teo = LAMBDA / (MU * (MU - LAMBDA))
    w_teo = 1.0 / (MU - LAMBDA)
    l_q_teo = (LAMBDA ** 2) / (MU * (MU - LAMBDA))
    l_teo = LAMBDA / (MU - LAMBDA)

    # Impresión de resultados comparativos
    print("-" * 60)
    print(f"Duración simulada          : {TIEMPO_SIM} horas")
    print(f"Total de clientes atendidos: {n_atendidos}")
    print("-" * 60)
    print(f"{'Métrica':<35} | {'Simulado':>10} | {'Teórico':>10}")
    print("-" * 60)
    print(f"Tiempo medio en cola (Wq) [horas]  | {w_q_sim:>10.4f} | {w_q_teo:>10.4f}")
    print(f"Tiempo medio en sistema (W) [horas]| {w_sim:>10.4f} | {w_teo:>10.4f}")
    print(f"Promedio clientes en cola (Lq)     | {l_q_sim:>10.4f} | {l_q_teo:>10.4f}")
    print(f"Promedio clientes en sistema (L)   | {l_sim:>10.4f} | {l_teo:>10.4f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
