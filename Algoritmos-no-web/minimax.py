"""
MiniMax (Tic-Tac-Toe / Tres en Raya)
=====================================

Algoritmo de búsqueda adversarial para juegos de suma cero con dos jugadores.
Explora el árbol de juego asumiendo que:

- MAX (X) elige la jugada que maximiza su beneficio.
- MIN (O) elige la jugada que minimiza el beneficio de MAX.

Utiliza recursión para evaluar todos los movimientos posibles hasta
alcanzar estados terminales (victoria, derrota o empate).

Propiedades:
- Completo: sí (explora todo el árbol de juego de Tic-Tac-Toe)
- Óptimo: sí (juego perfecto)
- Complejidad: O(b^d) donde b ≈ 9-d, d = profundidad restante
  (9! ≈ 362,880 estados en Tic-Tac-Toe)

Este algoritmo es la base de motores de ajedrez modernos (con poda α-β).
"""

from typing import List, Tuple, Optional


def hay_ganador(board: List[List[str]]) -> Optional[str]:
    """Devuelve 'X', 'O' si hay ganador, o None."""
    # Filas
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] and board[r][0] != ' ':
            return board[r][0]
    # Columnas
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] and board[0][c] != ' ':
            return board[0][c]
    # Diagonales
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None


def tablero_lleno(board: List[List[str]]) -> bool:
    """True si no quedan espacios vacíos."""
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                return False
    return True


def get_acciones(board: List[List[str]]) -> List[Tuple[int, int]]:
    """Devuelve lista de (fila, columna) de casillas vacías."""
    acciones = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                acciones.append((r, c))
    return acciones


def minimax(board: List[List[str]], es_maximizando: bool) -> Tuple[Optional[Tuple[int, int]], int]:
    """
    Algoritmo MiniMax recursivo.

    Parámetros:
        board:          tablero 3x3 actual
        es_maximizando: True si es turno de X (MAX), False si es O (MIN)

    Retorna:
        (mejor_jugada, valor)
        - valor =  1 si gana X
        - valor = -1 si gana O
        - valor =  0 si empate
    """
    # Casos base: estado terminal
    ganador = hay_ganador(board)
    if ganador == 'X':
        return None, 1
    elif ganador == 'O':
        return None, -1
    elif tablero_lleno(board):
        return None, 0

    acciones = get_acciones(board)
    if not acciones:
        return None, 0

    if es_maximizando:
        # Turno de X: maximizar
        mejor_valor = float("-inf")
        mejor_jugada = None
        for (r, c) in acciones:
            board[r][c] = 'X'
            _, valor = minimax(board, False)
            board[r][c] = ' '                    # deshacer jugada
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_jugada = (r, c)
        return mejor_jugada, mejor_valor
    else:
        # Turno de O: minimizar
        mejor_valor = float("inf")
        mejor_jugada = None
        for (r, c) in acciones:
            board[r][c] = 'O'
            _, valor = minimax(board, True)
            board[r][c] = ' '                    # deshacer jugada
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_jugada = (r, c)
        return mejor_jugada, mejor_valor


def mejor_movimiento(board: List[List[str]], jugador: str) -> Optional[Tuple[int, int]]:
    """
    Calcula el mejor movimiento para el jugador dado usando MiniMax.
    """
    jugada, _ = minimax(board, jugador == 'X')
    return jugada


# ─── Ejemplo de uso ────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Turno de X en un tablero casi vacío
    tablero = [
        [' ', ' ', ' '],
        [' ', 'X', ' '],
        [' ', ' ', 'O'],
    ]

    print("Tablero actual:")
    for fila in tablero:
        print(fila)

    jugada = mejor_movimiento(tablero, 'X')
    print(f"\nMejor jugada para X: {jugada}")

    if jugada:
        r, c = jugada
        tablero[r][c] = 'X'
        print("Tablero después del movimiento:")
        for fila in tablero:
            print(fila)
        ganador = hay_ganador(tablero)
        if ganador:
            print(f"¡{ganador} gana!")
