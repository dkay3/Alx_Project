# products/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image_url = models.URLField(max_length=500, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # Optional: Add a foreign key to the user who created the product
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name
