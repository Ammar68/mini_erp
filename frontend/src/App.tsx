import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from '@/components/Layout'
import LoginPage from '@/pages/LoginPage'
import DashboardPage from '@/pages/DashboardPage'

function App() {
  const token = localStorage.getItem('token')
  
  return (
    <Routes>
      <Route path="/login" element={token ? <Navigate to="/" /> : <LoginPage />} />
      <Route path="/" element={token ? <Layout /> : <Navigate to="/login" />}>
        <Route index element={<DashboardPage />} />
        <Route path="accounting/*" element={<div className="p-6">Accounting Module</div>} />
        <Route path="purchases/*" element={<div className="p-6">Purchases Module</div>} />
        <Route path="sales/*" element={<div className="p-6">Sales Module</div>} />
        <Route path="inventory/*" element={<div className="p-6">Inventory Module</div>} />
      </Route>
    </Routes>
  )
}

export default App
