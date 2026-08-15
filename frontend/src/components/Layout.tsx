import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import {
  LayoutDashboard,
  BookOpen,
  ShoppingCart,
  Receipt,
  Package,
  LogOut,
} from 'lucide-react'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/accounting', icon: BookOpen, label: 'Accounting' },
  { to: '/purchases', icon: ShoppingCart, label: 'Purchases' },
  { to: '/sales', icon: Receipt, label: 'Sales' },
  { to: '/inventory', icon: Package, label: 'Inventory' },
]

export default function Layout() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 border-r bg-card">
        <div className="p-6">
          <h1 className="text-xl font-bold">Mini ERP</h1>
        </div>
        <nav className="px-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                }`
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="absolute bottom-4 left-4">
          <Button variant="ghost" size="sm" onClick={handleLogout}>
            <LogOut className="h-4 w-4 mr-2" />
            Logout
          </Button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
