from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import CustomUser
from blogs.models import Category


class QuestionModel(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255)
    content = RichTextUploadingField(config_name='non_admin')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class AnswerModel(models.Model):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name='answers')
    answer = RichTextUploadingField(config_name='non_admin')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RequestModel(models.Model):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name='requests')
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    created_by= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
