from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_employee = models.BooleanField('Is employee', default=False)
    is_therapist = models.BooleanField('Is therapist', default=False)
    is_educator = models.BooleanField('Is educator', default=False)

class Category(models.Model):
    category = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.category

class Schedule(models.Model):
    category = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.category

class Service(models.Model):
    category_id = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(null=True,)

    def __str__(self):
        return self.name
    
