import axios from 'axios'

const BASE = '/api'

const api = axios.create({
  baseURL: BASE,
  timeout: 120000, // 2 min — AI analysis can take time
})

/** Analyze a GitHub repository */
export async function analyzeRepo(repoUrl) {
  const { data } = await api.post('/analyze', { repo_url: repoUrl })
  return data
}

/** Get results for a previously analyzed repo */
export async function getResults(repoId) {
  const { data } = await api.get(`/results/${repoId}`)
  return data
}

/** Get file tree for a repo */
export async function getFileTree(repoId) {
  const { data } = await api.get(`/filetree/${repoId}`)
  return data
}

/** Send a chat message about a repo */
export async function sendChatMessage(repoId, message) {
  const { data } = await api.post(`/chat/${repoId}`, { message })
  return data
}

/** List all analyzed repos (for dashboard) */
export async function listRepos() {
  const { data } = await api.get('/repos')
  return data
}

/** Delete a repo analysis */
export async function deleteRepo(repoId) {
  const { data } = await api.delete(`/repos/${repoId}`)
  return data
}
