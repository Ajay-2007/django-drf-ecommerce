# this file will be run first by pytest
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient


from .factories import CategoryFactory, BrandFactory, ProductFactory

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)


# pytest fixtures
@pytest.fixture
def api_client():
    return APIClient
