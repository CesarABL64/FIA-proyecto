"""
Escalada de Colina con Reinicios Aleatorios (Hill Climbing)
============================================================

Algoritmo de búsqueda local que parte de un estado inicial y se mueve
iterativamente al mejor vecino, siguiendo la dirección de mayor mejora
(menor valor de la función heurística).

Para evitar quedar atrapado en óptimos locales, se aplican reinicios
aleatorios: si no se encuentra solución, se genera un nuevo estado
aleatorio y se repite el proceso.

Aplicación clásica: problema de las 8 reinas.

Propiedades:
- Completo: con suficientes reinicios, sí (probabilísticamente)
- Óptimo: depende del problema; encuentra un óptimo local
- No garantiza solución global, pero es muy eficiente en memoria
"""

import random
from typing import List, Tuple, Optional


def heuristic(state: List[int]) -> int:
    """
    Cuenta el número de pares de reinas que se atacan entre sí.
    Dos reinas se atacan si comparten fila, columna o diagonal.
    """
    n = len(state)
    ataques = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Misma columna
            if state[i] == state[j]:
                ataques += 1
            # Misma diagonal
            elif abs(state[i] - state[j]) == abs(i - j):
                ataques += 1
    return ataques


def get_neighbors(state: List[int]) -> List[List[int]]:
    """
    Genera todos los vecinos: mover una reina a cualquier otra columna
    en su misma fila.
    """
    n = len(state)
    neighbors = []
    for row in range(n):
        for col in range(n):
            if state[row] != col:
                new_state = state[:]
                new_state[row] = col
                neighbors.append(new_state)
    return neighbors


def hill_climbing(n: int = 8, max_reinicios: int = 20) -> Optional[List[int]]:
    """
    Escalada de colina con reinicios aleatorios para N reinas.

    Parámetros:
        n:             número de reinas (default 8)
        max_reinicios: máximo de reinicios (default 20)

    Retorna:
        Estado solución (lista de n columnas), o None si no se encontró.
    """
    mejor_global = None
    mejor_ataques = float("inf")

    for reinicio in range(max_reinicios):
        # Generar estado inicial
        if reinicio == 0:
            state = [random.randint(0, n - 1) for _ in range(n)]
        else:
            state = [random.randint(0, n - 1) for _ in range(n)]

        ataques_actuales = heuristic(state)

        if ataques_actuales == 0:
            return state

        # Fase de mejora: moverse al mejor vecino mientras haya mejora
        while True:
            vecinos = get_neighbors(state)
            mejor_vecino = None
            mejores_ataques = ataques_actuales

            for vecino in vecinos:
                a = heuristic(vecino)
                if a < mejores_ataques:
                    mejores_ataques = a
                    mejor_vecino = vecino

            # Si ningún vecino mejora, terminar esta escalada
            if mejor_vecino is None:
                break

            state = mejor_vecino
            ataques_actuales = mejores_ataques

            if ataques_actuales == 0:
                return state

        # Actualizar mejor global encontrado
        if ataques_actuales < mejor_ataques:
            mejor_global = state[:]
            mejor_ataques = ataques_actuales

    return mejor_global


# ─── Ejemplo de uso ────────────────────────────────────────────────────────
if __name__ == "__main__":
    solucion = hill_climbing(n=8, max_reinicios=100)

    if solucion:
        print(f"Solución encontrada: {solucion}")
        print(f"Ataques: {heuristic(solucion)}")
    else:
        print("No se encontró solución perfecta.")
        if solucion:
            print(f"Mejor aproximación: {solucion} (ataques={heuristic(solucion)})")
