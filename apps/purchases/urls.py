from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vendors', views.VendorViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'bills', views.BillViewSet)
router.register(r'bill-payments', views.BillPaymentViewSet)

app_name = 'purchases'
urlpatterns = router.urls
