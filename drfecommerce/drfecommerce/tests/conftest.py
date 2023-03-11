# this file will be run first by pytest
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient


from .factories import (
    CategoryFactory,
    # BrandFactory, ProductFactory, ProductLineFactory, ProductImageFactory, AttributeFactory, AttributeValueFactory, ProductTypeFactory
)

register(CategoryFactory)
# register(BrandFactory)
# register(ProductFactory)
# register(ProductLineFactory) # to access ProductLineFactory we have to call product_line_factory
# register(ProductImageFactory)
# register(ProductTypeFactory)
# register(AttributeFactory)
# register(AttributeValueFactory)


# pytest fixtures
@pytest.fixture
def api_client():
    return APIClient
