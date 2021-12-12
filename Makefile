PYTHON=venv/bin/python3

.DEFAULT:
	help

help:
	@echo "make help"
	@echo "  show help"
	@echo "make init"
	@echo "  create venv and install requirements"
	@echo "make run-pivni-valka"
	@echo "  download stats and publish page"
	@echo "make run-pivni-valka-local"
	@echo "  generate stats and publish page"
	@echo "make test-pivni-valka"
	@echo "  run tests"
	@echo "make run-pipa"
	@echo "  download stats and publish page"
	@echo "make run-pipa-local"
	@echo "  generate stats and publish page"
	@echo "make test-pipa"
	@echo "  run tests"
	@echo "make mypy-install-types"
	@echo "  install mypy types"
	@echo "make mypy"
	@echo "  run mypy test"

init:
	python3 -m venv venv
	${PYTHON} -m pip install -r requirements.txt

run-pivni-valka:
	${PYTHON} run_pivni_valka.py

run-pivni-valka-local:
	${PYTHON} run_pivni_valka.py --local

test-pivni-valka:
	${PYTHON} -m pytest pivni_valka/tests.py

run-pipa:
	${PYTHON} run_pipa.py

run-pipa-local:
	${PYTHON} run_pipa.py --local

test-pipa:
	${PYTHON} -m pytest pipa/tests.py

mypy:
	${PYTHON} -m mypy --ignore-missing-imports .

remove-pivni-valka-stats-duplicates:
	echo "$$(uniq pivni_valka/stats.csv)" > pivni_valka/stats.csv
