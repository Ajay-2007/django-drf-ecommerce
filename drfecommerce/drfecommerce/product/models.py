from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    # if we do wanna delete anything, we wanna delete all the child category first, before we delete any parent category
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]


    def __str__(self):
        return self.name


class Brand(models.Model):
    # brand needs to be unique
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255) # slug is a mandatory field
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # the product not necessary depend on the category so on_delete, would be SET_NULL
    category = TreeForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)

    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.name



class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_line" # we can specify the name that can make things little bit readable, we will use this data to reference this data to build the reverse foreign key relationship
    )
    is_active = models.BooleanField(default=False)