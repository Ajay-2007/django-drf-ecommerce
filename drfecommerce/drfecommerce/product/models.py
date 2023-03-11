from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField


# # creating a custom manager
# class ActiveManager(models.Manager):
#     # we want to provide some override to the queryset
#     # to filterout any products that are not currently active
#     # override and provide an additional filter
#     # def get_queryset(self):
#     #     return super().get_queryset().filter(is_active=True)
#     def isactive(self):
#         return self.get_queryset().filter(is_active=True)


class IsActiveQueryset(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

class Category(MPTTModel):
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    # if we do wanna delete anything, we wanna delete all the child category first, before we delete any parent category
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    objects = IsActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=235)
    slug = models.SlugField(max_length=255) # slug is a mandatory field
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    # the product not necessary depend on the category so on_delete, would be SET_NULL
    category = TreeForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    # product_type = models.ForeignKey("ProductType", on_delete=models.PROTECT)

    is_active = models.BooleanField(default=False)
    objects = IsActiveQueryset.as_manager()
    created_at = models.DateTimeField(
        auto_now_add=True, # save the time and date when the product was added
        editable=False,
    )

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="attribute_value"
    )

    def __str__(self):
        return f"{self.attribute.name}-{self.attribute_value}"



class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av" # we don't want to have same related name twice
    )
    product_line = models.ForeignKey(
        'ProductLine', # we can reference it before the the class definition
        on_delete=models.CASCADE,
        related_name="product_attribute_value_pl"
    )


    class Meta:
        unique_together = ("attribute_value", "product_line", )


    def clean(self):
        qs = (
            ProductLineAttributeValue.objects.filter(
                attribute_value=self.attribute_value)
            .filter(product_line=self.product_line)
            .exists()
        )

        if not qs:
            # grab all the attributes that is associated with the particular product line
            iqs = Attribute.objects.filter(attribute_value__product_line_attribute_value=self.product_line).values_list("pk", flat=True) # we use __ to traverse to the next table

            if self.attribute_value.attribute.id in list(iqs):
                raise ValidationError("Duplicate attributes exists")

    def save(self, *args, **kwargs):
        # on save now we are running full_clean, meaning clean method
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


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
    order = OrderField(unique_for_field="product", blank=True) # we want to run our query on the product field only
    # ordering number will only be related to a product

    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )

    objects = IsActiveQueryset.as_manager()

    def clean(self):
        # this is gonna checked for every line
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order: # means there is duplicate
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        # on save now we are running full_clean, meaning clean method
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)



class ProductImage(models.Model):

    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    # related_name django can use it to built that reverse foreign key relationship in our serializer
    order = OrderField(unique_for_field="productline", blank=True) # we want to run our query on the product field only


    def clean(self):
        # this is gonna checked for every line
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order: # means there is duplicate
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        # on save now we are running full_clean, meaning clean method
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order)


class ProductType(models.Model):

    name = models.CharField(max_length=100)

    attribute = models.ManyToManyField(
        Attribute,
        through="ProductTypeAttribute",
        related_name="product_type_attribute",
    )

    def __str__(self):
        return str(self.name)


class ProductTypeAttribute(models.Model):


    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_pt" # we don't want to have same related name twice
    )

    attribute = models.ForeignKey(
        Attribute, # we can reference it before the the class definition
        on_delete=models.CASCADE,
        related_name="product_type_attribute_a"
    )


    class Meta:
        unique_together = ("product_type", "attribute", ) # unique_together prevents adding duplicate entries in the database

