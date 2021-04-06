SHELL := /bin/bash
CMD_INSTALL := pip install -r
PYTHON := ./venv/bin/python


help:
	@echo '=========================== Список команд ==========================='
	@echo 'make run:             Запуск бота, по умолчанию в режиме разработки'
	@echo 'make locales-build:   Компилляция переводов'
	@echo 'make install-dev:     Установка зависимостей для разработки'
	@echo 'make install:         Установка зависимостей для релиза'
	@echo 'make test:            Запуск тестов'
	@echo ''
	@echo '======================= Переменные окружения ========================'
	@echo 'ENV:                  Определяет режиме запуска'
	@echo 'CONFIG_PATH:          Путь до файла конфигурации'

run:
	if [ -f './.env' ]; then \
		export $(shell sed 's/===*//'g .env); \
	fi; \
	export PYTHONPATH=./app:$$PYTHONPATH; \
	export ENV=develop; \
	export CONFIG_PATH=./etc/app/app.yaml; \
	$(PYTHON) ./app/main.py


locales-build:
	pybabel compile -d ./app/ui/locales/ -D app;


install-dev:
	$(CMD_INSTALL) ./requirements-dev.txt


install:
	$(CMD_INSTALL) ./requirements.txt


test:
	export PYTHONPATH=./app:$$PYTHONPATH; \
	export ENV=testing; \
	export CONFIG_PATH=./etc/app/app.yaml; \
	rm -rf ./tests/ui/locales/en ./tests/ui/locales/ru ./tests/ui/locales/text.pot; \
	pybabel extract --input-dirs=./tests/ui/locales -o ./tests/ui/locales/text.pot;\
	pybabel init -i ./tests/ui/locales/text.pot -d ./tests/ui/locales -D text -l en; \
	pybabel compile -d ./tests/ui/locales/ -D text; \
	pybabel init -i ./tests/ui/locales/text.pot -d ./tests/ui/locales -D text -l ru; \
	flake8 ./app ./tests/; \
	pytest ./; \
	rm -rf ./tests/ui/locales/en ./tests/ui/locales/ru ./tests/ui/locales/text.pot;
