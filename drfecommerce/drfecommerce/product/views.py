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

from django.db.models import Prefetch



from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """

    A Simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)



class ProductViewSet(viewsets.ViewSet):
    """

    A Simple Viewset for viewing all products
    """

    # queryset = Product.objects.all()
    # queryset = Product.isactive.all()
    # queryset = Product.objects.isactive() # isactive is now a method which can be accessed through the manager
    queryset = Product.objects.all().is_active() # isactive is now a method which can be accessed through the queryset manager



    lookup_field = 'slug'

    def retrieve(self, request, slug=None): # this is the function we are using when we return individual products
        # serializer = ProductSerializer(self.queryset.filter(slug=slug), many=True) # setup the query and run our filter
        serializer = ProductSerializer(
            Product.objects.filter(slug=slug)
            .select_related("category", )
            # .prefetch_related(Prefetch("product_line"))
            .prefetch_related(Prefetch("product_line__product_image")) # to do reverse foreign key look up we have to do double underscore, it will fetch all of the product_image at once
            .prefetch_related(Prefetch("product_line__attribute_value__attribute"))
            , many=True,
        ) # setup the query and run our filter, performing left outer join
        # we just trying to find the data related to our product in the category table
        # select_related performs sql join behind the scene

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
                "product_product"."category_id",
                "product_product"."is_active"
            FROM "product_product"
            WHERE "product_product"."slug" = p3
        """
        # print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        data = Response(serializer.data)
        # q = list(connection.queries)
        # print(len(q))
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
        url_path=f"category/(?P<slug>[\w-]+)",
        # url_name="all",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint to return products by category
        """
        # query the category name for selecting products
        serializer = ProductSerializer(self.queryset.filter(category__slug=slug), many=True)
        return Response(serializer.data)