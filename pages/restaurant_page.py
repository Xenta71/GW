from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class RestaurantPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Добавить '{item_name}' в корзину")
    def add_to_cart(self, item_name):
        item_locator = (By.XPATH, f"//div[contains(@class, 'menu-item') and .//span[contains(text(), '{item_name}')]]")
        price_locator = (By.XPATH, f"{item_locator[1]}//span[contains(@class, 'price')]")

        item = self.wait.until(EC.visibility_of_element_located(item_locator))
        price = float(item.find_element(*price_locator).text.replace('₽', '').strip())

        add_button = item.find_element(By.XPATH, ".//button[contains(@class, 'add-button')]")
        add_button.click()

        return price

    @allure.step("Проверить корзину")
    def verify_cart_contains(self, item_name, expected_price):
        cart_item = (By.XPATH, f"//div[contains(@class, 'cart-item')]//span[contains(text(), '{item_name}')]")
        cart_total = (By.CSS_SELECTOR, "span[data-testid='cart-total-price']")

        self.wait.until(EC.visibility_of_element_located(cart_item))
        total_price = float(self.driver.find_element(*cart_total).text.replace('₽', '').strip())

        assert total_price == expected_price, f"Ожидаемая цена: {expected_price}, фактическая: {total_price}"
