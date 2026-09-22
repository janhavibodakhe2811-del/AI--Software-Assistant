import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Results from './pages/Results'
import Chat from './pages/Chat'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950">
      <Navbar />
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/results/:repoId" element={<Results />} />
          <Route path="/chat/:repoId" element={<Chat />} />
        </Routes>
      </main>
    </div>
  )
}
