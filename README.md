# Visualizador de Algoritmos de Búsqueda

Aplicación web interactiva que permite visualizar y comparar algoritmos de búsqueda aplicados a cuatro tipos clásicos de problemas de inteligencia artificial.

![Tech](https://img.shields.io/badge/frontend-React_+_Vite_+_Tailwind-61DAFB?logo=react)
![Tech](https://img.shields.io/badge/backend-Python_+_FastAPI-009688?logo=fastapi)

## Tabla de Contenidos

- [Sobre el proyecto](#sobre-el-proyecto)
- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Problemas y algoritmos](#problemas-y-algoritmos)
- [Uso de la aplicación](#uso-de-la-aplicación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [API del backend](#api-del-backend)
- [Extensión del proyecto](#extensión-del-proyecto)

## Sobre el proyecto

Este proyecto fue desarrollado con fines didácticos para la materia de Fundamentos de Inteligencia Artificial. Su objetivo es demostrar de forma visual cómo operan distintos tipos de algoritmos de búsqueda sobre problemas clásicos.

La aplicación permite:
- Seleccionar un problema y el algoritmo correspondiente
- Ejecutar la búsqueda
- **Visualizar paso a paso** el proceso (nodos explorados, frontera, camino solución)
- Ver métricas de rendimiento (nodos expandidos, costo, tiempo de ejecución)
- Ajustar parámetros como tamaño de cuadrícula o nivel de dificultad

## Requisitos

- **Python** 3.10+
- **Node.js** 18+

## Instalación y ejecución

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

El servidor arranca en `http://localhost:8000`. La documentación automática de la API está en `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

El frontend arranca en `http://localhost:5173`. Las peticiones a `/api` se redirigen automáticamente al backend (`vite.config.js`).

> El backend debe estar corriendo antes del frontend para que funcione la comunicación.

## Problemas y algoritmos

| Problema | Tipo de búsqueda | Algoritmos | Descripción |
|----------|-----------------|------------|-------------|
| **Frozen Lake** | No informada | BFS, DFS | Cuadrícula 4×4 a 6×6. El agente debe llegar del inicio a la meta evitando hoyos. |
| **Sokoban** | Informada | A\*, GBFS | Puzle de empujar cajas a posiciones objetivo. 3 niveles de dificultad. |
| **8 Reinas** | Local | Hill Climbing | Colocar 8 reinas en un tablero sin que se ataquen. Usa reinicio aleatorio si se estanca. |
| **Tic-Tac-Toe** | Adversaria | MiniMax | Árbol de juego del gato. Muestra la evaluación MiniMax de cada jugada posible. |

### Resumen de algoritmos

| Algoritmo | Clase | Estrategia |
|-----------|-------|------------|
| **BFS** | `bfs.py` | Cola FIFO — explora nivel por nivel |
| **DFS** | `dfs.py` | Pila LIFO — explora en profundidad |
| **A\*** | `a_star.py` | f(n) = g(n) + h(n) — cola de prioridad |
| **GBFS** | `gbfs.py` | Solo h(n) — cola de prioridad voraz |
| **Hill Climbing** | `hill_climbing.py` | Búsqueda local — mejor vecino + reinicios |
| **MiniMax** | `minimax.py` | Árbol adversario — profundidad limitada a 6 |

## Uso de la aplicación

1. **Selecciona un problema** en los recuadros superiores
2. **Elige un algoritmo** de los botones que aparecen
3. Ajusta parámetros (tamaño de cuadrícula para Frozen Lake, nivel para Sokoban)
4. Presiona **"Ejecutar búsqueda"**
5. Usa los controles de animación:
   - ▶ Play / Pause — reproduce o pausa automáticamente
   - ◀ ▶ Step — avanza o retrocede manualmente
   - Slider de velocidad — ajusta la rapidez de la animación
   - Barra de progreso — salta a cualquier paso
6. Observa las **métricas** al final

### Leyenda de colores

Cada tablero usa un esquema de colores para mostrar visualmente:
- Celdas exploradas, frontera de búsqueda y nodo actual
- Camino solución resaltado
- Conflicto en 8 Reinas, cajas en meta en Sokoban, etc.

## Estructura del proyecto

```
Proyecto final/
├── backend/
│   ├── main.py                    # Punto de entrada de FastAPI
│   ├── requirements.txt
│   ├── algorithms/                # Algoritmos (clases independientes)
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── a_star.py
│   │   ├── gbfs.py
│   │   ├── hill_climbing.py
│   │   └── minimax.py
│   ├── problems/                  # Definición de problemas
│   │   ├── frozen_lake.py         # Cuadrícula, hoyos, meta
│   │   ├── sokoban.py             # Niveles, paredes, cajas
│   │   ├── eight_queens.py        # Tablero, conflictos
│   │   └── tic_tac_toe.py         # Tablero 3x3, evaluación
│   └── routes/
│       └── search.py              # Endpoints de la API REST
├── frontend/
│   ├── vite.config.js             # Proxy /api → backend
│   ├── index.html
│   └── src/
│       ├── App.jsx                # Componente principal
│       ├── index.css              # Tailwind + estilos globales
│       ├── components/
│       │   ├── ProblemSelector.jsx
│       │   ├── AlgorithmSelector.jsx
│       │   ├── AnimationControls.jsx
│       │   ├── MetricsPanel.jsx
│       │   └── boards/            # Tableros de visualización
│       │       ├── FrozenLakeBoard.jsx
│       │       ├── SokobanBoard.jsx
│       │       ├── EightQueensBoard.jsx
│       │       └── TicTacToeBoard.jsx
│       └── services/
│           └── api.js             # Cliente HTTP (axios)
└── AGENTS.md                      # Guía para desarrollo con IA
```

## API del backend

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/problems` | Lista problemas y algoritmos disponibles |
| `GET` | `/api/problems/frozen-lake/grids` | Cuadrículas predefinidas (4×4, 5×5, 6×6) |
| `GET` | `/api/problems/sokoban/levels` | Niveles predefinidos (1, 2, 3) |
| `POST` | `/api/search` | Ejecuta un algoritmo sobre un problema |

**Ejemplo de petición POST /api/search:**

```json
{
  "problem": "frozen_lake",
  "algorithm": "bfs",
  "params": { "grid_size": 4 }
}
```

**Respuesta:**

```json
{
  "steps": [
    {
      "current": [0, 0],
      "explored": [[0, 0]],
      "frontier": [[0, 1], [1, 0]],
      "description": "Expandiendo...",
      ...
    }
  ],
  "solution": { "path": [[0,0], [0,1], ...], "actions": ["right", ...] },
  "metrics": {
    "nodes_expanded": 15,
    "path_cost": 6,
    "execution_time_ms": 23,
    "path_length": 7
  }
}
```

## Extensión del proyecto

### Agregar un nuevo algoritmo

1. Crea una clase en `backend/algorithms/` con un método `search()`
2. La clase recibe un `problem` en su constructor
3. Retorna `{ steps: [...], solution: {...}, metrics: {...} }`
4. Registra el algoritmo en `routes/search.py` (PROBLEM_ALGORITHMS y el `if` de ejecución)

### Agregar un nuevo problema

1. Crea una clase en `backend/problems/` que implemente la interfaz:
   - `get_start_state()`, `is_goal(state)`, `get_actions(state)`, `heuristic(state)`
2. Registra el problema en `routes/search.py`
3. Crea un componente de visualización en `frontend/src/components/boards/`
4. Agrega la serialización correspondiente en `serialize_step()` y el manejo de solución
