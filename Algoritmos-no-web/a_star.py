"""
A* (A-Estrella)
===============

Algoritmo de búsqueda informada que combina BFS (costo acumulado g)
con una heurística (estimación h) para guiar la búsqueda.

f(n) = g(n) + h(n)

- g(n): costo real desde el inicio hasta el nodo n
- h(n): costo estimado desde n hasta la meta (heurística)
- f(n): costo total estimado del camino que pasa por n

Propiedades:
- Completo: sí
- Óptimo: sí (si la heurística es admisible: nunca sobreestima)
- El más eficiente entre los óptimos con heurística consistente.

Heurística utilizada: distancia Manhattan
  h((r,c), meta) = |r - r_meta| + |c - c_meta|
"""

import heapq
from typing import List, Tuple, Optional


def distancia_manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Distancia Manhattan entre dos celdas (movimiento en 4 direcciones)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Encuentra el camino óptimo en una cuadrícula usando A*.

    Parámetros:
        grid:  matriz 2D (0 = libre, 1 = obstáculo)
        start: coordenadas de inicio
        goal:  coordenadas de la meta

    Retorna:
        Lista de coordenadas del camino óptimo, o None si no hay solución.
    """
    filas, columnas = len(grid), len(grid[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # g(n): costo real desde el inicio
    g_score = {start: 0}

    # Contador para desempate en la cola de prioridad
    contador = 0

    # Cola de prioridad: (f, contador, nodo)
    frontera = [(distancia_manhattan(start, goal), contador, start)]

    vino_de = {start: None}

    # Conjuntos para tracking
    en_frontera = {start}

    while frontera:
        _, _, actual = heapq.heappop(frontera)
        en_frontera.discard(actual)

        if actual == goal:
            return reconstruir_camino(vino_de, goal)

        for dr, dc in direcciones:
            nr, nc = actual[0] + dr, actual[1] + dc
            vecino = (nr, nc)

            if not (0 <= nr < filas and 0 <= nc < columnas):
                continue
            if grid[nr][nc] == 1:
                continue

            # g tentativo: costo desde inicio pasando por 'actual'
            g_tentativo = g_score[actual] + 1

            if vecino not in g_score or g_tentativo < g_score[vecino]:
                vino_de[vecino] = actual
                g_score[vecino] = g_tentativo
                f = g_tentativo + distancia_manhattan(vecino, goal)

                if vecino not in en_frontera:
                    contador += 1
                    heapq.heappush(frontera, (f, contador, vecino))
                    en_frontera.add(vecino)

    return None


def reconstruir_camino(vino_de: dict, meta: Tuple[int, int]) -> List[Tuple[int, int]]:
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = vino_de[actual]
    camino.reverse()
    return camino


# ─── Ejemplo de uso ────────────────────────────────────────────────────────
if __name__ == "__main__":
    laberinto = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    inicio = (0, 0)
    meta = (4, 4)

    resultado = a_star(laberinto, inicio, meta)

    if resultado:
        print(f"Camino óptimo encontrado ({len(resultado)} pasos): {resultado}")
    else:
        print("No se encontró camino.")
