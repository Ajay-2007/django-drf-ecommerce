import factory
import pytest
import json

from drfecommerce.product.models import Category

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:

    endpoint = "/api/category/"


    def test_category_get(self, category_factory, api_client):
        # Arrange
        # x = category_factory(name="test_cat")
        # create 4 new record in our test database
        category_factory.create_batch(4, is_active=True)
        # Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        # print(json.loads(response.content))
        assert len(json.loads(response.content)) == 4





class TestProductEndpoints:
    endpoint = "/api/product/"


    # def test_return_all_products(self, product_factory, api_client):
    #     # Arrange
    #     # create 4 new record in our test database
    #     product_factory.create_batch(4)
    #     # Act
    #     response = api_client().get(self.endpoint)
    #     # Assert
    #     assert response.status_code == 200
    #     # print(json.loads(response.content))
    #     assert len(json.loads(response.content)) == 4

    def test_return_single_product_by_slug(self, product_factory, api_client):
        obj = product_factory(slug="test-slug")
        # product_factory(category=obj)
        response = api_client().get(f"{self.endpoint}{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1


    def test_return_products_by_category_slug(self, category_factory, product_factory, api_client):
        obj = category_factory(slug="test-slug")
        product_factory(category=obj)
        response = api_client().get(f"{self.endpoint}category/{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1