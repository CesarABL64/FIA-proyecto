"""
Búsqueda Voraz Primero el Mejor (GBFS - Greedy Best-First Search)
==================================================================

Algoritmo de búsqueda informada que siempre expande el nodo que
*parece* más cercano a la meta según una heurística h(n).

A diferencia de A*, NO considera el costo acumulado g(n).
Solo ordena la frontera por h(n).

Propiedades:
- Completo: no (puede entrar en bucles si no usa visitados)
- Óptimo: no (la heurística puede engañarlo hacia caminos sub-óptimos)
- Complejidad: similar a A* en el mejor caso, pero generalmente más rápido
  (aunque puede explorar caminos muy largos si la heurística falla)

Ventaja: muy rápido cuando la heurística es buena.
Desventaja: no garantiza optimalidad.
"""

import heapq
from typing import List, Tuple, Optional


def distancia_manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def gbfs(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Búsqueda voraz: expande el nodo con menor h(n) (más cercano a la meta).

    En cada iteración, elige de la frontera el nodo con menor valor
    heurístico, sin importar cuánto costó llegar a él.
    """
    filas, columnas = len(grid), len(grid[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    contador = 0

    # Frontera: (heurística, contador, nodo)  — sin g(n)
    h_inicio = distancia_manhattan(start, goal)
    frontera = [(h_inicio, contador, start)]

    vino_de = {start: None}
    visitados = set()
    en_frontera = {start}

    while frontera:
        _, _, actual = heapq.heappop(frontera)

        if actual in visitados:
            continue

        en_frontera.discard(actual)
        visitados.add(actual)

        if actual == goal:
            return reconstruir_camino(vino_de, goal)

        for dr, dc in direcciones:
            nr, nc = actual[0] + dr, actual[1] + dc
            vecino = (nr, nc)

            if (0 <= nr < filas and 0 <= nc < columnas
                    and grid[nr][nc] == 0
                    and vecino not in visitados
                    and vecino not in vino_de):
                vino_de[vecino] = actual
                h = distancia_manhattan(vecino, goal)
                contador += 1
                heapq.heappush(frontera, (h, contador, vecino))
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

    resultado = gbfs(laberinto, inicio, meta)
    # Comparar con el camino óptimo de A* o BFS

    if resultado:
        print(f"Camino encontrado ({len(resultado)} pasos): {resultado}")
        print("Nota: GBFS no garantiza el camino óptimo. Compara con A*.")
    else:
        print("No se encontró camino.")
