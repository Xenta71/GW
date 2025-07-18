import pytest
import requests
from urllib.parse import urlencode
import sys
import os
# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import BASE_URL, TEST_COOKIES, TEST_HEADERS, COMMON_QUERY_PARAMS

@pytest.fixture
def auth_session():
    session = requests.Session()
    session.cookies.update(TEST_COOKIES)
    session.headers.update(TEST_HEADERS)
    yield session
    session.close()


@pytest.fixture(autouse=True)
def cart_cleanup(auth_session):
    """Автоматическая очистка корзины после каждого теста"""
    yield
    clear_params = COMMON_QUERY_PARAMS.copy()
    clear_params["screen"] = "checkout"

    auth_session.delete(
        f"{BASE_URL}/v2/cart?{urlencode(clear_params)}",
        timeout=3
    )


@pytest.fixture
def cart_with_item(auth_session):
    """Фикстура добавляет тестовый товар в корзину и возвращает cart_item_id"""
    payload = {
        "item_id": 19071240,
        "quantity": 1,
        "place_slug": "tanyki576_mp",
        "place_business": "restaurant",
        "item_options": []
    }

    response = auth_session.post(
        f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
        json=payload,
        timeout=5
    )

    if response.status_code == 200:
        cart_data = response.json()
        for item in cart_data.get("cart", {}).get("items", []):
            if item.get("item_id") == 19071240:
                return item.get("id")


@pytest.fixture
def prepared_cart(auth_session):
    """Фикстура добавляет тестовый товар в корзину перед тестом"""
    payload = {
        "item_id": 19071240,
        "quantity": 1,
        "place_slug": "tanyki576_mp",
        "place_business": "restaurant",
        "item_options": []
    }

    auth_session.post(
        f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
        json=payload,
        timeout=5
    )
