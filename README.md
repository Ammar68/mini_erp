# Mini ERP System

A multi-tenant SaaS ERP for small to medium businesses. Built with Django REST Framework backend and React + TypeScript frontend.

## Architecture

- **Backend**: Django 4.2 + Django REST Framework + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite + TanStack Query + Tailwind CSS + shadcn/ui
- **Multi-tenancy**: Row-level security via `company` foreign key on all business models
- **Admin**: Django Admin for subscription/company management

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for frontend development)

### Backend Setup

```bash
# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access admin at http://localhost:8000/admin
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:3000

## SaaS Multi-Tenancy

- Each `Company` represents a tenant
- Users belong to a `Company`
- All business data (vendors, products, invoices, etc.) is scoped to the user's company
- Superusers see all companies; regular users see only their own
- Subscriptions are managed via Django Admin (`Company.plan`, `subscription_expires_at`)

## Modules

- **Accounting**: Fiscal years, Chart of accounts, Journal entries
- **Purchases**: Vendors, Purchase orders, Bills, Bill payments
- **Sales**: Customers, Sales orders, Invoices, Payments
- **Inventory**: Products, Categories, Warehouses, Stock movements

## API Endpoints

```
/api/core/          - Authentication & users
/api/accounting/    - Chart of accounts, journal entries, fiscal years
/api/purchases/     - Vendors, purchase orders, bills
/api/sales/         - Customers, sales orders, invoices, payments
/api/inventory/     - Products, categories, warehouses, stock movements
```

## Development

```bash
# Backend
python manage.py runserver

# Frontend
cd frontend && npm run dev
```
