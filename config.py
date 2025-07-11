# Базовый URL API
BASE_URL = "https://eda.yandex.ru/api"

# Параметры авторизации
TEST_COOKIES = {
            "i": "oEMzoEY09E2D/GZFIy8SgGyoVNA/Uyi8MMdoggS3PoH7lUupNRL1/mYlMa62BiKWJcDe8K2cBXB3zHMlbW9KEJRy/98=",
            "yandexuid": "3757153871751567771",
            "Session_id": "3:1751567806.5.0.1751567806321:FTNPXw:eed4.1.2:1|44566069.-1.2.3:1751567806.6:2088431762.7:1751567806|3:10309889.290291.wfkPsm8C6E4tQJdidXc0xcFq0Oo"
        }

TEST_HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }


# Общие параметры запросов
COMMON_QUERY_PARAMS = {
    "longitude": 43.90708,
    "latitude": 56.33089,
    "screen": "menu",
    "shippingType": "delivery",
    "autoTranslate": "false"
}