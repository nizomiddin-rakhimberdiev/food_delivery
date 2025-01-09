from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Foydalanuvchi uchun telefon raqam talab qilinadi")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser is_staff=True bo‘lishi kerak.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser is_superuser=True bo‘lishi kerak.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'admin'),
        ('customer', 'customer'),
        ('restaurant_owner', 'restaurant_owner'),
        ('delivery_person', 'delivery_person'),  # Yetkazib beruvchi roli
    )
    phone_number = models.CharField(max_length=15, unique=True)
    user_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLES, default='customer')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['address']
    def __str__(self):
        return self.phone_number
