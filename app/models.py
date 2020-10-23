from django.db import models


# Create your models here.
class Product(models.Model):

    ref = models.TextField()

    # to verify
    # images = models.TextField()

    characteristics = models.JSONField()
    popularity = models.IntegerField()

    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)


class Filter(models.Model):
    characteristics = models.JSONField()
    # characteristics = {cpu: "checkbox"}
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)


class Details(models.Model):
    price = models.FloatField()
    owner = models.TextField()
    name = models.TextField()
    characteristics = models.JSONField()

    product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)


class Category(models.Model):
    name = models.TextField()
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True)
