from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Company(models.Model):
    PLAN_CHOICES = (
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='starter')
    is_active = models.BooleanField(default=True)
    subscription_expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    is_company_admin = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
