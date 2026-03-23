import { useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { analyzePdf } from '../api/client'
import type { AnalyzeResponse } from '../types'

const MAX_SIZE_MB = 50

function validate(file: File): string | null {
  if (!file.name.toLowerCase().endsWith('.pdf')) return 'Only PDF files are accepted.'
  if (file.size > MAX_SIZE_MB * 1024 * 1024) return `File must be under ${MAX_SIZE_MB} MB.`
  return null
}

export default function UploadPage() {
  const inputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalyzeResponse | null>(null)
  const [dragOver, setDragOver] = useState(false)

  function pick(f: File) {
    const err = validate(f)
    if (err) { setError(err); setFile(null); return }
    setError(null)
    setFile(f)
    setResult(null)
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      setResult(await analyzePdf(file))
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <nav className="navbar">
        <span className="brand">PDF Analyzer</span>
        <Link to="/history" className="nav-link">History →</Link>
      </nav>

      <main className="main">
        <form onSubmit={handleSubmit} className="upload-card">
          <div
            className={`drop-zone${dragOver ? ' drag-over' : ''}${file ? ' has-file' : ''}`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault()
              setDragOver(false)
              const f = e.dataTransfer.files[0]
              if (f) pick(f)
            }}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".pdf"
              hidden
              onChange={(e) => { const f = e.target.files?.[0]; if (f) pick(f) }}
            />
            {file ? (
              <>
                <span className="drop-icon">📄</span>
                <span className="file-name">{file.name}</span>
                <span className="file-meta">{(file.size / 1024 / 1024).toFixed(1)} MB</span>
              </>
            ) : (
              <>
                <span className="drop-icon">⬆</span>
                <span className="drop-label">Drop PDF here or <strong>click to browse</strong></span>
                <span className="file-meta">Max 50 MB · PDF only</span>
              </>
            )}
          </div>

          {error && <p className="error-msg">{error}</p>}

          <button type="submit" className="btn-primary" disabled={!file || loading}>
            {loading && <span className="spinner" />}
            {loading ? 'Analyzing…' : 'Analyze PDF'}
          </button>
        </form>

        {result && (
          <div className="result-card">
            <div className="result-header">
              <span className="result-filename">📄 {result.filename}</span>
            </div>
            <div className="result-body">{result.summary}</div>
          </div>
        )}
      </main>
    </div>
  )
}

