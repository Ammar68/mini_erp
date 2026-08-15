from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'stock-movements', views.StockMovementViewSet)

app_name = 'inventory'
urlpatterns = router.urls
