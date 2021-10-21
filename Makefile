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

init:
	python3 -m venv venv
	${PYTHON} -m pip install -r pivni_valka/requirements.txt

run-pivni-valka:
	${PYTHON} run_pivni_valka.py

run-pivni-valka-local:
	${PYTHON} run_pivni_valka.py --local

test-pivni-valka:
	${PYTHON} -m pytest pivni_valka/tests.py
