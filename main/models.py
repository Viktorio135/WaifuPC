from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("Either email or phone must be set")
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email or self.phone
    


def photo_works_upload_path(instance, filename):
    return f'works/{filename}'


class Works(models.Model):
    photo = models.ImageField(upload_to=photo_works_upload_path)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.description[:50] + ('...' if len(self.description) > 50 else '')


    class Meta:
        verbose_name = "Пример работы"
        verbose_name_plural = "Примеры работы"

class Builds(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')
    
    class Meta:
        verbose_name = "Индивидуальный сброки"
        verbose_name_plural = "Индивидуальный сброки"

class Repair(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')
    
    class Meta:
        verbose_name = "Ремонт"
        verbose_name_plural = "Ремонт"

class TradeIn(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')
    
    class Meta:
        verbose_name = "Trade-In"
        verbose_name_plural = "Trade-In"


class Contacts(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')
    
    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"