from django.contrib import admin
from django.db import models
from .models import Category, Tag, PostModel

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostModel)

