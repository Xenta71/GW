import pytest
import requests
import allure
from urllib.parse import urlencode
import json


@pytest.fixture(scope="module")
def authorized_session():
    """Фикстура для авторизованной сессии"""
    session = requests.Session()

    # Установка cookies
    session.cookies.update()

    # Заголовки
    session.headers.update()

    yield session
    session.close()


@pytest.fixture
def base_url():
    return "https://eda.yandex.ru/api"


@pytest.fixture
def common_params():
    return {
        "longitude": 43.90708,
        "latitude": 56.33089,
        "screen": "menu",
        "shippingType": "delivery",
        "autoTranslate": "false"
    }


class TestAddToCartAPI:
    @allure.title("Добавление ролла Филадельфия в корзину")
    def test_add_philadelphia_roll_to_cart(self, authorized_session, base_url, common_params):
        payload = {
            "item_id": 19071240,
            "quantity": 1,
            "place_slug": "tanyki576_mp",
            "place_business": "restaurant",
            "item_options": []
        }

        with allure.step("1. Отправка запроса на добавление в корзину"):
            try:
                response = authorized_session.post(
                    f"{base_url}/v1/cart?{urlencode(common_params)}",
                    json=payload,
                    timeout=10
                )
                response.raise_for_status()
            except Exception as e:
                pytest.fail(f"Ошибка запроса: {str(e)}")

            # Логирование для отладки
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("2. Проверка ответа"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

            try:
                response_data = response.json()
            except ValueError:
                pytest.fail("Невалидный JSON в ответе")

            assert isinstance(response_data, dict), "Ответ должен быть JSON-объектом"
            assert "cart" in response_data, "В ответе отсутствует информация о корзине"
            assert any(
                item["item_id"] == 19071240 for item in response_data["cart"]["items"]), "Товар не добавлен в корзину"

class TestUpdateCartItem:
    @allure.title("Изменение количества товара в корзине")
    def test_update_item_quantity(self, authorized_session, base_url, common_params):
        # Сначала добавляем товар в корзину
        add_payload = {
            "item_id": 19071240,
            "quantity": 1,
            "place_slug": "tanyki576_mp",
            "place_business": "restaurant",
            "item_options": []
        }

        add_response = authorized_session.post(
            f"{base_url}/v1/cart?{urlencode(common_params)}",
            json=add_payload
        )
        add_data = add_response.json()
        item_id = next(item["id"] for item in add_data["cart"]["items"] if item["item_id"] == 19071240)

        # Теперь обновляем количество
        update_payload = {
            "quantity": 4,
            "item_options": []
        }

        with allure.step("1. Отправка запроса на обновление количества"):
            update_response = authorized_session.put(
                f"{base_url}/v1/cart/{item_id}?{urlencode(common_params)}",
                json=update_payload,
                timeout=10
            )

        with allure.step("2. Проверка ответа"):
            assert update_response.status_code == 200
            update_data = update_response.json()
            updated_item = next(item for item in update_data["cart"]["items"] if item["id"] == item_id)
            assert updated_item["quantity"] == 4, "Количество товара не обновилось"

    @allure.title("Добавление другого товара в корзину")
    def test_add_another_item_to_cart(self, authorized_session, base_url, common_params):
        payload = {
            "item_id": 3017851315,  # Другой товар
            "quantity": 2,
            "place_slug": "tanyki576_mp",
            "place_business": "restaurant",
            "item_options": []
        }

        with allure.step("1. Отправка запроса на добавление в корзину"):
            response = authorized_session.post(
                f"{base_url}/v1/cart?{urlencode(common_params)}",
                json=payload,
                timeout=10
            )

        with allure.step("2. Проверка ответа"):
            assert response.status_code == 200
            response_data = response.json()
            assert any(
                item["item_id"] == 3017851315 for item in response_data["cart"]["items"]), "Товар не добавлен в корзину"

class TestCartCleanup:
    @allure.title("Полная очистка корзины через API v2")
    def test_clear_cart_completely(self, authorized_session, base_url, common_params):
        # Шаг 1: Отправляем запрос на полную очистку корзины
        with allure.step("1. Отправка DELETE запроса для очистки корзины"):
            clear_params = {
                "longitude": common_params["longitude"],
                "latitude": common_params["latitude"],
                "screen": "checkout",
                "shippingType": "delivery",
                "autoTranslate": "false"
            }

            clear_response = authorized_session.delete(
                f"{base_url}/v2/cart?{urlencode(clear_params)}",
                timeout=10
            )

            # Проверки ответа
            assert clear_response.status_code == 204, (
                f"Ожидался статус 204 No Content, получен {clear_response.status_code}"
            )
            assert not clear_response.content, "Тело ответа должно быть пустым"

        # Шаг 2: Проверяем что корзина пуста
        with allure.step("2. Проверка пустой корзины"):
            final_check = authorized_session.get(
                f"{base_url}/v1/cart?{urlencode(common_params)}",
                timeout=10
            )
            final_data = final_check.json()

            # Проверка через безопасный доступ к данным
            cart_items = final_data.get("cart", {}).get("items", [])
            assert len(cart_items) == 0, (
                f"Корзина не пуста после очистки. Найдены товары: {cart_items}"
            )

        # Дополнительное логирование для отладки
        allure.attach(
            f"DELETE запрос на очистку корзины:\n"
            f"URL: {base_url}/v2/cart\n"
            f"Параметры: {clear_params}\n"
            f"Статус: {clear_response.status_code}",
            name="Детали очистки корзины",
            attachment_type=allure.attachment_type.TEXT
        )