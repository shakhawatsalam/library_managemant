from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.


class User(AbstractUser):
    username = None
    name = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    
    
    
