# -------------------------------------
# MAKEFILE
# -------------------------------------


PYTHON = env/bin/python
PYTEST = pytest
FLAKE8 = flake8
TWINE = twine

#
# commands for artifact cleanup
#

.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -d -t f -name __pycache__ -exec rm -rf {} \;


#
# commands for testing
#

.PHONY: test
test: test.unittests test.flake8

.PHONY: test.flake8
test.flake8:
	${FLAKE8} .

.PHONY: test.unittests
test.unittests:
	${PYTEST} .


#
# commands for packaging and deploying to pypi
#

.PHONY: sdist
sdist: test
	${PYTHON} setup.py sdist
	${PYTHON}  setup.py bdist_wheel

.PHONY: release
release: clean sdist
	${TWINE} upload dist/*
