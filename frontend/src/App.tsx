import { Routes, Route } from 'react-router-dom'
import UploadPage from './pages/UploadPage'
import HistoryPage from './pages/HistoryPage'
import './App.css'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<UploadPage />} />
      <Route path="/history" element={<HistoryPage />} />
    </Routes>
  )
}
