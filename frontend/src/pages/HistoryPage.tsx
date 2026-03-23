import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getHistory } from '../api/client'
import type { HistoryRecord } from '../types'

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('en-GB', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

const PREVIEW_LENGTH = 220

export default function HistoryPage() {
  const [records, setRecords] = useState<HistoryRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expanded, setExpanded] = useState<Set<string>>(new Set())

  useEffect(() => {
    getHistory()
      .then(setRecords)
      .catch((err: unknown) => setError(err instanceof Error ? err.message : 'Failed to load history.'))
      .finally(() => setLoading(false))
  }, [])

  function toggle(id: string) {
    setExpanded(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  return (
    <div className="page">
      <nav className="navbar">
        <Link to="/" className="nav-link">← Back</Link>
        <span className="brand">History</span>
        <span />
      </nav>

      <main className="main">
        {loading && <p className="status-msg">Loading…</p>}
        {error && <p className="error-msg">{error}</p>}
        {!loading && !error && records.length === 0 && (
          <p className="status-msg">No analyses yet. <Link to="/" className="nav-link">Upload a PDF</Link> to get started.</p>
        )}

        <ul className="history-list">
          {records.map(r => {
            const long = r.result.length > PREVIEW_LENGTH
            const isOpen = expanded.has(r.id)
            return (
              <li key={r.id} className="history-card">
                <div className="history-card-header">
                  <span className="history-filename">📄 {r.filename}</span>
                  <span className="file-meta">{formatDate(r.created_at)}</span>
                </div>
                <p className="history-result">
                  {isOpen || !long ? r.result : r.result.slice(0, PREVIEW_LENGTH) + '…'}
                </p>
                {long && (
                  <button className="btn-text" onClick={() => toggle(r.id)}>
                    {isOpen ? 'Show less' : 'Show more'}
                  </button>
                )}
              </li>
            )
          })}
        </ul>
      </main>
    </div>
  )
}

