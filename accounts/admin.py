from django.contrib import admin
from django.db import models
from .models import CustomUser, Like, History

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Like)
admin.site.register(History)