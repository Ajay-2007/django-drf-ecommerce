from rest_framework import serializers

from .models import Brand, Category, Product, ProductLine


# all the data will be serialized and returned to the frontend
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = "__all__" # what data we return to the client
        fields = ["name"]


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
        exclude = ('id', ) # we can just exclude particular field


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer() # foreignkey relationship
    category = CategorySerializer()
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        # fields = "__all__" # what data we return to the client
        exclude = ('id', ) # we can just exclude particular field


