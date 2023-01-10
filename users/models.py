from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import reverse

# Create your models here.


class User(AbstractBaseUser):
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    followers = models.ManyToManyField("self")
    following = models.ManyToManyField("self")
    profile_image = models.TextField()
    USERNAME_FIELD = 'nickname'

