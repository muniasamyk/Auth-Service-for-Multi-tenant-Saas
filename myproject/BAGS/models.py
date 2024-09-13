from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import json

class Organization(models.Model):
    name = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    personal = models.BooleanField(default=False, null=True, blank=True)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile = models.JSONField(default=dict)
    status = models.IntegerField(default=0)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Member(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)
