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
    """Фикстура для авторизованной сессии"""
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

    try:
        auth_session.delete(
            f"{BASE_URL}/v2/cart?{urlencode(clear_params)}",
            timeout=10
        )
    except Exception as e:
        print(f"Ошибка при очистке корзины: {str(e)}")
