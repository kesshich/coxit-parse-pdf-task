import type { AnalyzeResponse, HistoryRecord } from '../types'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1'

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail ?? `Request failed: ${res.status}`)
  }
  return res.json()
}

export async function analyzePdf(file: File): Promise<AnalyzeResponse> {
  const form = new FormData()
  form.append('file', file)

  const res = await fetch(`${BASE_URL}/pdf/analyze`, { method: 'POST', body: form })
  return handleResponse<AnalyzeResponse>(res)
}

export async function getHistory(): Promise<HistoryRecord[]> {
  const res = await fetch(`${BASE_URL}/history/`)
  return handleResponse<HistoryRecord[]>(res)
}

