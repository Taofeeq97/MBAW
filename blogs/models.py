from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.title
    
    def uploaded_by(self):
        full_name = self.created_by.first_name + " " + self.created_by.last_name
        return full_name if full_name.strip() else self.created_by.username

    class Meta:
        ordering = ['-created_at']


class Subscriber(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']



class JobApplication(models.Model):
    job_title = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    cover_letter = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to='resume')

    def __str__(self):
        return f"{self.job_title} job application by {self.full_name}"

