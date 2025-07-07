import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from pages.address_modal import AddressModal


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get("https://eda.yandex.ru")
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//body[not(contains(@class, 'loading'))]")
        ))
        return self

    @allure.step("Установить адрес доставки: {address}")
    def set_delivery_address(self, address):
        try:
            self._click_delivery_button()
            modal = AddressModal(self.driver)
            modal.enter_address(address)
            modal.select_first_suggestion()
            modal.confirm_address()
            return self
        except Exception as e:
            self._take_screenshot("set_address_error")
            raise Exception(f"Ошибка при установке адреса: {str(e)}")

    def _click_delivery_button(self):
        locators = [
            (By.XPATH, "//button[.//div[contains(text(), 'Куда доставить')]]"),
            (By.CSS_SELECTOR, "button[data-testid='address_button']")
        ]

        for locator in locators:
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.actions.move_to_element(element).click().perform()
                return
            except:
                continue
        raise Exception("Не удалось найти кнопку доставки")

    def _take_screenshot(self, name):
        try:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {str(e)}")

    @allure.step("Поиск ресторана {name}")
    def search_restaurant(self, name):
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='search_input']"))
        )
        search_input.clear()
        search_input.send_keys(name)
        from pages.restaurant_page import RestaurantPage
        return RestaurantPage(self.driver)