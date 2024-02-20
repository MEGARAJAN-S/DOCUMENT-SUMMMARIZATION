from django.db import models

# Create your models here.
class login(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=30)

class FileUpload(models.Model):
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='file')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AudioUpload(models.Model):
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='audio')
    uploaded_at = models.DateTimeField(auto_now_add=True)