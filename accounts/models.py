from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from phone_field import PhoneField

# Create your models here.
class State(models.Model):
  state = models.CharField(verbose_name='State', max_length=20, unique=True)

  def __str__(self):
    return self.state
class User(AbstractUser):
  email = models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')
  state = models.ForeignKey(State,verbose_name='State', on_delete=models.CASCADE, blank=True, null=True)
  city = models.CharField(verbose_name='City', max_length=20, blank=True, null=True)
  address = models.CharField(verbose_name='Address', max_length=50, blank=True, null=True)
  zipcode = models.CharField(verbose_name='Zip Code',max_length=5, blank=True, null=True)
  phone_number = PhoneField(blank=True)