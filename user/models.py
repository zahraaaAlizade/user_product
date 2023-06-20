import uuid
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    password = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
