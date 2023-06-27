from django.db import models
from django.urls import reverse

from category.models import Category


class Product(models.Model):
    product_name    = models.CharField(max_length=256, unique=True)
    slug            = models.SlugField(max_length=256, unique=True)
    description     = models.TextField(max_length=512, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    # Return the product's url with the category slug and its own slug
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def colors(self):
        # Return colors from the products variation
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        # Return sizes from the products size
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'couleur'),
    ('size', 'taille'),
)


class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=128, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=128)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
