import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    """
    Класс для централизованного хранения конфигурации проекта.
    Все настройки могут быть переопределены через переменные окружения.
    """

    # Базовые настройки
    BASE_URL: str = os.getenv("BASE_URL", "https://eda.yandex.ru")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://eda.yandex.ru/api")
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "10"))

    # Настройки браузера
    BROWSER: str = os.getenv("BROWSER", "chrome").lower()
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    WINDOW_SIZE: str = os.getenv("WINDOW_SIZE", "1920x1080")

    # Настройки API
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "5"))
    API_MAX_RETRIES: int = int(os.getenv("API_MAX_RETRIES", "3"))

    # Настройки отчетов
    ALLURE_RESULTS_DIR: str = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
    SCREENSHOTS_DIR: str = os.getenv("SCREENSHOTS_DIR", "reports/screenshots")

    # Настройки окружения
    ENV: str = os.getenv("ENV", "dev").lower()
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Логирование
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")

    @classmethod
    def get_browser_settings(cls) -> Dict[str, Any]:
        """Возвращает настройки браузера в виде словаря"""
        return {
            "browser": cls.BROWSER,
            "headless": cls.HEADLESS,
            "window_size": tuple(map(int, cls.WINDOW_SIZE.split('x'))),
            "timeout": cls.DEFAULT_TIMEOUT
        }

    @classmethod
    def get_api_settings(cls) -> Dict[str, Any]:
        """Возвращает настройки API в виде словаря"""
        return {
            "base_url": cls.API_BASE_URL,
            "timeout": cls.API_TIMEOUT,
            "max_retries": cls.API_MAX_RETRIES
        }

    @classmethod
    def get_random_address(cls) -> str:
        """Возвращает случайный тестовый адрес"""
        import random
        return random.choice(cls.TEST_ADDRESSES)

    @classmethod
    def get_report_settings(cls) -> Dict[str, str]:
        """Возвращает настройки отчетов"""
        return {
            "allure_dir": cls.ALLURE_RESULTS_DIR,
            "screenshots_dir": cls.SCREENSHOTS_DIR
        }


# Экземпляр конфигурации для импорта
config = Config()