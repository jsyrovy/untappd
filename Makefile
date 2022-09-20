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
	@echo "make run-hospody"
	@echo "  download stats and publish page"
	@echo "make run-hospody-local"
	@echo "  generate stats and publish page"
	@echo "make test-hospody"
	@echo "  run tests"
	@echo "make run-notifier"
	@echo "  download current beer offer and send notification"
	@echo "make run-notifier-tweetless"
	@echo "  download current beer offer without notification"
	@echo "make mypy-install-types"
	@echo "  install mypy types"
	@echo "make mypy"
	@echo "  run mypy test"

init:
	python3 -m venv venv
	${PYTHON} -m pip install -r requirements.txt

run-pivni-valka:
	${PYTHON} run_pivni_valka.py

run-pivni-valka-tweetless:
	${PYTHON} run_pivni_valka.py --tweetless

run-pivni-valka-local:
	${PYTHON} run_pivni_valka.py --local

test-pivni-valka:
	${PYTHON} -m pytest pivni_valka/tests.py

run-hospody:
	${PYTHON} run_hospody.py

run-hospody-local:
	${PYTHON} run_hospody.py --local

test-hospody:
	${PYTHON} -m pytest hospody/tests.py

run-notifier:
	${PYTHON} run_notifier.py

run-notifier-tweetless:
	${PYTHON} run_notifier.py --tweetless

mypy:
	${PYTHON} -m mypy --ignore-missing-imports .

remove-pivni-valka-stats-duplicates:
	echo "$$(uniq pivni_valka/stats.csv)" > pivni_valka/stats.csv
