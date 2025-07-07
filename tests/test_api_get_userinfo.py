import pytest
import allure
import requests


@allure.feature("API Яндекс Еды")
@allure.story("Профиль пользователя")
class TestUserProfileAPI:
    @allure.title("Получение информации профиля")
    @allure.description("Проверка получения данных профиля авторизованного пользователя")
    def test_get_user_profile(self):
        # 1. Подготовка тестовых данных
        base_url = "https://eda.yandex.ru/api/v1"
        endpoint = "/user/profile"
        cookies =

        headers =

        with allure.step("1. Отправка GET-запроса для получения профиля"):
            response = requests.get(
                f"{base_url}{endpoint}",
                cookies=cookies,
                headers=headers
            )

        with allure.step("2. Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("3. Проверка структуры ответа"):
            profile_data = response.json()

            # Проверяем основные поля профиля
            required_fields = [
                'email', 'first_name', 'phone_number',
                'passport_uid', 'uuid', 'has_delivered_orders'
            ]

            for field in required_fields:
                assert field in profile_data, f"Отсутствует обязательное поле {field}"

            # Проверка формата email
            assert "@" in profile_data["email"], "Email имеет неверный формат"

            # Проверка формата телефона
            assert profile_data["phone_number"].startswith("+"), "Телефон должен начинаться с +"
            assert len(profile_data["phone_number"]) > 5, "Телефон слишком короткий"

        with allure.step("4. Проверка времени ответа"):
            assert response.elapsed.total_seconds() < 1.0, "Время ответа превышает 1 секунду"
