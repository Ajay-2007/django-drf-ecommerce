from rest_framework import serializers

from .models import Brand, Category, Product, ProductLine


# all the data will be serialized and returned to the frontend
class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name") # getting the name from category model

    class Meta:
        model = Category
        # fields = "__all__" # what data we return to the client
        # fields = ["name"]
        fields = ["category_name"] # it will just return the category_name in the json response


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        # fields = "__all__" # what data we return to the client
        exclude = ('id', ) # we can just exclude particular field


# move it front of the ProductSerializer in order to use it in ProductSerializer
class ProductLineSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = ProductLine
        # fields = "__all__" # what data we return to the client
        exclude = ('id', "is_active", "product") # we can just exclude particular field


class ProductSerializer(serializers.ModelSerializer):
    # brand = BrandSerializer() # foreignkey relationship
    brand_name = serializers.CharField(source='brand.name')
    # category = CategorySerializer()
    category_name = serializers.CharField(source='category.name') # we are able to do this because there is category field within the Product table
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        # fields = "__all__" # what data we return to the client
        # exclude = ('id', ) # we can just exclude particular field
        fields = ("name", "slug", "description", "brand_name", "category_name", "product_line") # specify what we want to include, in order


