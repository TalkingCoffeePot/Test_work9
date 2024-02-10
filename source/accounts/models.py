from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(AbstractUser):
    name = models.CharField('Имя', max_length=100, blank=True, null=True)
    info = models.TextField('Инфо', max_length=1000, blank=True, null=True)
    number = models.IntegerField('Номер телефона', blank=True, null=True)

    def __str__(self):
        return self.username