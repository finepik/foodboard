from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Product(models.Model):
    name_product = models.CharField(max_length=15)
    total_count = models.IntegerField()
    calories = models.IntegerField()

    # avatar = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    # user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.name_product

    def safe_get(self, search):
        try:
            product = self.objects.get(name_product=search)
        except ObjectDoesNotExist:
            product = None
        return product


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    product_number = models.IntegerField()
    calories = models.IntegerField()
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET(None), null=True)
    product = models.ManyToManyField(Product, verbose_name='Эталонный продукт')

    def __str__(self):
        return self.title


class About_user(models.Model):
    level = models.CharField(max_length=80)
    description = models.CharField(max_length=80)
    avatar = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    favorite_recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.level


class User_product(models.Model):
    name_product = models.CharField(max_length=15)
    total_count = models.IntegerField()
    calories = models.IntegerField()
    # avatar = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Эталонный продукт', on_delete=models.SET(None), null=True)

    def __str__(self):
        return self.name_product
