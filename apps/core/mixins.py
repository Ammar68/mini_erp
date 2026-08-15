from rest_framework import viewsets, permissions


class TenantQuerySetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        company = getattr(user, 'company', None)
        if company:
            return queryset.filter(company=company)
        return queryset.none()
    
    def perform_create(self, serializer):
        company = getattr(self.request.user, 'company', None)
        if company and not self.request.user.is_superuser:
            serializer.save(company=company, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)
