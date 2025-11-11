"""
Account models.
Following Single Responsibility Principle - models contain only data structure.
"""
from django.db import models
from django.conf import settings
from core.models import BaseModel


class Profile(BaseModel):
    """
    User profile model.
    Inherits from BaseModel for timestamps and soft delete functionality.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self) -> str:
        return f'Profile for user {self.user.username}'
    
    class Meta:
        db_table = 'accounts_profile'