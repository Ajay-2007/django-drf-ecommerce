from django.db import connection # to inspect queryset
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqliteConsoleLexer, SqlLexer
from sqlparse import format

from drf_spectacular.utils import extend_schema



from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """

    A Simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """

    A Simple Viewset for viewing all brands
    """

    queryset = Brand.objects.all()


    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """

    A Simple Viewset for viewing all products
    """

    queryset = Product.objects.all()



    lookup_field = 'slug'

    def retrieve(self, request, slug=None): # this is the function we are using when we return individual products
        # serializer = ProductSerializer(self.queryset.filter(slug=slug), many=True) # setup the query and run our filter
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related("category", "brand"), many=True
        ) # setup the query and run our filter, performing left outer join
        # we just trying to find the data related to our product in the category table

        # x = Response(serializer.data)

        # x = self.queryset.filter(slug=slug)
        # print(connection.queries)
        # sqlformatted = format(str(x.query), reindent=True)
        """
            SELECT "product_product"."id",
                "product_product"."name",
                "product_product"."slug",
                "product_product"."description",
                "product_product"."is_digital",
                "product_product"."brand_id",
                "product_product"."category_id",
                "product_product"."is_active"
            FROM "product_product"
            WHERE "product_product"."slug" = p3
        """
        # print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        data = Response(serializer.data)
        q = list(connection.queries)
        print(len(q))
        # for qs in q:
        #     sqlformatted = format(str(qs["sql"]), reindent=True)
        #     print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))


        return data


    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)


    @action(
        methods=["get"],
        detail=False, # it indicates if the current action is configured for the list or a detail view False means for list
        url_path=f"category/(?P<category>\w+)/all",
        # url_name="all",
    )
    def list_product_by_category(self, request, category=None):
        """
        An endpoint to return products by category
        """
        # query the category name for selecting products
        serializer = ProductSerializer(self.queryset.filter(category__name=category), many=True)
        return Response(serializer.data)