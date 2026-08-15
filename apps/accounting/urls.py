from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'fiscal-years', views.FiscalYearViewSet)
router.register(r'chart-of-accounts', views.ChartOfAccountViewSet)
router.register(r'journal-entries', views.JournalEntryViewSet)

app_name = 'accounting'
urlpatterns = router.urls
