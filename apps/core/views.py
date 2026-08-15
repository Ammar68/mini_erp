from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserSerializer
from .mixins import TenantQuerySetMixin

User = get_user_model()


class UserViewSet(TenantQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = User.objects.all()
        user = self.request.user
        if user.is_superuser:
            return queryset
        company = getattr(user, 'company', None)
        if company:
            return queryset.filter(company=company)
        return queryset.none()


class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
