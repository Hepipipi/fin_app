from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]


    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(str(self.name)))
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.type})"



class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="records")
    name = models.CharField(max_length=40)
    price = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Category: {self.category}, Record: {self.name}, Price: {self.price}, Date: {self.date}"



















