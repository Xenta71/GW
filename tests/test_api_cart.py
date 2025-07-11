import allure
from urllib.parse import urlencode
from config import BASE_URL, COMMON_QUERY_PARAMS

class TestAddToCartAPI:
    @allure.title("Добавление ролла Филадельфия в корзину")
    def test_add_philadelphia_roll_to_cart(self, auth_session):
        payload = {
            "item_id": 19071240,
            "quantity": 1,
            "place_slug": "tanyki576_mp",
            "place_business": "restaurant",
            "item_options": []
        }

        with allure.step("Отправка запроса на добавление в корзину"):
            response = auth_session.post(
                f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
                json=payload,
                timeout=10
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            response_data = response.json()
            assert "cart" in response_data
            assert any(item["item_id"] == 19071240 for item in response_data["cart"]["items"])

    @allure.title("Добавление товара ID 3017851315 в корзину")
    @allure.description("Проверка добавления другого товара в корзину в количестве 2 штук")
    def test_add_another_item_to_cart(self, auth_session):
        payload = {
            "item_id": 3017851315,  # ID другого товара
            "quantity": 2,  # Количество 2 штуки
            "place_slug": "tanyki576_mp",
            "place_business": "restaurant",
            "item_options": []
        }

        with allure.step("1. Отправка запроса на добавление в корзину"):
            response = auth_session.post(
                f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
                json=payload,
                timeout=10
            )

        with allure.step("2. Проверка ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

            response_data = response.json()
            assert "cart" in response_data, "В ответе отсутствует информация о корзине"

            # Проверяем что товар добавлен с правильным ID и количеством
            found = False
            for item in response_data["cart"]["items"]:
                if item["item_id"] == 3017851315:
                    assert item["quantity"] == 2, f"Количество товара должно быть 2, получено {item['quantity']}"
                    found = True
                    break

            assert found, "Товар с ID 3017851315 не найден в корзине"

class TestUpdateCartItem:
    @allure.title("Изменение количества товара в корзине")
    def test_update_item_quantity(self, auth_session):
        add_payload = {
            "item_id": 19071240,
            "quantity": 1,
            "place_slug": "tanyki576_mp",
            "place_business": "restaurant",
            "item_options": []
        }

        add_response = auth_session.post(
            f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
            json=add_payload
        )
        add_data = add_response.json()
        item_id = next(item["id"] for item in add_data["cart"]["items"] if item["item_id"] == 19071240)

        update_payload = {"quantity": 4, "item_options": []}

        with allure.step("Отправка запроса на обновление количества"):
            update_response = auth_session.put(
                f"{BASE_URL}/v1/cart/{item_id}?{urlencode(COMMON_QUERY_PARAMS)}",
                json=update_payload,
                timeout=10
            )

        with allure.step("Проверка ответа"):
            assert update_response.status_code == 200
            update_data = update_response.json()
            updated_item = next(item for item in update_data["cart"]["items"] if item["id"] == item_id)
            assert updated_item["quantity"] == 4


class TestCartCleanup:
    @allure.title("Полная очистка корзины через API v2")
    def test_clear_cart_completely(self, auth_session):
        add_payload = {
            "item_id": 19071240,
            "quantity": 1,
            "place_slug": "tanyki576_mp",
            "place_business": "restaurant",
            "item_options": []
        }

        auth_session.post(
            f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
            json=add_payload
        )

        clear_params = COMMON_QUERY_PARAMS.copy()
        clear_params["screen"] = "checkout"

        with allure.step("Отправка DELETE запроса для очистки корзины"):
            clear_response = auth_session.delete(
                f"{BASE_URL}/v2/cart?{urlencode(clear_params)}",
                timeout=10
            )

        with allure.step("Проверка ответа на очистку"):
            assert clear_response.status_code == 204
            assert not clear_response.content

        with allure.step("Проверка пустой корзины"):
            final_check = auth_session.get(
                f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
                timeout=10
            )
            final_data = final_check.json()
            cart_items = final_data.get("cart", {}).get("items", [])
            assert len(cart_items) == 0