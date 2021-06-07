from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User




class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        if not self.parent:
            return f"{self.name}"
        else:
            return f"{self.parent} --> {self.name}"

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', null=True)






