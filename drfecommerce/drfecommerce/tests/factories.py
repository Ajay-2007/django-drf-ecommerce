import factory

from drfecommerce.product.models import Category, Brand, Product, ProductLine, ProductImage, ProductType


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # name = "test_category"
    name = factory.Sequence(lambda n: "Category_%d" % n)



class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    # name = "test_brand"
    name = factory.Sequence(lambda n: "Brand_%d" % n)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "test_type"

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    # should you have two products that needs the same name
    name = "test_product"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test alternative text"
    url = "test.jpg"
    productline = factory.SubFactory(ProductLineFactory)

