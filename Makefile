PY := python3
PY_VERSION := $(shell ${PY} --version 2>&1 | cut -f 2 -d ' ')

test:
	${PY} -m unittest discover -s tests -p '*.py'
.PHONY: test
