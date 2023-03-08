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
        fields = "__all__" # what data we return to the client


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer() # foreignkey relationship
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__" # what data we return to the client


class ProductLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = ProductLine
        fields = "__all__" # what data we return to the client
