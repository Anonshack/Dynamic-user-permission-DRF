from django.contrib.auth.models import AbstractUser
from django.db import models


class Myapp(models.Model):
    title = models.CharField(max_length=255)


class MyUser(AbstractUser):
    USERNAME_FIELD = "username"
