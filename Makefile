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
	@echo "make test-pivni-valka"
	@echo "  run tests"

init:
	python3 -m venv venv
	${PYTHON} -m pip install -r pivni-valka/requirements.txt

run-pivni-valka:
	${PYTHON} pivni-valka/run.py

run-pivni-valka-local:
	${PYTHON} pivni-valka/run.py --local

test-pivni-valka:
	${PYTHON} -m pytest pivni-valka/tests.py
