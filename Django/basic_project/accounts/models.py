from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    condition = models.TextField(max_length=200)
    name = models.TextField(max_length=20)
    grade = models.IntegerField()