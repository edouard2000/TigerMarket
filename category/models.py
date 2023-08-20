from django.db import models

# // category model

class Category(models.Model):
    category_name = models.CharField(max_length= 50, unique=True)
    slug = models.CharField(max_length=100, unique = True)
    description = models.TextField(max_length= 255)
    cat_image = models.ImageField(upload_to = "photos/categories", blank=True)

def __str__(self):
    return self.category_name()
    