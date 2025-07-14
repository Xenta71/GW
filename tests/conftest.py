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

    # ПОСЛЕ теста: очистка корзины
    clear_params = COMMON_QUERY_PARAMS.copy()
    clear_params["screen"] = "checkout"

    try:
        session.delete(
            f"{BASE_URL}/v2/cart?{urlencode(clear_params)}",
            timeout=3
        )
    except Exception as e:
        print(f"Ошибка при очистке корзины: {str(e)}")

    session.close()


@pytest.fixture
def cart_with_item(auth_session):
    """
    Фикстура добавляет тестовый товар в корзину и возвращает cart_item_id.
    Не делает никаких проверок - просто добавляет товар.
    """
    payload = {
        "item_id": 19071240,
        "quantity": 1,
        "place_slug": "tanyki576_mp",
        "place_business": "restaurant",
        "item_options": []
    }

    try:
        response = auth_session.post(
            f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            cart_data = response.json()
            # Пытаемся извлечь ID элемента корзины
            for item in cart_data.get("cart", {}).get("items", []):
                if item.get("item_id") == 19071240:
                    return item.get("id")
    except Exception:
        pass

    # Возвращаем None если не удалось добавить
    return None


@pytest.fixture
def prepared_cart(auth_session):
    """
    Фикстура просто добавляет товар в корзину перед тестом
    и ничего не возвращает. Используется для теста очистки.
    """
    payload = {
        "item_id": 19071240,
        "quantity": 1,
        "place_slug": "tanyki576_mp",
        "place_business": "restaurant",
        "item_options": []
    }

    try:
        auth_session.post(
            f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
            json=payload,
            timeout=5
        )
    except Exception:
        pass