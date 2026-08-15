import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Package, ShoppingCart, Receipt, Users } from 'lucide-react'

export default function DashboardPage() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const [products, orders, invoices, customers] = await Promise.all([
        api.get('/inventory/products/'),
        api.get('/sales/sales-orders/'),
        api.get('/sales/invoices/'),
        api.get('/sales/customers/'),
      ])
      return {
        products: products.data.count || 0,
        orders: orders.data.count || 0,
        invoices: invoices.data.count || 0,
        customers: customers.data.count || 0,
      }
    },
  })

  const statCards = [
    { title: 'Products', value: stats?.products || 0, icon: Package },
    { title: 'Sales Orders', value: stats?.orders || 0, icon: ShoppingCart },
    { title: 'Invoices', value: stats?.invoices || 0, icon: Receipt },
    { title: 'Customers', value: stats?.customers || 0, icon: Users },
  ]

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
