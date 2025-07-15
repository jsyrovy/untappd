.DEFAULT:
	help

help:
	@echo "I don't know what you want me to do."

run-pivni-valka:
	uv run --no-dev run_pivni_valka.py

run-pivni-valka-notificationless:
	uv run --no-dev run_pivni_valka.py --notificationless

run-pivni-valka-local:
	uv run --no-dev run_pivni_valka.py --local

publish-pivni-valka:
	uv run --no-dev run_pivni_valka.py --publish

test-pivni-valka:
	uv run --dev pytest tests/pivni_valka

run-notifier:
	uv run --no-dev run_notifier.py

run-notifier-notificationless:
	uv run --no-dev run_notifier.py --notificationless

run-notifier-ambasada:
	uv run --no-dev run_notifier.py --ambasada

run-archivist:
	uv run --no-dev run_archivist.py

mypy:
	uv run --dev -m mypy --ignore-missing-imports --strict  --exclude tests .
	uv run --dev -m mypy --ignore-missing-imports  tests

remove-pivni-valka-stats-duplicates:
	echo "$$(uniq pivni_valka/stats.csv)" > pivni_valka/stats.csv

format:
	uvx ruff format

test:
	uv run --dev -m pytest

coverage:
	uv run --dev -m coverage run -m pytest
	uv run --dev -m coverage report -m

save-db-to-file:
	uv run --no-dev -m run_tool save-db-to-file

before-commit:
	make format
	make test
	make lint-fix
	make mypy

ipython:
	uv run --dev python -c "import IPython;IPython.terminal.ipapp.launch_new_instance();"

lint:
	uvx ruff check

lint-fix:
	uvx ruff check --fix

ty:
	uvx ty check