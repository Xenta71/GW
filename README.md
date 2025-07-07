# GW
Graduate work on QA Engineering course

## Шаблон для автоматизации тестирования на Python

### Шаги:
1. Склонировать репозиторий 'git clone https://github.com/Xenta71/GW.git'
2. Установить зависимости
3. Запустить тесты 'pytest'

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy
- allure
- config

### Полезные ссылки
- [Подсказка по markdown] (https://www.markdownguide.org/cheat-sheet)
- [Генератор файла .gitignore] (https://www.toptal.com/developers/gitignore/)

### Библиотеки
- pip install pytest
- pip install selenium
- pip install webdriver-manager
**# Автотесты для Яндекс.Еды
- 
- ## Структура проекта
- `config/` - настройки и тестовые данные
- `pages/` - Page Object модели
- `tests/` - тесты (UI и API)
- `utils/` - вспомогательные функции

## Запуск тестов
1. Установить зависимости: `pip install -r requirements.txt`
2. Запуск всех тестов: `pytest`
3. Только UI тесты: `pytest tests/test_ui.py`
4. Только API тесты: `pytest tests/test_api*.py`
5. С отчетом Allure: `pytest --alluredir=allure-results && allure serve allure-results`

## Дополнительно
- Для проверки стиля: `flake8 .`
- Для линтинга: `pylint **/*.py`******

