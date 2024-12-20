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

run-hospody:
	uv run --no-dev run_hospody.py

run-hospody-local:
	uv run --no-dev run_hospody.py --local

test-hospody:
	uv run --dev -m pytest tests/hospody

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

flake8:
	uv run --dev -m flake8 --color=always .

pylint:
	uv run --dev -m pylint -j 0 --output-format=colorized --recursive=y .

remove-pivni-valka-stats-duplicates:
	echo "$$(uniq pivni_valka/stats.csv)" > pivni_valka/stats.csv

black:
	uv run --dev -m black --line-length 120 .

test:
	uv run --dev -m pytest

coverage:
	uv run --dev -m coverage run -m pytest
	uv run --dev -m coverage report -m

save-db-to-file:
	uv run --no-dev -m run_tool save-db-to-file

before-commit:
	make black
	make test
	make ruff
	make mypy
	make flake8
	make pylint

ipython:
	uv run --dev python -c "import IPython;IPython.terminal.ipapp.launch_new_instance();"


ruff:
	uv run --dev -m ruff check .
