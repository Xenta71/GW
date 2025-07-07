import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import Settings
from config.test_data import TestData


@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    if Settings.HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def auth_driver(browser):
    browser.get(Settings.BASE_URL)

    # Добавляем куки для авторизации
    for name, value in TestData.COOKIES.items():
        browser.add_cookie()

    browser.refresh()
    yield browser

@pytest.fixture
def base_url():
    return os.getenv("BASE_URL", "https://eda.yandex.ru")


@pytest.fixture
def default_timeout():
    return int(os.getenv("DEFAULT_TIMEOUT", 10))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "browser" in item.fixturenames:
                browser = item.funcargs["browser"]
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")