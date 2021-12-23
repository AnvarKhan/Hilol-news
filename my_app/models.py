from django.db import models


# Create your models here.


class Category(models.Model):
    """Categoriyalar"""
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class News(models.Model):
    """yangiliklar blogi"""
    title = models.CharField(max_length=250, null=False, blank=False)
    image = models.ImageField(upload_to='images/', blank=True)
    text = models.TextField(null=False, blank=False)
    category = models.ForeignKey(
        Category, blank=False,
        null=True,
        on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title