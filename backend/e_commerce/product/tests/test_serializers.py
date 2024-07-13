import pytest

from product.serializers import ProductSerializer

@pytest.fixture
def sample_product():
    return {
        "name": "Chair",
        "main_price": "200",
        "description": "A furniture for sitting"
    }

def test_product_correct_representation():
    pass