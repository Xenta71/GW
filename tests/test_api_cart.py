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
            assert any(item["item_id"] == 19071240 for item in response_data["cart"]["items"]), \
                "Товар с ID 19071240 не найден в корзине"

    @allure.title("Добавление товара ID 3017851315 в корзину")
    @allure.description("Проверка добавления другого товара в корзину в количестве 2 штук")
    def test_add_another_item_to_cart(self, auth_session):
        payload = {
            "item_id": 3017851315,
            "quantity": 2,
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
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
            response_data = response.json()

            # Проверка структуры ответа
            assert "cart" in response_data, "В ответе отсутствует информация о корзине"
            cart_items = response_data["cart"].get("items", [])

            # Поиск нужного товара
            target_item = next((item for item in cart_items if item["item_id"] == 3017851315), None)
            assert target_item is not None, "Товар с ID 3017851315 не найден в корзине"
            assert target_item["quantity"] == 2, \
                f"Ожидалось количество: 2, получено: {target_item['quantity']}"


class TestUpdateCartItem:
    @allure.title("Изменение количества товара в корзине")
    def test_update_item_quantity(self, auth_session, cart_with_item):
        # Фикстура гарантирует наличие товара в корзине
        update_payload = {"quantity": 4, "item_options": []}

        with allure.step("Отправка запроса на обновление количества"):
            update_response = auth_session.put(
                f"{BASE_URL}/v1/cart/{cart_with_item}?{urlencode(COMMON_QUERY_PARAMS)}",
                json=update_payload,
                timeout=10
            )

        with allure.step("Проверка ответа"):
            assert update_response.status_code == 200
            update_data = update_response.json()

            # Проверка обновленного количества
            updated_item = next(
                (item for item in update_data["cart"]["items"] if item["id"] == cart_with_item),
                None
            )
            assert updated_item is not None, "Элемент корзины не найден после обновления"
            assert updated_item["quantity"] == 4, \
                f"Ожидалось количество: 4, получено: {updated_item['quantity']}"


class TestCartCleanup:
    @allure.title("Полная очистка корзины через API v2")
    def test_clear_cart_completely(self, auth_session, prepared_cart):
        """
        Фикстура prepared_cart гарантирует наличие товара в корзине перед тестом
        """
        clear_params = COMMON_QUERY_PARAMS.copy()
        clear_params["screen"] = "checkout"

        with allure.step("1. Отправка запроса на очистку корзины"):
            clear_response = auth_session.delete(
                f"{BASE_URL}/v2/cart?{urlencode(clear_params)}",
                timeout=3
            )
            assert clear_response.status_code == 204

        with allure.step("2. Проверка что корзина пуста"):
            final_check = auth_session.get(
                f"{BASE_URL}/v1/cart?{urlencode(COMMON_QUERY_PARAMS)}",
                timeout=5
            )
            assert final_check.status_code == 200
            final_data = final_check.json()
            cart_items = final_data.get("cart", {}).get("items", [])
            assert len(cart_items) == 0, f"Корзина не пуста: {len(cart_items)} элементов"
