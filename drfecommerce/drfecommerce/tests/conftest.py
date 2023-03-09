# this file will be run first by pytest
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient


from .factories import CategoryFactory, BrandFactory, ProductFactory, ProductLineFactory, ProductImageFactory

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory) # to access ProductLineFactory we have to call product_line_factory
register(ProductImageFactory)


# pytest fixtures
@pytest.fixture
def api_client():
    return APIClient
