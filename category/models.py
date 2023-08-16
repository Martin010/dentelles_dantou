from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name   = models.CharField(max_length=128, unique=True)
    slug            = models.SlugField(max_length=128, unique=True)
    description     = models.TextField(max_length=255, blank=True)
    category_image  = models.ImageField(upload_to='photos/categories', blank=True)

    # Display "categories" in the Django administrator instead of "categorys"
    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'

    # # Return the category's url with its own slug
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
