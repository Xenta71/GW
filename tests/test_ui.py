import pytest
import time
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class TestYandexEda:
    BASE_URL = "https://eda.yandex.ru"

    @pytest.fixture(scope="function")
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)

        yield driver
        driver.quit()

    @pytest.fixture(scope="function")
    def auth_driver(self, driver):
        """Фикстура с обработкой попапов"""
        driver.get(self.BASE_URL)
        time.sleep(3)

        # Обработка попапа адреса
        try:
            yes_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Да')]")
                )
            )
            yes_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Не удалось обработать попап адреса: {str(e)}")

        yield driver

    @allure.title("Добавление товара из ресторана 'Тануки'")
    def test_add_from_tanuki(self, auth_driver):
        driver = auth_driver
        wait = WebDriverWait(driver, 20)
        actions = ActionChains(driver)

        with allure.step("1. Поиск ресторана 'Тануки'"):
            try:
                # Находим поле ввода поиска
                search_input = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "input[placeholder='Найти ресторан, блюдо или товар']"))
                )
                search_input.clear()
                search_input.send_keys("Тануки")

                # Нажимаем Enter для поиска
                search_input.send_keys(Keys.RETURN)
                time.sleep(3)

                # Кликаем на первый результат поиска
                first_result = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "(//*[contains(translate(., 'ТАНУКИ', 'тануки'), 'тануки')]/ancestor::a)[1]"))
                )
                first_result.click()
                time.sleep(3)
            except Exception as e:
                current_url = driver.current_url
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="search_failed",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail(f"Ошибка поиска ресторана: {str(e)}\nURL: {current_url}")

        with allure.step("2. Проверка статуса ресторана"):
            try:
                # Проверяем, не закрыт ли ресторан
                closed_banner = driver.find_elements(By.XPATH, "//*[contains(., 'закрыт')]")

                if closed_banner:
                    # Если ресторан закрыт, пропускаем тест
                    pytest.skip("Ресторан закрыт, невозможно добавить товар")

                # Если ресторан открыт - проверяем наличие поиска в ресторане
                wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder='Найти в ресторане']"))
                )
            except Exception as e:
                current_url = driver.current_url
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="restaurant_page_not_loaded",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail(f"Страница ресторана не загрузилась: {str(e)}\nURL: {current_url}")

        with allure.step("3. Поиск 'Ролл Филадельфия' внутри ресторана"):
            try:
                # Локатор для поиска внутри ресторана
                restaurant_search = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//input[@placeholder='Найти в ресторане']"))
                )
                restaurant_search.clear()
                restaurant_search.send_keys("Ролл Филадельфия")
                restaurant_search.send_keys(Keys.RETURN)
                time.sleep(2)  # Краткая пауза для обновления результатов

                # Клик по найденному товару
                dish_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@aria-label, 'Ролл Филадельфия')]"))
                )
                dish_button.click()

                # Ожидание добавления в корзину
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[contains(text(), 'Ролл Филадельфия')]"))
                )
            except Exception as e:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="dish_search_failed",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail(f"Ошибка поиска блюда: {str(e)}")

        with allure.step("4. Проверка корзины"):
            try:
                # Открытие корзины
                cart_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@href, '/cart')]"))
                )
                cart_button.click()

                # Ожидание загрузки корзины
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//div[contains(text(), 'Ролл Филадельфия')]"))
                )

                # Проверка наличия товара
                dish_in_cart = driver.find_element(
                    By.XPATH, "//div[contains(text(), 'Ролл Филадельфия')]")
                assert dish_in_cart.is_displayed(), "Товар не найден в корзине"

                # Проверка суммы
                total_price = driver.find_element(
                    By.XPATH, "//span[contains(@class, 'cart-total-price')]").text
                assert "820" in total_price, f"Сумма заказа {total_price} не соответствует 820 ₽"

                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="cart_verification",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="cart_check_failed",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail(f"Ошибка проверки корзины: {str(e)}")