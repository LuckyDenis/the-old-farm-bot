SHELL := /bin/bash
CMD_INSTALL := pip install -r
PYTHON := ./venv/bin/python

run:
	export PYTHONPATH=./app:$$PYTHONPATH; \
	export ENV=develop; \
	export CONFIG_PATH=./etc/app/app.yaml; \
	$(PYTHON) ./app/main.py

install-dev:
	$(CMD_INSTALL) ./requirements-dev.txt

install:
	$(CMD_INSTALL) ./requirements.txt


test-full:
	export PYTHONPATH=./app:$$PYTHONPATH; \
	export ENV=testing; \
	export CONFIG_PATH=./etc/app/app.yaml; \
	flake8 ./app ./tests/; pytest ./

test:
	pytest ./

flake8:
	flake8 ./app ./tests/

