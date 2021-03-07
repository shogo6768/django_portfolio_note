from django.contrib import admin
from django.db import models
from .models import QuestionModel, AnswerModel, RequestModel

# Register your models here.
admin.site.register(QuestionModel)
admin.site.register(AnswerModel)
admin.site.register(RequestModel)