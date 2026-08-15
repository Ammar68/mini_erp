from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'sales-orders', views.SalesOrderViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'payments', views.PaymentViewSet)

app_name = 'sales'
urlpatterns = router.urls
