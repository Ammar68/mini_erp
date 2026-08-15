from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

app_name = 'core'
urlpatterns = [
    path('login/', obtain_auth_token, name='token_obtain'),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
]

urlpatterns += router.urls
