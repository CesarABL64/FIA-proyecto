import axios from 'axios'

const API_URL = import.meta.env.PROD ? '/_/backend/api' : '/api'

export async function getProblems() {
  const res = await axios.get(`${API_URL}/problems`)
  return res.data
}

export async function getFrozenLakeGrids() {
  const res = await axios.get(`${API_URL}/problems/frozen-lake/grids`)
  return res.data
}

export async function getSokobanLevels() {
  const res = await axios.get(`${API_URL}/problems/sokoban/levels`)
  return res.data
}

export async function runSearch(problem, algorithm, params = {}) {
  const res = await axios.post(`${API_URL}/search`, {
    problem,
    algorithm,
    params,
  })
  return res.data
}