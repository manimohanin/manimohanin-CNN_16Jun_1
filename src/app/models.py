from django.db import models


class CleanImage(models.Model):
    image = models.ImageField(upload_to='train/clean')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class MessyImage(models.Model):
    image = models.ImageField(upload_to='train/messy')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class NotcrImage(models.Model):
    image = models.ImageField(upload_to='train/notcr')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CleanValidateImage(models.Model):
    image = models.ImageField(upload_to='validate/clean')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class MessyValidateImage(models.Model):
    image = models.ImageField(upload_to='validate/messy')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class NotcrValidateImage(models.Model):
    image = models.ImageField(upload_to='validate/notcr')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TestImage(models.Model):
    image = models.ImageField(upload_to='test', verbose_name='Uploaded Test Image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

