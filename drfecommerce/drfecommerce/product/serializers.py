from rest_framework import serializers

from .models import Brand, Category, Product, ProductImage, ProductLine, Attribute, AttributeValue, ProductType


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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "productline")


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("name", "id",)


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ("attribute", "attribute_value", )

# move it front of the ProductSerializer in order to use it in ProductSerializer
class ProductLineSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # product_image = ProductImageSerializer(many=True) # multiple images
    attribute_value = AttributeValueSerializer(many=True) # we have many attributes return


    class Meta:
        model = ProductLine
        # fields = "__all__" # what data we return to the client
        # exclude = ('id', "is_active", "product") # we can just exclude particular field
        fields = (
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
            "attribute_value",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["attribute"]["id"] : key["attribute_value"]})
        data.update({"specification": attr_values})
        return data



class ProductSerializer(serializers.ModelSerializer):
    # brand = BrandSerializer() # foreignkey relationship
    brand_name = serializers.CharField(source='brand.name')
    # category = CategorySerializer()
    category_name = serializers.CharField(source='category.name') # we are able to do this because there is category field within the Product table
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = "__all__" # what data we return to the client
        # exclude = ('id', ) # we can just exclude particular field
        fields = (
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
            "attribute"
        ) # specify what we want to include, in order


    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["id"] : key["name"]})
        data.update({"type specification": attr_values})
        return data

