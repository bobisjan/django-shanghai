PY := python3
PY_VERSION := $(shell ${PY} --version 2>&1 | cut -f 2 -d ' ')

serve:
	${PY} tests/project/manage.py runserver 8000

test:
	${PY} setup.py test
.PHONY: test
