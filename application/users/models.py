from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("Email address"), unique=True)
    phone = models.CharField(_("Phone Number"), max_length=15, unique=True, null=True, blank=True)  # New phone field
    location = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    social_links = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)  # New image field
    password = models.CharField(_("Password"), max_length=128)  # Explicit password field (not necessary if inheriting from AbstractUser)
