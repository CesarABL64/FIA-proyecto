"""
Búsqueda en Profundidad (DFS - Depth-First Search)
===================================================

Algoritmo de búsqueda no informada que explora un grafo en profundidad:
avanza hasta un nodo terminal antes de retroceder (backtracking).
Utiliza una pila LIFO (o recursión).

Propiedades:
- Completo: solo en espacios de estados finitos (o si se controla ciclos)
- Óptimo: no (no garantiza camino más corto)
- Complejidad temporal: O(b^m) donde m = profundidad máxima
- Complejidad espacial: O(b·m) con pila explícita

Ventaja: consume poca memoria comparado con BFS.
"""

from typing import List, Tuple, Optional


def dfs(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Encuentra un camino en una cuadrícula usando DFS (pila explícita).

    A diferencia de BFS, DFS puede encontrar un camino más largo primero.
    """
    filas, columnas = len(grid), len(grid[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Pila LIFO para expansión
    frontera = [start]
    vino_de = {start: None}
    visitados = {start}

    while frontera:
        actual = frontera.pop()       # ← LIFO: último en entrar, primero en salir

        if actual == goal:
            return reconstruir_camino(vino_de, goal)

        for dr, dc in direcciones:
            nr, nc = actual[0] + dr, actual[1] + dc
            vecino = (nr, nc)

            if (0 <= nr < filas and 0 <= nc < columnas
                    and grid[nr][nc] == 0
                    and vecino not in visitados):
                visitados.add(vecino)
                frontera.append(vecino)
                vino_de[vecino] = actual

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

    resultado = dfs(laberinto, inicio, meta)

    if resultado:
        print(f"Camino encontrado ({len(resultado)} pasos): {resultado}")
        print("Nota: DFS no garantiza el camino más corto.")
    else:
        print("No se encontró camino.")
