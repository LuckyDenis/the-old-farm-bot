Игровой телеграм бот: The Old Farm v2
-------------------------------------

### Статус тестов
|Ветка | Статус |
|------|--------|
|Master|[![CI](https://github.com/LuckyDenis/the-old-farm-bot/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/LuckyDenis/the-old-farm-bot/actions/workflows/ci.yaml) |
|Dev   |[![CI](https://github.com/LuckyDenis/the-old-farm-bot/actions/workflows/ci.yaml/badge.svg?branch=dev)](https://github.com/LuckyDenis/the-old-farm-bot/actions/workflows/ci.yaml)|


### Команды makefile
|Команда              | Описание                                      |
|---------------------|-----------------------------------------------|
|`make run`           | Запуск бота, по умолчанию в режиме разработки |
|`make locales-build` | Компилляция переводов                         | 
|`make install-dev`   | Установка зависимостей для разработки         |
|`make install`       | Установка зависимостей для релиза             |
|`make test`          | Запуск тестов                                 |
|`make migrate-commit`| Создает автоматический commit для базы данных |
|`make migrate-update`| Отправит изменения в базу данных              |

### Переменные окружения
|Имя переменной  | Описание                 |
|----------------|--------------------------|
|`ENV`           |Определяет режиме запуска |
|`CONFIG_PATH`   |Путь до файла конфигурации|
