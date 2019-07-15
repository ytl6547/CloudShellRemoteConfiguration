from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime

class Device(models.Model):
    # _id = models.
    id = models.CharField(max_length=255, primary_key=True)
    # name = models.CharField(max_length=255)
    lastAccessTime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.id

class Port(models.Model):
    originalPort = models.CharField(max_length=255, primary_key=True)
    transferedPort = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()
#
#     def __str__(self):
#         return self.name
#
# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#
#     def __str__(self):
#         return self.name
#
# class Entry(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField()
#     mod_date = models.DateField()
#     authors = models.ManyToManyField(Author)
#     n_comments = models.IntegerField()
#     n_pingbacks = models.IntegerField()
#     rating = models.IntegerField()
#
#     def __str__(self):
#         return self.headline