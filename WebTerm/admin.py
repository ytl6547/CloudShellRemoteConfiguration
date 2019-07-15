from django.contrib import admin

# Register your models here.
from .models import Device
from .models import Port

admin.site.register(Device)
admin.site.register(Port)