PYTHON=venv/bin/python3

.DEFAULT:
	help

help:
	@echo "I don't know what you want me to do."

init:
	python3 -m venv venv
	${PYTHON} -m pip install -r requirements.txt

init-dev:
	python3 -m venv venv
	${PYTHON} -m pip install -r requirements_dev.txt

run-pivni-valka:
	${PYTHON} run_pivni_valka.py

run-pivni-valka-notificationless:
	${PYTHON} run_pivni_valka.py --notificationless

run-pivni-valka-local:
	${PYTHON} run_pivni_valka.py --local

publish-pivni-valka:
	${PYTHON} run_pivni_valka.py --publish

test-pivni-valka:
	${PYTHON} -m pytest tests/pivni_valka

run-hospody:
	${PYTHON} run_hospody.py

run-hospody-local:
	${PYTHON} run_hospody.py --local

test-hospody:
	${PYTHON} -m pytest tests/hospody

run-notifier:
	${PYTHON} run_notifier.py

run-notifier-notificationless:
	${PYTHON} run_notifier.py --notificationless

run-notifier-ambasada:
	${PYTHON} run_notifier.py --ambasada

run-archivist:
	${PYTHON} run_archivist.py

mypy:
	${PYTHON} -m mypy --ignore-missing-imports --strict  --exclude tests .
	${PYTHON} -m mypy --ignore-missing-imports  tests

flake8:
	${PYTHON} -m flake8 --color=always .

pylint:
	${PYTHON} -m pylint -j 0 --output-format=colorized --recursive=y .

remove-pivni-valka-stats-duplicates:
	echo "$$(uniq pivni_valka/stats.csv)" > pivni_valka/stats.csv

black:
	${PYTHON} -m black --line-length 120 .

test:
	${PYTHON} -m pytest

coverage:
	${PYTHON} -m coverage run -m pytest
	${PYTHON} -m coverage report -m

save-db-to-file:
	${PYTHON} -m run_tool save-db-to-file

before-commit:
	make black
	make test
	make ruff
	make mypy
	make flake8
	make pylint

ipython:
	${PYTHON} -c "import IPython;IPython.terminal.ipapp.launch_new_instance();"


ruff:
	${PYTHON} -m ruff check .
