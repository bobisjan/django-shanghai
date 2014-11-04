PY := python3
PY_VERSION := $(shell ${PY} --version 2>&1 | cut -f 2 -d ' ')

COVERAGE := bin/coverage-3.4


serve:
	${PY} tests/project/manage.py runserver 8000

coverage:
	${COVERAGE} run --source=shanghai setup.py test
	${COVERAGE} report

test:
	${PY} setup.py test
.PHONY: test
