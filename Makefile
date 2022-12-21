PYTHON=venv/bin/python3

.DEFAULT:
	help

help:
	@echo "I don't know what you want me to do."

init:
	python3 -m venv venv
	${PYTHON} -m pip install -r requirements.txt

run-pivni-valka:
	${PYTHON} run_pivni_valka.py

run-pivni-valka-tweetless:
	${PYTHON} run_pivni_valka.py --tweetless

run-pivni-valka-local:
	${PYTHON} run_pivni_valka.py --local

publish-pivni-valka:
	${PYTHON} run_pivni_valka.py --publish

test-pivni-valka:
	${PYTHON} -m pytest pivni_valka/tests

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

flake8:
	${PYTHON} -m flake8 .

remove-pivni-valka-stats-duplicates:
	echo "$$(uniq pivni_valka/stats.csv)" > pivni_valka/stats.csv

black:
	${PYTHON} -m black .
