from django.db import models

class Device(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    lastAccessTime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.id

class Port(models.Model):
    originalPort = models.CharField(max_length=255, primary_key=True)
    transferedPort = models.CharField(max_length=255)
    available = models.BooleanField(default=True)