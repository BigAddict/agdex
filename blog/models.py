from django.contrib.auth.models import User
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Departments"
    
    def __str__(self) -> str:
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='blog/thumbnails')
    short_description = models.TextField(max_length=200)
    created_on = models.DateField(auto_now_add=True)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title
    