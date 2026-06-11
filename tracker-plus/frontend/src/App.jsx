import { BrowserRouter, Routes, Route } from 'react-router-dom'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<div>Dashboard (a implementar)</div>} />
        <Route path="/stats" element={<div>Stats (a implementar)</div>} />
      </Routes>
    </BrowserRouter>
  )
}
