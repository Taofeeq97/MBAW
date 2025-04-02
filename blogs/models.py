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