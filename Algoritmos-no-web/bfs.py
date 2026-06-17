"""
Búsqueda en Anchura (BFS - Breadth-First Search)
=================================================

Algoritmo de búsqueda no informada que explora un grafo nivel por nivel.
Utiliza una cola FIFO para expandir nodos en orden de descubrimiento.

Propiedades:
- Completo: sí (si el espacio de estados es finito)
- Óptimo: sí (encuentra el camino más corto en grafos no ponderados)
- Complejidad temporal: O(b^d) donde b = factor de ramificación, d = profundidad
- Complejidad espacial: O(b^d)

Ideal para problemas donde el costo entre nodos es uniforme.
"""

from collections import deque
from typing import List, Tuple, Optional


def bfs(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Encuentra el camino más corto en una cuadrícula usando BFS.

    Parámetros:
        grid:  matriz 2D donde 0 = libre, 1 = obstáculo
        start: coordenadas (fila, columna) de inicio
        goal:  coordenadas (fila, columna) de la meta

    Retorna:
        Lista de coordenadas del camino, o None si no hay solución.
    """
    filas, columnas = len(grid), len(grid[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha

    # Cola FIFO para los nodos por expandir
    frontera = deque([start])

    # Para reconstruir el camino: de dónde vine y qué acción tomé
    vino_de = {start: None}

    # Conjunto de visitados para evitar ciclos
    visitados = {start}

    while frontera:
        actual = frontera.popleft()

        # Meta alcanzada -> reconstruir y devolver camino
        if actual == goal:
            return reconstruir_camino(vino_de, goal)

        # Expandir vecinos
        for dr, dc in direcciones:
            nr, nc = actual[0] + dr, actual[1] + dc
            vecino = (nr, nc)

            # Verificar límites, obstáculos y si ya fue visitado
            if (0 <= nr < filas and 0 <= nc < columnas
                    and grid[nr][nc] == 0
                    and vecino not in visitados):
                visitados.add(vecino)
                frontera.append(vecino)
                vino_de[vecino] = actual

    # No se encontró camino
    return None


def reconstruir_camino(vino_de: dict, meta: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Reconstruye el camino desde la meta hasta el inicio."""
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = vino_de[actual]
    camino.reverse()
    return camino


# ─── Ejemplo de uso ────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 0 = libre, 1 = obstáculo
    laberinto = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    inicio = (0, 0)
    meta = (4, 4)

    resultado = bfs(laberinto, inicio, meta)

    if resultado:
        print(f"Camino encontrado ({len(resultado)} pasos): {resultado}")
    else:
        print("No se encontró camino.")
